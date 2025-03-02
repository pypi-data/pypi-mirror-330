from brian2lava.utils.utils import find_func_args_in_dict
from brian2lava.utils.files import scrap_folder
from importlib.machinery import SourceFileLoader
import numpy as np
from brian2 import get_device
from brian2lava.utils.const import LOIHI2_SPECS, EPSILON
import typing as ty


class F2F:
	"""
	Static class that can handle conversions between floating-point and fixed-point numbers (which are needed,
	e.g., on Loihi 2).
	If parameters are already given in fixed-point representation (i.e., as ``int``),
	then the functions in this class will simply act as the identity operator.
	
	NOTE This is still in a testing stage.
	"""
	# Set manually through the setter method
	additional_accuracy = 0

	def __init__(self):
		self.logger = get_device().logger

		# Set internally
		self._binary_shift = None

		

		# Updated by the device
		self.parameters = {}
	
	def add_model(self,model,brian_object,parameters,device):
		"""
		This method is not needed for the generic F2F converter since 
		the conversion is done regardless of model specificity
		"""
		pass

	
	def update_parameters(self,parameters : dict, owner_name : str, exceptions : ty.List[str] = []):
		"""
		Use this function to add all the simulation parameters into the converter.
		After having added all the necessary parameters, we will perform the conversion 
		at a later stage.
		"""
		for varname,val in parameters.items():
			# Some checks to make sure only numbers are considered
			is_exception = False
			for ex in exceptions:
				# Allow generic exceptions like 'delta_' to select any parameter starting with that string
				if varname.startswith(ex):
					is_exception = True
					break
			if is_exception: continue
					
			if not isinstance(val,(list,np.ndarray,int,float)):
				continue
			if isinstance(val,list) and len(val):
				# Assume that lists only have consistent data types in them
				if isinstance(val[0],str):
					continue
			if not owner_name in self.parameters:
				self.parameters[owner_name] = {}

			self.parameters[owner_name][varname] = val
	
	@staticmethod
	def set_binary_accuracy(val : int):
		"""
		Sets the additional term which will be counted when converting to fixed point
		representation (e.g. new_val = old_val * 2 ** (exponent + add_accuracy)).
		"""
		if not type(val) == int:
			raise TypeError(
				"Binary accuracy can only be set with 'int'" 
				"(binary places to round to in case it's necessary)."
				f" The given type was instead {type(val)}"
				)
		F2F.additional_accuracy = val

	@staticmethod
	def set_decimal_accuracy(val : int):
		"""
		Sets the additional term which will be counted when converting to fixed point
		representation (e.g. new_val = old_val * 2 ** (exponent + add_accuracy)).
		The user-given value is in decimal places, so we first find its equivalent
		in binary representation. This will inevitably lead to approximation error,
		but I believe it's more intuitive in terms of UX.
		"""
		if not type(val) == int:
			raise TypeError(
				"Decimal accuracy can only be set with 'int'" 
				"(decimal places to round to in case it's necessary)."
				f" The given type was instead {type(val)}"
				)
		binary_exponent = int(np.log2(10**val))
		F2F.additional_accuracy = binary_exponent

	def find_scaling_params(self):
		"""
		Previous mechanism to determine the range of values of our parameters
		"""
		pass
		"""
		min_value = np.inf
		max_value = -np.inf
		# Only for debugging
		var_max = None
		var_min = None
		add_accuracy = F2F.additional_accuracy
		# First find the min and the max in our parameters
		for obj_params in self.parameters.values():
			for varname,var in obj_params.items():
				# We only care about nonzero values of arrays (empty arrays are handled in the try-except)
				if hasattr(var,"shape") and var.shape:
					var = var[np.nonzero(var)]
				# Catch errors if var is empty array (we just skip it then)
				try:
					var_min = np.min(np.abs(var))
					var_max = np.max(np.abs(var))
					# Variables undergoing MSB alignment in Lava will be shifted by the opposite number of bits,
					# so for F2F conversion, they are considered as smaller.
					# TODO I guess the following has to be fixed, there is no `LOIHI2_SPECS.MSB_Alignments`!
					if varname in LOIHI2_SPECS.MSB_Alignments:
						amount = LOIHI2_SPECS.MSB_Alignments[varname]
						var_min = var_min * 2 ** - amount
						var_max = var_max * 2 ** - amount
				except Exception as e:
					continue
				if var_min < min_value and var_min != 0:
					min_value = var_min
					varname_min = varname
				if var_max > max_value and var_max != 0:
					max_value = var_max
					varname_max = varname
		
		# Check that loihi can handle the max value
		tmp =  max_value*2**add_accuracy
		max_val = LOIHI2_SPECS.Max_Variables if varname_max != 'w' else LOIHI2_SPECS.Max_Weights
		too_large =  tmp > max_val
		if too_large:
			raise ValueError(f"Parameter value exceeds Loihi2 range of values: {var_max} * accuracy(2^{add_accuracy})>{max_val}")

		# Set the decimal shift accounting for the smallest value
		self._binary_shift = max(-int(np.floor(np.log2(abs(min_value)))), 0) + add_accuracy

		self.logger.debug(f"Found binary shift for F2F converter: {self._binary_shift}, min {varname_min}={min_value}, max {varname_max}={max_value}")

		# Make sure loihi can handle the range of scales of the parameters
		param_range = max_value/min_value
		if param_range*2** add_accuracy > LOIHI2_SPECS.Max_Variables:
			raise ValueError("The range of your parameters exceeds the maximum range of values supported by Loihi2. "\
					f"Please make sure that the range does not exceed {LOIHI2_SPECS.Max_Variables}. Currently:"\
					f" {var_max}/{var_min} * accuracy(2^{add_accuracy}) = {param_range * 2**add_accuracy}.")
		"""
	
	
	def float_to_fixed(self, value, varname = None, obj_name = None):
		"""
		Convert floating-point representation to a consistent fixed-point number which accounts
		for the whole range of parameters and the intended accuracy.

		NOTE The redundant arguments are being used by the ``ModelWiseF2F`` class which for now inherits from ``F2F``
		in order to keep the pipeline unchanged. 

		Parameters
		----------
		value : `float`
			Floating-point value to be converted to fixed-point representation
		
		Returns
		-------
		`int`
			Converted fixed-point representation of the input value
		"""
		binary_shift = self._binary_shift
		# Decimal shift accounting for parameter values is computed in determine_shift_factor()
		shift_factor = 2 ** binary_shift
		shifted_val = value * shift_factor
		# Use numpy functions to allow conversion of arrays and matrices
		fixed_val = np.int32(np.round(shifted_val))
		
		return fixed_val
	
	def fixed_to_float(self, value):
		"""
		Convert fixed-point back to floating-point representation in a way compatible with the previous transformation.

		Parameters
		----------
		value : `float`
			Fixed-point value to be converted to floating-point representation
		
		Returns
		-------
		`int`
			Converted floating-point representation of the input value
		"""

		shift_factor = 2**(-self._binary_shift)
		
		return value*shift_factor
	
	
	def params_float_to_fixed(self, params : dict, obj_name : str, exceptions: ty.List[str] = []):
		"""
		Converts all the internal parameters to fixed point. Note that we don't need a reverse of this operation
		because parameter values will have changed after running the simulation, so we will need to retrieve them
		directly from the Lava Process one by one.

		Parameters
		----------
		params : `dict`
				A dictionary of the parameters to be converted from floating-point to fixed-point representation.
		exceptions : `list(str)`
				A list containing names of some parameters which should not be converted (for example array shape or indices).
		"""
		# To avoid 'dictionary changed size during iteration' error, needed since
		# we still want the dict to contain the variables that we're not converting.
		params_out = params.copy()
		for varname, value in params.items():
			# Some checks to make sure only the right parameters are considered
			if varname in exceptions:
				continue
			if not isinstance(value,(list,np.ndarray,int,float)):
				continue
			if isinstance(value,list) and len(value):
				# Only check first element: assume that lists only have consistent data types in them
				if isinstance(value[0],str):
					continue
			params_out[varname] = self.float_to_fixed(value,varname=varname,obj_name=obj_name)
		return params_out
	
		
	def reset(self):
		self.parameters = {}

import os
from brian2lava.preset_mode.abstract_model import Model
class ModelWiseF2F(F2F):
	"""
	Class inheriting from ``F2F`` to enable F2F conversion in a model-aware manner.

	NOTE This is still in a testing stage.
	"""

	def __init__(self):
		super().__init__()
		self.scalers = {}
		self.processes_data = {}

	
	def _find_scaler(self,neuron_model: ty.List[Model]):

		# No need to add the scaler twice
		if neuron_model.name in self.scalers:
			return
		
		f2f_path = scrap_folder(neuron_model.path,endswith='f2f.py',max_files=1,empty_ok=True,return_full_path=True)[0]

		if not f2f_path:
			raise FileNotFoundError(f"F2F scaler for model {neuron_model.name} was not found." 
						   "F2F conversion is not supported for this model")
		
		f2f_module_name = os.path.splitext(os.path.basename(f2f_path))[0]
		scaler = SourceFileLoader(f2f_module_name,f2f_path).load_module().ModelScaler
		self.scalers[neuron_model.name] = scaler
		# Read the MSB variables from the neuron model (which have been read from 'model.json')
		scaler.msb_align_act = neuron_model.msb_align_act
		scaler.msb_align_decay = neuron_model.msb_align_decay
		scaler.msb_align_prob = neuron_model.msb_align_prob
		# Don't count weights in constants, if they are present in the model parameters
		scaler.const = neuron_model.parameters - set(['w','weights'])

	
	def add_model(self, model, brian_object, parameters, device):
		"""
		Considers a new model for the F2F conversion mechanism. Uses values from pre-processed list of
		Lava parameters/variables.

		Params
		------
		model: dict
				A dictionary of the parameters to be converted from floating point to fixed point representation
		brian_object: `BrianObject`
			Brian object related to the model
		parameters : `dict` of `any`
			Dictionary of Lava parameters/variables and their values
		device : `Device`
			The current Brian device.
		"""
		self._find_scaler(model)

		if not brian_object.name in self.processes_data:
			
			self.processes_data[brian_object.name] = {
				"model": model.name,
				"synapses": [],
				"scalings" : {},
				"vars_minmax": {}
				}

		# Only the variables that actually need scaling
		for var_name in self.scalers[model.name].forward_ops:
			# Weights are taken care of later
			if var_name == 'w':
				continue
			if var_name == 'dt': # TODO remove?
				value = device.defaultclock.dt_
			else:
				value = parameters[var_name]
			self._add_minmax_var(value, var_name, brian_object.name)

		# We also add the weights of synapses targetting this neurongroup
		for port in device.lava_ports.values():
			pathway = port['pathway']

			if pathway.target != brian_object:
				continue

			# The only vars needed from synapses are the weights
			self._add_minmax_var(pathway.synapses.variables['w'].get_value(), 'w', brian_object.name)
			self.logger.debug(f"Found synapses {pathway.name} connected to {brian_object.name} that need f2f conversion.")
			# Add the synapses names to the object data, used when finding the scaling params 
			self.processes_data[brian_object.name]['synapses'].append(pathway.synapses.name)

	
	def _add_minmax_var(self,value,varname,obj_name):

		if varname in self.processes_data[obj_name]:
			raise KeyError(f"Variable {varname} is already in dict.")
		
		# Make every value into an iterable for conveniency
		if not isinstance(value,(list,np.ndarray)):
			value = [value]
		value = np.abs(value)
		# Exclude zeros
		self.logger.diagnostic(f"Value to minmax for ModelWiseF2F: {obj_name}.{varname}: {value}")
		value = value[np.nonzero(value)]
		if len(value):
			var_min = np.min(value)
			var_max = np.max(value)
		else:
			# Zeros will be ignored later
			var_min = var_max = 0
		self.processes_data[obj_name]["vars_minmax"][varname] = (var_min,var_max)

		if not self.processes_data[obj_name].get(varname,None):
			self.logger.debug(f"Adding variable {varname} to F2F model {obj_name} minmax")
		

	
	def find_scaling_params(self):
		synapses_dict = {}

		for obj_name,data_dict in self.processes_data.items():
			scaler = self.scalers[data_dict['model']]
			vars = data_dict['vars_minmax']
			scaling_params = scaler.optimal_scaling_params(vars)
			data_dict['scalings'] = scaling_params
			self.logger.debug(f"Found scaling parameters for {obj_name}: {scaling_params}")

			# Create an entry for synapses too, this allows smoother conversion later
			if 'synapses' in data_dict:
				for synapses_name in data_dict['synapses']:
					synapses_dict[synapses_name] = {
						'model': self.processes_data[obj_name]['model'],
						'scalings': scaling_params
					}

		self.processes_data.update(synapses_dict)

	
	def _forward_scaling(self,value,varname,obj_name):
		"""
		Performs the forward scaling (required for brian2 -> lava conversion) of parameters
		depending on the operations required by the current model. These operations
		are defined in the model library in the f2f files for each model.
		"""
		process_data = self.processes_data[obj_name]
		scaler = self.scalers[process_data['model']]
		kwargs = process_data['scalings']
		if '_mant' in varname:
			varname = varname[:-5]
		
		value = value * scaler.forward_ops[varname](**kwargs)
		
		return value

	
	def _inverse_scaling(self,value,varname,obj_name):
		"""
		Inverse conversion (required for brian2 <- lava conversion). See self.forward_scaling.
		"""
		# TODO a bit annoying that we have to keep accounting for this.
		if varname == 'weights':
			varname == 'w'
		process_data = self.processes_data[obj_name]
		scaler = self.scalers[process_data['model']]
		kwargs = process_data['scalings']
		value = value * scaler.forward_ops[varname](**kwargs)**-1
		
		return value
	
	
	def float_to_fixed(self,value, varname, obj_name):
		"""
		Convert floating-point representation to a consistent fixed-point number which accounts
		for the whole range of parameters and the intended accuracy.

		Parameters
		----------
		value : `float`
			Floating-point value to be converted to fixed-point representation
		
		Returns
		-------
		`int`
			Converted fixed-point representation of the input value
		"""
		# TODO: We unfortunately still have to account for this naming inconsistency
		if varname == 'weights':
			varname = 'w'
		# Use numpy functions to allow conversion of arrays and matrices
		scaled_val = self._forward_scaling(value,varname,obj_name)
		fixed_val = np.int32(scaled_val)
		
		return fixed_val
	
	
	def fixed_to_float(self,value,varname,obj_name):
		"""
		Convert fixed-point back to floating-point representation in a way compatible with the previous transformation.

		Parameters
		----------
		value : `float`
			Fixed-point value to be converted to floating-point representation
		
		Returns
		-------
		`int`
			Converted floating-point representation of the input value
		"""
		return self._inverse_scaling(value,varname,obj_name)
	
	def reset(self):
		"""
		Reset needed when running multiple simulations with ``device.reinit()``
		"""
		self.logger.debug("Emptying parameters stored in F2F converter.")
		super().reset()
		self.scalers = {}
		self.processes_data = {}
