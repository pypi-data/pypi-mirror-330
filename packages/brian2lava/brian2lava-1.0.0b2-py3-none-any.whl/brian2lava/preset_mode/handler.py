from jinja2 import FileSystemLoader, Environment
import os
import importlib
import inspect
import re
import numpy as np
from brian2lava.utils.files import scrap_folder
from brian2 import get_device, Quantity, units, second
from brian2 import NeuronGroup, SpikeGeneratorGroup
from brian2.synapses.synapses import SynapticPathway, Synapses
from brian2.core.variables import ArrayVariable, DynamicArrayVariable, Subexpression
from brian2lava.utils.math import sparse_to_dense, generate_spikes, check_convert_to_int32
from brian2lava.utils.f2f import ModelWiseF2F as F2F
from brian2lava.utils.files import get_module_name
from brian2lava.utils.const import HARDWARE, objects_using_f2f, LOIHI2_SPECS, EPSILON
from brian2lava.preset_mode.model_loader import ModelLoader
from brian2lava.preset_mode.lava_parameters import LavaParameters
from brian2 import get_logger


class PresetProcessHandler():
	"""
	Handler class with the purpose to:
	
	1. retrieve the files required by the preset mode simulation,
	
	2. operate a translation between Brian and Lava of the arguments required by the preset models.

	These two mechanisms take place in ``copy_files_to_workspace()`` and ``translate_arg()``, respectively.

	Parameters
	----------
	device : `Device`
		The current Brian device.
	obj : `BrianObject`
		Brian object corresponding to the loaded model.
	"""
	copied_lava_proc_files = False

	def __init__(self, device, obj):
		# Keep count of how many processmodel files exist
		# To make it a bit clearer we use a char counter, I expect there won't be more than 20 PM files for a process..
		self.proc_model_counter = 'a'

		# Store device and brian object to manage
		self.device = device
		self.brian_object = obj
		self.base_name = str(device.hardware) + '_' + device.mode + '_' + self.brian_object.name

		# Get variables and parameters of Brian object
		self.variables = self.brian_object.variables
		self.parameters = self.get_namespace_parameters()
		
		# Class name of the Lava process, will be set below
		self.class_name = None

		# Neuron model, may be set below
		self.model = None

		# Case of neuron group (only for these, preset models are used)
		# -> search for applicable neuron model
		if isinstance(self.brian_object, NeuronGroup):
			self.model = self.find_compatible_model()
			self.class_name = self.model.process_name
			# Microcode file extensions
			# TODO Pass this as argument
			self.ucode_extensions = self.model.ucode_extensions

			# Copy the files for this process to the workspace folder and
			# initialize the generator for the ucode file.
			model_path = self.copy_model_files_to_workspace()
			self.generator = MicrocodeGenerator(obj, 
												model_path = model_path, 
												extension = self.ucode_extensions['template'], 
												variables = self.variables, 
												params = self.parameters)
		# Case of synapses or synaptic pathway
		elif isinstance(self.brian_object, (Synapses, SynapticPathway)):
			# TODO Make sure that the `on_pre` and `on_post` conditions are compatible with our implementation.
			self.class_name = "Dense"
			# Only copy files if customization is needed (due to the use of individual weight exponents)
			if device.use_exp_array:
				self.copy_lava_proc_files_to_workspace()
		# Case of spike generator group
		elif isinstance(self.brian_object, SpikeGeneratorGroup):
			self.class_name = "RingBuffer"
		# Case of unknown object
		# NOTE this should never be reached due to earlier handling by `check_for_brian2lava_support()`
		else:
			raise ValueError(f"Object type '{type(self.brian_object)}' is not supported by Brian2Lava in preset mode.")
		

	@staticmethod
	def f2f_converter_requested(brian_object, device):
		"""
		Checks if F2F conversion ha been requested.
  
		Returns
		-------
		`bool`
			``True if F2F conversion shall be used, ``False`` if not.
		"""

		# If user has chosen fixed-point computation and F2F conversion
		if device.is_using_f2f():
			# If given object is eligible for F2F conversion
			if isinstance(brian_object, objects_using_f2f):
				return True
		
		# using floating point repr.
		return False


	def find_compatible_model(self):
		"""
		Checks if the equations of the user-defined model equal those of any of the preset models. 
		In addition, sets the class name of the given object and, optionally, the ucode extensions.
  
		Returns
		-------
		model : `Model`
			If there is one, the preset model that corresponds to ``self.brian_object``,
			``None`` if the Brian object is not a ``NeuronGroup``.
		"""
		def compare_equations(user_equations, model_equations):
			"""
			Compare two equations objects for equality. Ignores simple state variable declarations.

			Parameters
			----------
			user_equations : `Equations`
				Equations object created from the equations provided by the user in the Brian script.
			model_equations : `Equations`
				Equations object created from the equations provided by a preset model.

			Returns
			-------
			`bool`
				Returns `True` if the equations match, `False` otherwise.
			"""
			user_equations_list = [user_equations[eq] for eq in user_equations]
			model_equations_list = [model_equations[eq] for eq in model_equations]
			# Check if all user-defined equations are contained in the list of model equations (ignoring statements
			# that do not contain an equals sign)
			for user_eq in user_equations_list:
				if not user_eq in model_equations_list and '=' in str(user_eq):
					return False
			# Check if all model equations are contained in the list of user-defined equations (ignoring statements
			# that do not contain an equals sign)
			for model_eq in model_equations_list:
				if not model_eq in user_equations_list and '=' in str(model_eq):
					return False
			return True

		def compare_conditions(user_conditions, model_conditions):
			"""
			Compare two dictionaries of conditions for their equality.

			Parameters
			----------
			user_conditions : `dict`
				Dictionary created from the conditions provided by the user in the Brian script.
			model_conditions : `dict`
				Dictionary created from the conditions provided by a preset model.

			Returns
			-------
			`int`
				Returns ``2`` if the conditions match, ``1`` if they match partially, and ``0`` otherwise.
			"""	
			only_partial = 0
			# Check if all user-defined equations are contained in the list of model equations
			for key in user_conditions.keys():
				user_conds = user_conditions[key]
				model_conds = model_conditions.get(key, "")
				user_conds = [user_conds] if not isinstance(user_conds, list) else user_conds
				model_conds = [model_conds] if not isinstance(model_conds, list) else model_conds
				# Check if number of sub-conditions matches
				if len(user_conds) != len(model_conds):
					return 0
				# Loop over sub-conditions
				for user_cond, model_cond in zip(user_conds, model_conds):
					user_cond = user_cond.replace(' ', '')
					model_cond = model_cond.replace(' ', '')
					# Check for perfect match between conditions
					if user_cond == model_cond:
						continue
					# Check for matching variables and operators
					user_var, user_op, _ = BrianCondEvaluate.eval_cond(user_cond, eval_rhs_value = False)
					model_var, model_op, _ = BrianCondEvaluate.eval_cond(model_cond, eval_rhs_value = False)
					if user_var == model_var and user_op == model_op:
						only_partial = 1
						continue
					return 0
			return 2 - only_partial
		
		def compare_refractory(user_using_rp, model_ref):
			"""
			Compare two flags indicating that a hard (Brian-type) refractory period is used.
		
			Parameters
			----------
			user_using_rp : `str`
				Refractory period flag obtained from the code provided by the user in the
				Brian script.
			model_ref : `str`
				Refractory period flag string provided by preset model.
		
			Returns
			-------
			`int`
				Returns ``2`` if the flags match, ``1`` if refractory period is not used but supported
				(unnecessarily), and ``0`` otherwise.
			"""			
			user_ref = "True" if user_using_rp else "False"
			model_ref = model_ref.replace(' ', '')
			if user_ref == "": user_ref = "False" 
			if model_ref == "": model_ref = "False" 
			# Check -- either they match, or the preset model supports a refractory period,
			# but it is not used by the user; or it does not fit
			if user_ref == model_ref:
				return 2
			elif model_ref == "True":
				return 1
			return 0
		
		def compare_learning(user_learning, model_learning):
			"""
			Compare two flags indicating that a hard (Brian-type) refractory period is used.
		
			Parameters
			----------
			user_learning : `bool`
				Flag that specifies whether the user-defined script requires learning mechanisms or not.
			model_learning : `bool`
				Flag that specifies whether the model supports learning mechanisms or not.
		
			Returns
			-------
			`int`
				Returns ``2`` if the flags match, ``1`` if learning is not used but supported (unnecessarily),
				and ``0`` otherwise.
			"""			
			if user_learning == model_learning:
				return 2
			elif model_learning:
				return 1
			return 0
		
		# Compile dictionary of user conditions and obtain refractory period flag
		user_conditions = {
			               "th" : self.brian_object.events.get('spike', "").split("\n"),  #  threshold condition
		                   "rs" : self.brian_object.event_codes.get('spike', "").split("\n")  # reset condition(s)
						  }
		user_using_rp = BrianCondEvaluate.eval_refractory(self.brian_object, self.variables, self.parameters,
												          self.device.logger) > 0
		
		# Check if the equations and conditions provided by the user match any of the preset models 
		# from the model library (and check how well -> 2: perfectly, 1: possibly, 0: not)
		model = None
		comp_cond = 0
		comp_refr = 0
		comp_learning = 0
		for _model in ModelLoader.preset_models:
			if compare_equations(self.brian_object.user_equations, _model.equations):
				_comp_cond = compare_conditions(user_conditions, _model.conditions)
				_comp_refr = compare_refractory(user_using_rp, _model.refractory_period)
				_comp_learning = compare_learning(False, _model.loihi_2_learning_support) # TODO Change `False` to suitable function once
                                                                                          #  learning support is merged.
				# Found a model that is possibly suitable
				if _comp_cond > 0 and _comp_refr > 0:
					# Store properties
					model = _model
					comp_cond = _comp_cond
					comp_refr = _comp_refr
					comp_learning = _comp_learning
					# This model is definitely suitable
					if _comp_cond == 2 and _comp_refr == 2 and _comp_learning == 2:
						# Leave the loop
						break

		# Found a model to use
		if model is not None:
			# Print information
			self.device.logger.info(f"Selected preset model '{model.process_name.lower()}' for '{self.brian_object.name}'.")
			# Throw warnings, if necessary
			if comp_cond == 1:
				warning_message = f"Cannot state with certainty that the selected preset model implements " + \
					f"the right {[key for key in user_conditions.keys()]} conditions (values " +\
					f"provided by you: {[val for val in user_conditions.values()]}). If you want to avoid " + \
					f"this warning, make sure that you use the exact same expressions for " + \
					f"the conditions of your neuron group as those provided with the preset " + \
					f"model (call `{model.process_name.lower()}.conditions` to see them)."
				self.device.logger.warn(warning_message)
			if comp_refr == 1:
				warning_message = f"The selected preset model supports a hard refractory period, but you did " + \
					f"not specify a value for this in your Brian 2 script. If you want to avoid this warning, " + \
					f"specify the refractory period for your neuron group via the 'refractory' argument."
				self.device.logger.warn(warning_message)
			if _comp_learning == 1:
				warning_message = (f"Could only find a model implementation ('{model_with_learning_support.process_name}') that has "
					f"included support for learning on Loihi 2. This implementation will now be used, but note that "
					f"its efficiency might not be optimal.")
				self.device.logger.warn(warning_message)
			# Return the model
			return model
		
		# Error message telling the user that the defined script can not be executed, and letting them know
		# which models are available.
		# TODO Display of `user_equations` should be made better (e.g., "V" -> "volt"; we should see if Brian
		#   offers the possibility).
		usr_eqs_str = "\n".join([str(self.brian_object.user_equations[eq]) for eq in self.brian_object.user_equations])
		usr_cds_str = "\n".join([f"{key} : {val}" for key, val in user_conditions.items()])
		available_desc = ""
		for _model in ModelLoader.preset_models:
			available_desc += f"\n---------------------------------"
			available_desc += f"\n-- {_model.process_name} --"  # name
			available_desc += f"\n{_model.string_equations}"  # equations
			for key, value in _model.conditions.items():
				available_desc += f"\n{key} : {value}"  # conditions
			if _model.refractory_period == "True":  # support for refractory period
				available_desc += '\n<supporting refractory period>'
			else:
				available_desc += '\n<no refractory period>'
		msg = (f"No implementation found that corresponds to the equations and conditions used for '{self.brian_object.name}':\n"
				f"{usr_eqs_str}\n"
				f"{usr_cds_str}\n"
				f"{'<using refractory period>' if user_using_rp else '<no refractory period>'}\n\n"
				f"Please make sure that any object in your simulation uses one of these available models (note that equation-type "
				f"definitions need to match entirely, while simple variable declarations will be ignored):"
				f"{available_desc}")
		raise ValueError(msg)

	def copy_model_files_to_workspace(self):
		"""
		Based on the available Lava processes and process models, get all the files required to run this
		process and copy them into the project folder. These files will be then used to run the simulation.
  
		Returns
		-------
		path : `string`
			Path to the model
		"""
		path =  self.model.path

		# Scrap the model folder for the required files.
		file_contents = ''
		files = scrap_folder(path, endswith = 'process.py', max_files=1, return_full_path=True)
		files.extend(scrap_folder(path, endswith = 'process_model.py', max_files=None, return_full_path=True))
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

		# If there is a plain ucode file we make sure to copy it to the folder. If a template is check if the conditions (such as "th" and "rs") match with preset model as wellalso present, this will be overwritten later on.
		ucode_file = scrap_folder(path,endswith=self.ucode_extensions["file"], max_files=1,empty_ok=True,return_full_path=True)
		if ucode_file:
			with open(ucode_file[0],'r') as ucode_f:
				self.device.writer.write(self.base_name+self.ucode_extensions['file'],ucode_f.read())

		return path

	def copy_lava_proc_files_to_workspace(self):
		"""
		Copy the available (additional) Lava processes and process models into the project folder. 
		These files will be used to run the simulation. 

		NOTE This function is currently only relevant for Loihi 2 hardware.
		"""
		# Only continue if files have not been copied yet
		if PresetProcessHandler.copied_lava_proc_files:
			return
		
		#logger = device.get_logger(__name__)
		lava_proc_dir = self.device.lava_proc_dir
		# Init dictionary of process directories
		proc_dirs = {}

		# Only go on if the user has specified a lava processes directory.
		if lava_proc_dir is not None:
			
			# Get names and dirs
			try:
				usr_proc_names = next(os.walk(lava_proc_dir))[1]
			except StopIteration:
				raise ValueError(f"The path to the folder containing Lava processes is either empty or does not exist: '{lava_proc_dir}'")
			
			proc_dirs = { **{ proc_name : os.path.join(lava_proc_dir, proc_name) for proc_name in usr_proc_names } }
    
		# Iterate over model names, obtained from child folder names
		for proc_name, path in proc_dirs.items():
			self.device.logger.debug(f"Extracting processes from module '{proc_name}' in '{os.path.split(path)[0]}'.")
			#print(f"Extracting processes from module '{proc_name}' in '{os.path.split(path)[0]}'.")
			# Scrap the user-defined Lava processes folder for the required files
			files = scrap_folder(path, endswith = '.py', max_files=None, return_full_path=True)
			# Skip irrelevant folders
			if not len(files):
				continue
			# Loop over files
			for file_in in files:
				self.device.logger.debug(f"Extracting file '{file_in}'.")
				#print(f"Extracting file '{file_in}'.")
				with open(file_in, 'r') as f:
					contained_code = f.read()
				# Write file in subfolder of the project folder
				file_out = os.path.basename(file_in)
				self.device.logger.debug(f"Writing file '{file_out}' in module subfolder '{proc_name}'.")
				#print(f"Writing file '{file_out}' in module subfolder '{proc_name}'.")
				self.device.writer.write(file_out, contained_code, subfolder=proc_name)

		# Set static flag
		PresetProcessHandler.copied_lava_proc_files = True

	def get_namespace_parameters(self):
		"""
		Retrieves the parameters in the namespace of the Brian object.

		Returns
		-------
		`dict`
			A dictionary containing the parameter objects
		"""

		parameters = {}
		for obj in self.brian_object._contained_objects:
			if obj.codeobj is not None:
				parameters.update(obj.codeobj.namespace)

		return parameters


	def get_lava_process_kwargs(self):
		"""
		Initialize keyword arguments for Lava process with user-defined variables and parameters
  
		Returns
		-------
		kwargs : `dict`
			A dictionary of keyword arguments
		
		NOTE The functionality given by this function could easily be extended to already initialize the 
		Processes themselves. The reason why we don't do that here is that we have to keep the Loihi implementation
		compatible with the CPU implementation. This means that the modules are loaded one more time in the ``device.run()``
		and Processes are initialized there.
		"""
		module_name = get_module_name(self.brian_object, self.device, self.base_name)
		try:
			process = getattr(importlib.import_module(module_name), self.class_name)
		except Exception as e:
			if type(e) == AttributeError:
				raise ImportError(
					f"An exception occurred while trying to import '{self.class_name}' from '{module_name}'. " 
					"This could be caused by a mismatch between the class name specified in the '.json' file and the name in the "
					f"Python file defining the Process class.\nThe exception: {e}"
				)
			else:
				
				import warnings
				cwd = os.getcwd()
				warnings.warn(f"module name: {module_name}\n\n"
				              f"current working directory: {cwd}\n"
				              f"contents of lava workspace directory in current working directory:\n"
				              f"  {os.listdir(os.path.join(cwd, 'lava_workspace'))}\n\n"
				              f"project directory: {self.device.project_dir}\n"
				              f"contents of project directory:\n"
				              f"  {os.listdir(self.device.project_dir)}\n")
				
				raise e
		self.device.logger.debug(f"Imported module '{module_name}'.")
		#print(f"Imported module '{module_name}'.")

		# Get specs of init function from Process that contains all available keyword arguments
		specs = inspect.getfullargspec(process.__init__)
		# Extract keyword-only arguments
		arguments = specs.kwonlyargs
		# Remove 'log_config' to avoid raising warnings
		if 'log_config' in arguments:
			arguments.remove('log_config')
		if 'name' in arguments:
			arguments.remove('name')

		# Iterate over available keyword arguments from Lava Process and find
		# a match in the existing user-defined variables or parameters
		kwargs = self.match_arguments(arguments, defaults = specs.kwonlydefaults)

		if PresetProcessHandler.f2f_converter_requested(self.brian_object,self.device):
			if self.model:
				self.device.f2f.add_model(self.model, self.brian_object, kwargs, self.device)
			self.device.f2f.update_parameters(kwargs, owner_name=self.brian_object.name, exceptions=['shape'])

		# Spike generation on Loihi requires a spike adapter to act as intermediary between the generator and the synapses.
		if isinstance(self.brian_object, SpikeGeneratorGroup) and self.device.hardware == HARDWARE.Loihi2:
			kwargs['adapter_class'] = 'PyToNxAdapter'
			kwargs['adapter_module'] = 'lava.proc.embedded_io.spike'

		kwargs['class_name'] = self.class_name

		return kwargs


	def match_arguments(self, arguments, defaults = {}):
		"""
		Searches the Brian 2 namespace for the arguments needed to instantiate the Lava Process,
		and returns a dictionary with the mapping.

		Parameters
		----------
		arguments : `list`
			List of keyword arguments of the Lava process
		defaults : `dict`
			Dictionary of keyword arguments with their default values

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
			adjusted_arg = arg
			# Argument with mantissa/exponent representation
			if arg.endswith("_mant") or arg == 'weights':
				# If necessary, remove the '_mant' part from the variable name;
				# set name of exponent variable
				if arg.endswith("_mant"):
					adjusted_arg = arg[:-5]
					exp_name = adjusted_arg + "_exp"
				else:
					exp_name = "weight_exp"
				# In fixed-point mode, actually compute the representation 
				if self.device.num_repr == "fixed":
					obj_name = self.brian_object.synapses.name if isinstance(self.brian_object,SynapticPathway) else self.brian_object.name
					LavaParameters.add_mantissa_and_exp_param(adjusted_arg, obj_name, mant_name=arg,exp_name=exp_name)
			# Get argument value translated from Brian
			val = self.translate_arg(adjusted_arg)
			# Leave out this argument if its value is `None`
			if val is None:
				if not arg == "num_message_bits":
					self.device.logger.warn(f"Variable or parameter '{adjusted_arg}' was not defined. The default value " +
					                        f"{defaults.get(arg, None)} from Process is used.")
				continue
			# Add argument value to the dictionary (argument depends on whether it's mantissa/exposed-based or not)
			dict_out[arg] = val
			
		return dict_out
	
	
	def translate_arg(self, arg):
		"""
		Interprets an argument for the Lava Process and returns the corresponding
		value taken from the Brian objects (after some preprocessing to translate it
		into a Lava-compatible format).

  		Parameters
		----------
		arg : `string`
			The name of a keyword argument

   		Returns
		-------
		`any`
			The value of the keyword argument, from Brian
		"""
		# Special variables
		if arg == 'shape':
			return (self.variables['N'].get_value(),)
		elif arg == 'weights':
			# Considering the weight of a synaptic pathway
			if isinstance(self.brian_object,(SynapticPathway)):
				pathway = self.brian_object
				i = self.device.get_value(pathway.synapse_sources,access_data = True)
				j = self.device.get_value(pathway.synapse_targets,access_data = True)
				w = self.variables['w'].get_value()
				# Multiply by dt to account for the fact that Lava implements integration without taking
				# timestep size into account.
				# w *= self.device.defaultclock.dt_
				n_rows = pathway.source.N
				n_cols = pathway.target.N
				return sparse_to_dense(i, j, w, n_rows=n_rows, n_cols=n_cols)
			# Support for empty synapses (in that case `brian_object` is a `Synapses` instance)
			else:
				shape = (self.brian_object.target.N, self.brian_object.source.N)
				return np.zeros(shape = shape)
		# SpikeGeneratorGroup
		elif arg == 'data' and isinstance(self.brian_object, SpikeGeneratorGroup):
			neuron_index = self.brian_object.variables["neuron_index"].get_value()
			timebins = self.brian_object.variables["_timebins"].get_value()
			period_bins = self.brian_object.variables["_period_bins"].get_value()
			num_neurons = self.brian_object.N
			N_timesteps = int(self.device.duration / self.device.defaultclock.dt)
			spikes = generate_spikes(neuron_index,timebins,period_bins,num_neurons,N_timesteps)
			return spikes
		# Decay constants: compute from time constant and time step (alternatively, use given value)
		elif arg[:6] == 'delta_':
			tau_name = f'tau_{arg[6:]}'
			self.device.logger.info(f"Encountered variable named '{arg}' in Lava process: Assuming "
			                        f"that this is a decay constant. Now looking in Brian script for "
			                        f"according decay time constant '{tau_name}'.")
			# Search Brian variables
			if self.variables.get(tau_name) is not None:
				dt = self.device.defaultclock.dt_
				# Get the time constant(s)
				# NOTE clipping to `dt` for "delta-function" synapses is not supported here
				timescale = self.variables[tau_name].get_value()
				# Get the decay constant(s)
				decay_constant = dt/timescale
				self.device.logger.debug(f"Decay time constant '{tau_name}' found in Brian variables. "
							             f"Computed decay constant '{arg} = dt/{tau_name} = {decay_constant}'.")
			# Search Brian parameters
			elif self.parameters.get(tau_name) is not None:
				dt = self.device.defaultclock.dt_
				# Get the time constant (clip to `dt` for "delta-function" synapses)
				timescale = max(dt, self.parameters[tau_name])
				# Get the decay constant
				decay_constant = dt/timescale
				self.device.logger.debug(f"Decay time constant '{tau_name}' found in Brian parameters. "
							             f"Computed decay constant '{arg} = dt/{tau_name} = {decay_constant}'.")
			# Now look for plain decay constant in Brian parameters
			else:
				self.device.logger.warn(f"Decay time constant '{tau_name}' not found! Now looking in "
							            f"Brian script for decay constant '{arg}'.")
				if self.parameters.get(arg):
					# Get the decay constant
					decay_constant = self.parameters[arg[:6]]
				else:
					self.device.logger.warn(f"Decay constant '{arg}' not found either! Expect "
							                f"odd behavior...")
					# Set the decay to nan
					decay_constant = np.nan					
			return decay_constant
		# Threshold voltage (is extracted from condition provided with neuron group)
		elif arg == 'vth' or arg == 'v_th':
			_, _, cond_rhs_value =\
				BrianCondEvaluate.eval_threshold(self.brian_object, self.variables, self.parameters, self.device.logger)
			return cond_rhs_value
		# Reset voltage (is extracted from condition provided with neuron group)
		elif arg == 'vrs' or arg == 'v_rs':
			_, cond_rhs_value =\
				BrianCondEvaluate.eval_reset(self.brian_object, self.variables, self.parameters, self.device.logger)
			return cond_rhs_value
		# Refractory period (is extracted from condition provided with neuron group)
		elif arg == 't_rp_steps':
			cond_value =\
				BrianCondEvaluate.eval_refractory(self.brian_object, self.variables, self.parameters, self.device.logger)
			# Calculate number of timesteps for refractory period
			dt = self.device.defaultclock.dt_
			t_rp_steps = int(np.round(cond_value / dt))
			return t_rp_steps
		# Variables that don't need preprocessing
		elif arg in self.variables._variables.keys():
			# Considering dynamic array variable
			if isinstance(self.variables[arg], DynamicArrayVariable):
				return self.variables[arg].get_value(access_data = True)
			# Considering subexpression: value cannot be retrieved
			elif isinstance(self.variables[arg], Subexpression):
				# For the bias variable: look at the expression and possibly perform special treatment
				if arg == 'bias':
					R_name = 'R'
					I_stim__name = 'I_stim_pA'
					I_stim_unit_name = 'pA'
					I_bg_name = 'I_bg_mean'
					special_expr = f'{R_name}*({I_stim__name}(t, i)*{I_stim_unit_name} + {I_bg_name})'
					# Using the special case: retrieve the values of the stimulation current and other parameters and
					# calculate the result
					if self.variables[arg].expr == special_expr:
						dt = self.device.defaultclock.dt
						N_timesteps = int(self.device.duration / dt)
						N_neurons = self.brian_object.N
						self.device.logger.debug(f"Performing special treatment for 'bias' variable "
									             f"(N_neurons = {N_neurons}, N_timesteps = {N_timesteps})")
						try:
							R = self.parameters[R_name]
							I_stim_ = self.parameters[I_stim__name]
							I_bg = self.parameters[I_bg_name]
						except:
							raise ValueError(f"Attempted special treatment for the 'bias' expression '{self.variables[arg].expr}', "
							                 f"but could not evaluate the expression. Probably one of the following "
							                 f"parameters is not defined: '{R_name}', '{I_stim__name}', '{I_bg_name}'.")
						I_stim_unit = float(eval(f"units.{I_stim_unit_name}"))
						# Calculate bias for all timesteps and save it to a file
						bias_for_all_times = np.zeros((N_neurons, N_timesteps))
						for ts in range(N_timesteps):
							# Calculate bias for all neurons at time `t`
							# NOTE Brian defines a Python function for the TimedArray `I_stim_pA`
							t = ts*dt
							for i in range(N_neurons):
								bias_for_all_times[i,ts] = R * (I_stim_(t,i)*I_stim_unit + I_bg)
						np.save(os.path.join(self.device.project_dir, "bias_for_all_times"), bias_for_all_times)
						# Just return the initial value(s) here because Lava can only take arrays of shape `(N_neurons,)`
						return bias_for_all_times[:, 0]
					# Not using the special case: throw a warning
					else:
						self.device.logger.warn(f"Not performing special treatment for the 'bias' expression "
						                        f"'{self.variables[arg].expr}'. However, this could be necessary for "
												f"proper functioning with Brian2Lava. You may want to consider using the "
							                    f"special expression '{special_expr}' instead.")
				# In any other case just return the unevaluated expression
				return self.variables[arg].expr
			return self.variables[arg].get_value()
		# Parameters that don't need preprocessing
		elif arg in self.parameters.keys():
			return self.parameters[arg]
		
		return None


	def generate_ucode(self):
		"""
		Generate the microcode from the Jinja template and write it to a file. Uses
		an instance of the ``MicrocodeGenerator`` class.
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
	and reset conditions as well as refractory period definition of neuron groups.
	"""
	@staticmethod
	def eval_reset(neuron_group, variables, parameters, logger):
		"""
		Evaluates the reset condition of a Brian NeuronGroup.

		Parameters
		----------
		neuron_group : NeuronGroup
			The NeuronGroup object whose reset condition is to be evaluated.
		variables : dict
			Dictionary containing the current Brian variables.
		parameters : dict
			Dictionary containing the current Brian parameters.
		logger : any
			The logger object from Brian.

		Returns
		-------
		cond_variable : `str`
			The variable that the condition relates to.
		cond_rhs_value : `any`
			The value of the right-hand side of the condition after
			its evaluation (``0`` if no valid condition was given).
		"""
		if not 'spike' in neuron_group.event_codes:
			return None, 0
		# Get reset condition and remove whitespaces
		rs_cond = neuron_group.event_codes['spike'].replace(' ', '')

		# Throw a warning and return if the condition is empty
		if rs_cond == '':
			logger.info(f"Empty reset condition '{rs_cond}'.")
			return None, 0

		# Evaluate the condition and throw a warning if there is an unexpected variable or operator
		cond_variable, cond_operator, cond_rhs_value =\
			BrianCondEvaluate.eval_cond(rs_cond, variables, parameters)
		if cond_variable != "v":
			logger.warn(f"Unexpected variable in reset condition '{rs_cond}'. Currently, Brian2Lava's preset mode only supports "
				         "conditions with the 'v' variable.")
		if cond_operator != "=":
			logger.info(f"Unexpected operator in reset condition '{rs_cond}'.")
			
		return cond_variable, cond_rhs_value


	@staticmethod
	def eval_threshold(neuron_group, variables, parameters, logger):
		"""
		Evaluates the threshold condition of a Brian neuron group.

		Parameters
		----------
		neuron_group : `NeuronGroup`
			The NeuronGroup object whose threshold condition is to be evaluated.
		variables : `dict`
			Dictionary containing the current Brian variables.
		parameters : `dict`
			Dictionary containing the current Brian parameters.
		logger : `any`
			The logger object from Brian.

		Returns
		-------
		cond_variable : `str`
			The variable that the condition relates to.
		cond_operator : `str`
			The operator (<= | >= | = | < | >) in the condition.
		cond_rhs_value : `any`
			The value of the right-hand side of the condition after
			its evaluation (``0`` if no valid condition was given).
		"""
		if not 'spike' in neuron_group.events:
			return None, None, 0
		
		# Get threshold condition and remove whitespaces
		th_cond = neuron_group.events['spike'].replace(' ', '')

		# Throw a warning and return if the condition is empty
		if th_cond == '':
			logger.warn(f"Empty threshold condition: '{th_cond}'.")
			return None, None, 0

		# Evaluate the condition and throw a warning if there is an unexpected variable or operator
		cond_variable, cond_operator, cond_rhs_value =\
			BrianCondEvaluate.eval_cond(th_cond, variables, parameters)
		if cond_variable != "v":
			logger.warn(f"Unexpected variable in threshold condition '{th_cond}'. Currently, Brian2Lava's preset mode only supports "
				         "conditions with the 'v' variable.")
		if cond_operator != ">":
			logger.warn(f"Unexpected operator in threshold condition '{th_cond}'. Currently, Brian2Lava's preset mode only supports "
				         "conditions with the '>' operator.")
			
		return cond_variable, cond_operator, cond_rhs_value
	

	@staticmethod
	def eval_refractory(neuron_group, variables, parameters, logger):
		"""
		Evaluates the refractory condition of a Brian NeuronGroup.

		Parameters
		----------
		neuron_group : NeuronGroup
			The NeuronGroup object whose refractory condition is to be evaluated.
		variables : dict
			Dictionary containing the current Brian variables.
		parameters : dict
			Dictionary containing the current Brian parameters.

		Returns
		-------
		cond_value : `any`
			The value of the of the condition after its evaluation (``0`` if no valid condition was given).
		"""
		# Check if refractory attribute is there
		if not hasattr(neuron_group, '_refractory'):
			return None
		# Get refractory condition 
		refractory = neuron_group._refractory

		# If a `Quantity` object is given, convert it to a string
		if isinstance(refractory, Quantity):
			refractory = refractory.in_unit(second, python_code=True)

		# Check if valid refractory condition is given
		if refractory:
			# Remove whitespaces
			ref_cond = refractory.replace(' ', '')
		else:
			# Set to empty (for instance, might have been `False`` before)
			ref_cond = ''

		# Throw a warning and return if the condition is empty
		if ref_cond == '':
			logger.debug(f"Empty refractory condition: '{ref_cond}'.")
			return 0

		# Evaluate the condition and throw a warning if there is an unexpected variable or operator
		cond_variable, cond_operator, cond_value =\
			BrianCondEvaluate.eval_cond(ref_cond, variables, parameters)
			
		return cond_value
	
	@staticmethod
	def eval_cond(cond, variables = {}, parameters = {}, eval_rhs_value = True):
		"""
		Evaluates a Brian condition.

		Parameters
		----------
		cond : `str`
		    The condition expression to be evaluated.
		variables : `dict`, optional
			Dictionary containing the current Brian variables.
		parameters : `dict`, optional
			Dictionary containing the current Brian parameters.
		eval_rhs_value : `bool`, optional
			Specifies whether the function should evaluate the value of the right-hand-side
			or not (depends on whether it is used for the actual conditions or just to compare
			conditions).

		Returns
		-------
		cond_variable : `str`
			The variable that the condition relates to.
		cond_operator : `str`
			The operator (<= | >= | = | < | >) in the condition.
		cond_rhs_value : `any`
			The value of the right-hand side of the condition after
			its evaluation.
		"""
		# If possible, split statement, get variable and right-hand side of the condition
		cond_operator_find = re.search("(?:<=|>=|=|<|>)", cond)
		if cond_operator_find is not None:
			cond_operator = cond_operator_find.group(0)
			cond_split = cond.split(cond_operator)
			cond_variable = cond_split[0]
			cond_rhs = cond_split[1]
		# Otherwise, take the whole statement
		else:
			cond_operator = ""
			cond_variable = ""
			cond_rhs = cond

		# Already return if the value of the right-hand side should not be evaluated
		if not eval_rhs_value:
			return cond_variable, cond_operator, cond_rhs

		# Replace parameters in right-hand side with values
		# TODO This is a bit dangerous if there are overlapping names.
		# 	We should use brian's parsing tools to make it a bit more solid.
		for k, v in parameters.items():
			cond_rhs = cond_rhs.replace(k, str(v))

		# Raise an error if variables are used in the right-hand side
		for k, v in variables.items():
			if cond_rhs.find(k) != -1:
				raise Exception(f"Error in condition '{cond}': currently, "
					            f"only parameters may be used, not variables "
								f"(encountered variable '{cond_rhs}').")

		# Evaluate reset condition and obtain scaled threshold value
		exec_vars = {}
		exec(f'cond_rhs_value = {cond_rhs}', globals(), exec_vars)
		cond_rhs_value = exec_vars['cond_rhs_value']

		return cond_variable, cond_operator, cond_rhs_value

class MicrocodeGenerator():
	"""
	A generator to fill in the gaps in the microcode templates. Allows for the definition of custom quantities such as thresholds, reset conditions, etc.
	By default, it will treat each of the keyword arguments given during the initialization of a brian object, managing each separately.

	NOTE The approach is not finally implemented yet, since microcode usability is currently still largely restricted.
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
		Method that renders the microcode (ucode), using the template and parameter mappings.

		Returns
		-------
		`str`
			The rendered microcode.
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
		and generate a dictionary of keywords which will be used by Jinja to generate the file 
		from the template.

		Returns
		-------
		`dict`
			Dictionary of keywords for Jinja.
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
		Method getting attributes related to the reset condition of a ``NeuronGroup``.

		Returns
		-------
		`dict`
			Dictionary containing items for reset variable and value.
		"""
		loihi_reset_variable, loihi_reset_value = \
			BrianCondEvaluate.eval_reset(self.brian_object, self.variables, self.parameters,
								         self.device.logger)

		# Do float-to-fixed conversion if it is requested
		if self.device.is_using_f2f():
			loihi_reset_value = self.device.f2f.float_to_fixed(loihi_reset_value)

		return {'rs_var': loihi_reset_variable, 'rs_val': loihi_reset_value}


	def eval_threshold(self):
		"""
		Method getting attributes related to the threshold condition of a ``NeuronGroup``.

		Returns
		-------
		`dict`
			Dictionary containing items for threshold variable and value.
		"""
		loihi_threshold_variable, _, loihi_threshold_value = \
			BrianCondEvaluate.eval_threshold(self.brian_object, self.variables, self.parameters,
									         self.device.logger)

		# Do float-to-fixed conversion if it is requested
		if self.device.is_using_f2f():
			loihi_threshold_value = self.device.f2f.float_to_fixed(loihi_threshold_value)

		return {'th_var': loihi_threshold_variable, 'th_val': loihi_threshold_value}