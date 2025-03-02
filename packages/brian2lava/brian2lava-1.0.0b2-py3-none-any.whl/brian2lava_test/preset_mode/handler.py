from jinja2 import FileSystemLoader, Environment
import os
import importlib
import inspect
import warnings
import re
import numpy as np
from brian2lava_test.utils.files import scrap_folder
from brian2 import get_device, get_logger
from brian2 import NeuronGroup, SpikeGeneratorGroup
from brian2.synapses.synapses import SynapticPathway, Synapses
from brian2.core.variables import DynamicArrayVariable
from brian2lava_test.utils.math import sparse_to_dense, F2F, generate_spikes, check_convert_int
from brian2lava_test.utils.files import get_module_name
from brian2lava_test.utils.const import HARDWARE, objects_f2f, LOIHI2_MANTISSA_MAX_VALUE
from brian2lava_test.preset_mode.model_loader import ModelLoader


class PresetProcessHandler():

	def __init__(self, device, obj):
		"""
		PresetProcessHandler.
		The main scope of this class is:
		 1. to organize the files required by the preset_mode simulation
		 2.	operate a translation of the arguments required by the preset models between brian and lava.
		These two mechanisms take place in: 'copy_files_to_workspace()' and 'translate_arg()' respectively.
		"""
		# Keep count of how many processmodel files exist
		# To make it a bit clearer we use a char counter, I expect there won't be more than 20 PM files for a process..
		self.proc_model_counter = 'a'
		

		# Store device and brian object to manage
		self.device = device
		self.brian_object = obj
		self.base_name = str(device.hardware) + '_' + device.mode + '_' + self.brian_object.name

		# Get variables and parameters of neuron group
		self.variables = self.brian_object.variables
		self.parameters = self.get_namespace_parameters()
		
		self.class_name = None # Will be set at a later stage
		self.ucode_extensions = None
		self.model = self.check_for_model_compatibility()
		# Synapses don't need microcode so we don't need direct access to files or code generation.
		if self.model:
			# Copy the files for this process to the workspace folder and
			# initialize the generator for the ucode file
			self.model_path = self.copy_files_to_workspace()
			self.generator = MicrocodeGenerator(obj, 
									            model_path = self.model_path, 
									            extension = self.ucode_extensions['template'], 
			                                    variables = self.variables, 
												params = self.parameters)
	
	@staticmethod
	def requires_float2fixed_converter(brian_object, device):

		# If user has chosen fixed-point computation and F2F conversion
		if device.is_using_f2f():
			# If given object is eligible for F2F conversion
			if isinstance(brian_object, objects_f2f):
				return True
		
		# using floating point repr.
		return False
	
	def check_for_model_compatibility(self):
		# We only have models for neurongroups 
		if isinstance(self.brian_object, NeuronGroup):
			for model in ModelLoader.preset_models:
				# Check if the model defined by the equations is available to the device
				if self.brian_object.user_equations == model.equations:
					self.class_name = model.process_name
					self.ucode_extensions = model.ucode_extensions
					return model
			
			# This error message should be updated to be more informative on what models are available for each brian object.
			available_eq = '\n'.join([f"-- {model.process_name} --\n{str(model.equations)}" for model in ModelLoader.preset_models])
			msg = (f"No implementation corresponding to the equations used for '{self.brian_object.name}' has been found.\n"
			       f"Please make sure that all the objects in your simulation use models from the currently available models: \n"
		           f"{available_eq}")	
			raise ValueError(msg)
		# Synapses case
		elif isinstance(self.brian_object,SynapticPathway):
			# Make sure that the on_pre and on_post conditions are compatible with our implementation.
			self.class_name = "Dense"
			return None
		
		elif isinstance(self.brian_object, SpikeGeneratorGroup):
			self.class_name = "RingBuffer"
			return None


	
	def copy_files_to_workspace(self):
		"""
		Based on the available Loihi models, get all the files required to run this process
		and copy them into the project folder. These files will be then used to run the simulation.
  
		Returns
		-------
		model.path : `string`
			Path to the model
		"""
		model =  self.model

		# Scrap the model folder for the required files.
		file_contents = ''
		files = scrap_folder(model.path,endswith = 'process.py', max_files=1, return_full_path=True)
		files.extend(scrap_folder(model.path,endswith = 'process_model.py', max_files=None, return_full_path=True))
		# We create a single file containing process and process models, to avoid problems with imports later on
		for file in files:
			with open(file,'r') as f:
				contained_code = f.read()
				# Scan for the 'ucoded' tag from NeuroCore ProcessModels
				if 'ucoded' in contained_code:
					# Don't copy the contents of the NeuronCore processmodel if we're not using Loihi
					# to avoid import errors due to non-existent nc files.
					if self.device.runtime_tag == 'ucoded': 
						# If the microcode is generated, it will be found at this location
						ucode_file_loc = os.path.join(self.device.project_dir,self.base_name+self.ucode_extensions['file'])
						# Define the path to the microcode file globally in the generated code file
						contained_code = f'ucode_file = "{ucode_file_loc}"\n' + contained_code
					else:
						continue
				file_contents += '\n' + contained_code
		# Write the file in the project folder.
		self.device.writer.write(self.base_name+'.py',file_contents)

		# If there is a plain ucode file we make sure to copy it to the folder. If a template is also present, this will be overwritten later on.
		ucode_file = scrap_folder(model.path,endswith=self.ucode_extensions["file"], max_files=1,empty_ok=True,return_full_path=True)
		if ucode_file:
			with open(ucode_file[0],'r') as ucode_f:
				self.device.writer.write(self.base_name+self.ucode_extensions['file'],ucode_f.read())

		return model.path

	def get_namespace_parameters(self):
		"""
		get_namespace_parameters
		"""

		parameters = {}
		for obj in self.brian_object._contained_objects:
			parameters.update(obj.codeobj.namespace)

		return parameters

	def get_lava_process_kwargs(self):
		"""
		Initialize keyword arguments for Lava process with user-defined variables and parameters
  
		Returns
		-------
		kwargs : `dict`
			A dictionary of keyword arguments
		
		Note that the functionality given by this function could easily be extended to already initialize the 
		Processes themselves. The reason why we don't do that here is that we have to keep the Loihi implementation
		compatible with the CPU implementation. This means that the modules are loaded one more time in the device.run()
		and Processes are initialized there.
		"""
		module_name = get_module_name(self.brian_object,self.device.project_dir,self.base_name)
		try:
			process = getattr(importlib.import_module(module_name),self.class_name)
		except Exception as e:
			if type(e) == AttributeError:
				raise ImportError(
					f"An exception occurred while trying to import {self.class_name} from {module_name}. " 
		      		"This could be caused by a mismatch between the class name specified in the '.json' file and the name in the "
			  		"Python file containing the definition of the Process class."
				)
			else:
				raise e

		# Get specs of init function from Process that contains all available keyword arguments
		specs = inspect.getfullargspec(process.__init__)
		# Extract keyword-only arguments
		arguments = specs.kwonlyargs
		# Remove 'log_config' to avoid raising warnings
		if 'log_config' in arguments:
			arguments.remove('log_config')
		if 'name' in arguments:
			arguments.remove('name')

		# Iterate over available keyword arguments from Process and
		# find a match in the existing user defined variables or parameters
		kwargs = self.collect_parameters(arguments, defaults = specs.kwonlydefaults)

		if PresetProcessHandler.requires_float2fixed_converter(self.brian_object,self.device):
			F2F.update_parameters(kwargs, owner_name=self.brian_object.name, exceptions=['shape'])

		# Spike generation on Loihi requires a spike adapter to act as intermediary between the generator and the synapses.
		if isinstance(self.brian_object, SpikeGeneratorGroup) and self.device.hardware == HARDWARE.Loihi2:
			kwargs['adapter_class'] = 'PyToNxAdapter'
			kwargs['adapter_module'] = 'lava.proc.embedded_io.spike'

		kwargs['class_name'] = self.class_name

		return kwargs
	
	def collect_parameters(self, arguments, defaults = {}):
		"""
		Finds parameters needed to instantiate the Lava Process in the Brian2 namespace and
		returns a dictionary mapping the keyword arguments to the right parameters.

		Parameters
		----------
		arguments : `list`
			A list of keyword arguments
		defaults : `dict`
			A dictionary of keyword arguments with their default values

		Returns
		-------
		dict_out : `dict`
			A dictionary mapping the keyword arguments to the right parameters
		"""
		dict_out = {}
		self.device.logger.debug(f"Lava process arguments = {sorted(arguments)}\n"
		                         f"Brian variables = {sorted(list(self.variables._variables.keys()))}\n"
		                         f"Brian parameters = {sorted(list(self.parameters.keys()))}")
		for arg in arguments:
			must_set_mant_exp = False
			# Mantissa/exponent related code
			if self.device.num_repr == "fixed" and ('_mant' in arg or arg == 'weights'):
				mant_name = arg
				# Remove the mant!
				if '_mant' in arg:
					arg = arg[:-5]
				exp_name = arg + "_exp" if not arg == 'weights' else 'weight_exp'
				if PresetProcessHandler.requires_float2fixed_converter(self.brian_object,self.device):
					F2F.add_mantissa_and_exp_param(arg, mant_name=mant_name,exp_name=exp_name) 
				else:
					must_set_mant_exp = True
			# Get argument values translated from Brian and leave if it is None
			val = self.translate_arg(arg)
			if val is None:
				if not '_exp' in arg:
					warnings.warn(f"Variable or parameter '{arg}' was not defined. The default value " +
					              f"{defaults.get(arg, None)} from Process is used.")
				continue
			# If fixed-point representation has been requested, check values, and convert them to 32-bit integers
			# TODO This code could also serve as a test for `use_f2f == True` after F2F conversion has been done
			if self.device.num_repr == "fixed" and not self.device.use_f2f and not arg == "shape":
				val = check_convert_int(val, arg)
			# Add value to dictionary
			dict_out[arg] = val
			# Mantissa/exponent without F2F (but algorithm same as in `F2F.float_to_mantissa_exponent()`)
			if must_set_mant_exp:
				dict_out.pop(arg)
				'''
				max_val = LOIHI2_MANTISSA_MAX_VALUE.weights if arg == 'weights' else LOIHI2_MANTISSA_MAX_VALUE.other
				print(f"arg = {arg}, max_val = {max_val}, val = {val}")
				req_shift = np.int32(min(np.log2(max_val/val), 0)) # negative or zero
				mant = 2**req_shift * val
				exp = max(- req_shift, 0) # positive or zero
				'''
				mantissa = exponent = 0
				if np.any(val != 0):
					# Find out if the weights are larger than the 8 bit maximum allowed and by how many bits
					max_val = LOIHI2_MANTISSA_MAX_VALUE.weights if arg == 'weights' else LOIHI2_MANTISSA_MAX_VALUE.other
					max_bit_to_weight_ratio = np.log2(max_val/np.max(abs(val)))
					# Only shift the weights if the previous calculation returned a negative value (use floor for extra safety)
					mantissa_shift = np.floor(min(max_bit_to_weight_ratio, 0))
					mantissa = np.int32(val * 2**mantissa_shift)
					# Only need the exponent if we had to downscale our weights (so sign(mantissa_shift)==-1)
					exponent = np.int32(max(-mantissa_shift, 0))
				#print(f"arg = {arg}, mantissa = {mantissa}, exponent = {exponent}")
				dict_out[mant_name] = mantissa
				dict_out[exp_name] = exponent
			
		return dict_out
	
	def translate_arg(self, arg):
		"""
		Interprets an argument for the Lava Process and returns the corresponding
		value taken from the Brian objects after some preprocessing to translate them
		into a lava-compatible format.

  		Parameters
		----------
		arg : `string`
			The name of a keyword argument

   		Returns
		-------
		diverse : `any`
			The value of the keyword argument, from Brian
		"""
		# Special variables
		if arg == 'shape':
			return (self.variables['N'].get_value(),)
		elif arg == 'weights' and isinstance(self.brian_object,SynapticPathway):
			pathway = self.brian_object
			i = self.device.get_value(pathway.synapse_sources,access_data = True)
			j = self.device.get_value(pathway.synapse_targets,access_data = True)
			w = self.variables['w'].get_value()
			# Multiply by dt to account for the fact that Lava implements integration without taking
			# timestep size into account.
			# w *= self.device.defaultclock.dt_
			n_rows = pathway.source.N
			n_cols = pathway.target.N
			return sparse_to_dense(i,j,w,n_rows=n_rows,n_cols=n_cols)
		# SpikeGeneratorGroup
		elif arg == 'data' and isinstance(self.brian_object, SpikeGeneratorGroup):
			neuron_index = self.brian_object.variables["neuron_index"].get_value()
			timebins = self.brian_object.variables["_timebins"].get_value()
			period_bins = self.brian_object.variables["_period_bins"].get_value()
			num_neurons = self.brian_object.N
			N_timesteps = int(self.device.duration / self.device.defaultclock.dt)
			spikes = generate_spikes(neuron_index,timebins,period_bins,num_neurons,N_timesteps)
			return spikes
		# Fixed-point decay constants: compute from time constant and time step 
		elif arg == 'delta_j' or arg == 'delta_v':
			tau_name = f'tau_{arg[-1]}'
			dt = self.device.defaultclock.dt_
			# Get the time constant (clip to `dt` for "delta" synapses)
			timescale = max(dt, self.parameters[tau_name])
			# Do 12-bit shift, but only for fixed-point models
			if self.device.num_repr == 'fixed':
				delta = check_convert_int((dt/timescale)*2**12, f"{arg} = dt/{tau_name}*2^12")
			else:
				delta = dt/timescale
			return delta
		# Threshold voltage
		elif arg == 'vth':
			_, _, cond_rhs_value =\
				BrianCondEvaluate.eval_threshold(self.brian_object, self.variables, self.parameters)
			return cond_rhs_value
		# Reset voltage
		elif arg == 'vrs':
			_, cond_rhs_value =\
				BrianCondEvaluate.eval_reset(self.brian_object, self.variables, self.parameters)
			return cond_rhs_value
		# Variables that don't need preprocessing
		elif arg in self.variables._variables.keys():
			if isinstance(self.variables[arg], DynamicArrayVariable):
				return self.variables[arg].get_value(access_data = True)
			return self.variables[arg].get_value()
		# Parameters that don't need preprocessing
		elif arg in self.parameters.keys():
			return self.parameters[arg]
		
		return None


	def generate_ucode(self):
		"""
		Generate the microcode from the jinja template and write it to a file. Uses
		an instance of the `MicrocodeGenerator` class.
		"""
		# This method is not used for synapses.
		if not isinstance(self.brian_object, NeuronGroup):
			return 
		ucode = self.generator.get_ucode()
		# Write the microcode to a file so that it can be used by the processmodel.
		if not self.generator.template_name is None:
			file_name = self.base_name + self.ucode_extensions['file']
			self.device.writer.write(file_name,ucode)
		# The template was not in the folder when we looked for it
		else:
			# Try to look for a non-templated script in the project directory. If it's there we don't need to do anything.
			try:
				scrap_folder(self.device.project_dir,startswith=self.base_name,endswith=self.ucode_extensions['file'])
			except FileNotFoundError:
				msg = f"""Neither a template with extension '{self.ucode_extensions['template']}' nor a '{self.ucode_extensions['file']}' file
				were found. In order to run a Loihi simulation, a file containing the code to be executed on Loihi is required. 
				Either a template or a predefined script can be provided. For more information, please read the brian2lava documentation for the
				Loihi implementation.
				"""
				raise FileNotFoundError(msg)

class BrianCondEvaluate:
	"""
	Abstract class providing methods to evaluate condition expressions in Brian. Mainly for threshold
	and reset conditions in neuron groups.
	"""
	@staticmethod
	def eval_reset(neuron_group, variables, parameters):
		"""
		Evaluates the reset condition of a Brian NeuronGroup.

		Parameters:
		-----------
		neuron_group : NeuronGroup
			The NeuronGroup object whose reset condition is to be evaluated.
		variables : dict
			Dictionary containing the current Brian variables.
		parameters : dict
			Dictionary containing the current Brian parameters.

		Returns:
		--------
		cond_variable
			The variable that the condition relates to.
		cond_rhs_value
			The value of the right-hand side of the condition after
			its evaluation.
		"""
		# Get reset condition and remove whitespaces
		rs_cond = neuron_group.event_codes['spike'].replace(' ', '')

		# Evaluate the condition and throw a warning if there is an unexpected variable or operator
		cond_variable, cond_operator, cond_rhs_value =\
			BrianCondEvaluate.eval_cond(rs_cond, variables, parameters)
		if cond_variable != "v":
			warnings.warn(f"Unexpected variable in reset condition '{rs_cond}'. Currently, Brian2Lava's preset mode only supports"
				           "conditions with the 'v' variable.")
		if cond_operator != "=":
			warnings.warn(f"Unexpected operator in reset condition '{rs_cond}'.")
			
		return cond_variable, cond_rhs_value


	@staticmethod
	def eval_threshold(neuron_group, variables, parameters):
		"""
		Evaluates the threshold condition of a Brian NeuronGroup.

		Parameters:
		-----------
		neuron_group : NeuronGroup
			The NeuronGroup object whose threshold condition is to be evaluated.
		variables : dict
			Dictionary containing the current Brian variables.
		parameters : dict
			Dictionary containing the current Brian parameters.

		Returns:
		--------
		cond_variable
			The variable that the condition relates to.
		cond_operator
			The operator (<= | >= | = | < | >) in the condition.
		cond_rhs_value
			The value of the right-hand side of the condition after
			its evaluation.
		"""
		# Get threshold condition and remove whitespaces
		th_cond = neuron_group.events['spike'].replace(' ', '')

		# Evaluate the condition and throw a warning if there is an unexpected variable or operator
		cond_variable, cond_operator, cond_rhs_value =\
			BrianCondEvaluate.eval_cond(th_cond, variables, parameters)
		if cond_variable != "v":
			warnings.warn(f"Unexpected variable in threshold condition '{th_cond}'. Currently, Brian2Lava's preset mode only supports"
				           "conditions with the 'v' variable.")
		if cond_operator != ">":
			warnings.warn(f"Unexpected operator in threshold condition '{th_cond}'. Currently, Brian2Lava's preset mode only supports"
				           "conditions with the '>' operator.")
			
		return cond_variable, cond_operator, cond_rhs_value

	@staticmethod
	def eval_cond(cond, variables, parameters):
		"""
		Evaluates a Brian condition.

		Parameters:
		-----------
		cond : str
		    The condition expression to be evaluated.
		variables : dict
			Dictionary containing the current Brian variables.
		parameters : dict
			Dictionary containing the current Brian parameters.

		Returns:
		--------
		cond_variable
			The variable that the condition relates to.
		cond_operator
			The operator (<= | >= | = | < | >) in the condition.
		cond_rhs_value
			The value of the right-hand side of the condition after
			its evaluation.
		"""
		# Split statement, get variable and right-hand side of the condition
		cond_operator = re.search("(?:<=|>=|=|<|>)", cond).group(0)
		cond_statement = cond.split(cond_operator)
		cond_variable = cond_statement[0]
		cond_rhs = cond_statement[1]
			
		# Replace parameters in right-hand side with values
		# TODO This is a bit dangerous if there are overlapping names.
		# 	We should use brian's parsing tools to make it a bit more solid.
		for k, v in parameters.items():
			cond_rhs = cond_rhs.replace(k, str(v))

		# Raise an error if variables are used in the right-hand side
		for k, v in variables.items():
			if cond_rhs.find(k) != -1:
				raise Exception(f"Error in condition '{cond}': currently, "
					             "only parameters may be used, not variables.")

		# Evaluate reset condition and obtain scaled threshold value
		exec_vars = {}
		exec(f'cond_rhs_value = {cond_rhs}', globals(), exec_vars)
		cond_rhs_value = exec_vars['cond_rhs_value']

		return cond_variable, cond_operator, cond_rhs_value

class MicrocodeGenerator():
	"""
	A generator to fill in the gaps in the microcode templates.
	Allows for the definition of custom quantities such as thresholds, reset conditions, etc.
	By default, it will treat each of the keyword arguments given during the initialization of a 
	BrianObject and manage each separately. 
	"""
	def __init__(self,obj, model_path = None, name = 'process', extension = '.j2', params = {}, variables = {}):
		self.device = get_device()
		self.object_name = name
		self.extension = extension
		self.brian_object = obj
		self.parameters = params
		self.variables = variables
		self.template_dir = model_path
		# Get path to template
		self.template_name = scrap_folder(model_path, endswith=self.extension, max_files=1,empty_ok=True)
		if not len(self.template_name):
			self.device.logger.debug(f"No template for this model's microcode was found. Object related to this model: {self.brian_object}")
			self.template_name = None
		else:
			self.template_name = self.template_name[0]

	
	def get_ucode(self):
		"""
		get_ucode
		"""
		# If there is no template (e.g. for SynapticPathway)
		if self.template_name is None:
			return ""

		template_kwds = self.eval_code_conditions()
		
		# Defined Jinja file system loader based on a path to the template files
		loader = FileSystemLoader(searchpath=self.template_dir)
		
		# Return the environment, containing the file loader
		env = Environment(
			loader=loader,
			trim_blocks=True,
			lstrip_blocks=True
		)

		# Load and render the microcode
		ucode_template = env.get_template(self.template_name)
		ucode_rendered = ucode_template.render(
			**template_kwds
		)

		return ucode_rendered
	

	def eval_code_conditions(self):
		"""
		Here we go through all the possible conditions defined by the user in the simulation
		and generate a dictionary of keywords which will be used by jinja to generate the file 
		from the template.
		"""
		template_kwds = {}
		if isinstance(self.brian_object, NeuronGroup):
			# Reset
			template_kwds.update(self.eval_reset())

			# Threshold
			template_kwds.update(self.eval_threshold())

		return template_kwds
	

	def eval_reset(self):
		"""
		Method getting attributes related to the reset condition of a NeuronGroup.

		Returns:
		--------
		dict
			Dictionary containing items for reset variable and value.
		"""
		loihi_reset_variable, loihi_reset_value = \
			BrianCondEvaluate.eval_reset(self.brian_object, self.variables, self.parameters)

		# Do float-to-fixed conversion if it is requested
		if self.device.is_using_f2f():
			loihi_reset_value = F2F.float_to_fixed(loihi_reset_value)

		return {'rs_var': loihi_reset_variable, 'rs_val': loihi_reset_value}


	def eval_threshold(self):
		"""
		Method getting attributes related to the threshold condition of a NeuronGroup.

		Returns:
		--------
		dict
			Dictionary containing items for threshold variable and value.
		"""
		loihi_threshold_variable, _, loihi_threshold_value = \
			BrianCondEvaluate.eval_threshold(self.brian_object, self.variables, self.parameters)

		# Do float-to-fixed conversion if it is requested
		if self.device.is_using_f2f():
			loihi_threshold_value = F2F.float_to_fixed(loihi_threshold_value)

		return {'th_var': loihi_threshold_variable, 'th_val': loihi_threshold_value}