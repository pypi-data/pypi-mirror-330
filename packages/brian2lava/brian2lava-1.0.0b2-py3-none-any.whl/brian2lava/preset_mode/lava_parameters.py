import numpy as np
from brian2 import get_device
from brian2.synapses.synapses import SynapticPathway, Synapses
from brian2lava.utils.math import check_convert_to_int32
from brian2lava.utils.const import LOIHI2_SPECS, EPSILON
from brian2 import get_logger


class LavaParameters:
	"""
	This class holds essential, static methods for preset mode, serving to manage special parameters that
	have particular representations in Lava. The class makes it easy to access the methods throughout
	the code without cluttering it too much.
	"""
	mantissa_exp_vars = {}
	msb_aligned_vars = {}
	logger = get_logger('brian2lava.preset_mode.lava_parameters')

	@ staticmethod
	def reset():
		"""
		Resets the ``mantissa_exp_vars`` and ``msb_aligned_vars`` fields.
		"""
		LavaParameters.mantissa_exp_vars = {}
		LavaParameters.msb_aligned_vars = {}

	def track_msb_aligned_vars(process):
		"""
		Tracks the variables that have to be MSB-aligned.

		TODO It would make sense to just have one dictionary in 'model.json' with this structure (which would 
		make the code here and in other places much cleaner):
		``MSB_aligned_vars = {
		var_name_0 : shift_amount,
		var_name_1 : ...,
		...
		}``
		"""

		if isinstance(process.brian_object,SynapticPathway):
			obj_name = process.brian_object.synapses.name
		else:
			obj_name = process.brian_object.name

		if obj_name in LavaParameters.msb_aligned_vars:
			raise ValueError(f"Process {obj_name} msb aligned vars are already being tracked.")
		
		# This should only happen for synapses objects
		if not process.model:
			LavaParameters.msb_aligned_vars[obj_name] = {
				'msb_align_act' : [],
				'msb_align_decay': [],
				'msb_align_prob' : []
			}
			return
		
		LavaParameters.msb_aligned_vars[obj_name] = {
			'msb_align_act' : process.model.msb_align_act,
			'msb_align_decay': process.model.msb_align_decay,
			'msb_align_prob' : process.model.msb_align_prob
		}
	
	def revert_msb_alignment(value,var_name,obj_name):
		"""
		Reverts the MSB alignment when retrieving values from Lava.
		"""
		obj_alignments = LavaParameters.msb_aligned_vars[obj_name]
		
		bit_shift = 0
		if var_name in obj_alignments['msb_align_act']:
			bit_shift = LOIHI2_SPECS.MSB_Alignment_Act
			
		if var_name in obj_alignments['msb_align_decay']:
			bit_shift = LOIHI2_SPECS.MSB_Alignment_Decay
			
		if var_name in obj_alignments['msb_align_prob']:
			bit_shift = LOIHI2_SPECS.MSB_Alignment_Prob
			
		return value * 2**-bit_shift

	
	def parameters_to_lava_format(params, preset_process):
		"""
		Conversion method that targets two types of variables (which don't necessarily exclude each other):
		
		1. Variables that have to be MSB-aligned (for Loihi, eventually): we shift them by the number of bits 
		corresponding to their function in Lava, which is specified by the ``msb_align_*`` lists.
		
		2. Variables that are required to have mantissa/exponent representation: we take their values as input
		and return mantissa and exponent.

		Is only used with fixed-point number representation.

		Parameters
		----------
		params : `defaultdict`
			Dictionary of process keyword arguments
		preset_process : `PresetProcessHandler`
			The object to create the preset process (represented as an instance of ``PresetProcessHandler``).

		Returns
		-------
		params_out : `defaultdict`
			Updated dictionary of process keyword arguments
		"""

		LavaParameters.track_msb_aligned_vars(preset_process)
		# TODO Find a cleaner approach
		if not isinstance(preset_process.brian_object, SynapticPathway):
			obj_name = preset_process.brian_object.name 
		else:
			obj_name = preset_process.brian_object.synapses.name
		
		msb_align_act = LavaParameters.msb_aligned_vars[obj_name]['msb_align_act']
		msb_align_decay = LavaParameters.msb_aligned_vars[obj_name]['msb_align_decay']
		msb_align_prob = LavaParameters.msb_aligned_vars[obj_name]['msb_align_prob']
		params_out = params.copy()
		device = get_device()
		for var_name, value in params.items():
			# Some checks to make sure only the right parameters are considered
			if not isinstance(value,(list,np.ndarray,int,float, np.int32,np.float64)):
				continue
			if isinstance(value,list) and len(value):
				# Only check first element: assume that lists only have consistent data types in them
				if isinstance(value[0],str):
					continue
			updated_value = value

			# Left-shifts for activation-related variables/parameters
			if var_name in msb_align_act:
				# Get number of bits for shift
				bit_shift = LOIHI2_SPECS.MSB_Alignment_Act
				device.logger.debug(f"Variable '{var_name}' will be aligned by factor 2^{bit_shift} (left-shifted).")
				# We do the shift that Lava/Loihi needs (no check for "silenced elements" necessary
				# since we do left shifting).
				shifted_value = check_convert_to_int32(value * 2**bit_shift, var_name)
				# Assign new value
				updated_value = shifted_value

			# Left-shifts for decay-related variables/parameters
			if var_name in msb_align_decay:
				# Get number of bits for shift
				bit_shift = LOIHI2_SPECS.MSB_Alignment_Decay
				device.logger.debug(f"Variable '{var_name}' will be aligned by factor 2^{bit_shift} (left-shifted).")
				# Compile specific information for decay constants (which are computed from time constant and timestep)
				if var_name[:6] == 'delta_':
					tau_name = f'tau_{var_name[6:]}'
					var_info = f"{var_name} = dt/{tau_name}*2^{LOIHI2_SPECS.MSB_Alignment_Decay}"
				else:
					tau_name = ""
					var_info = var_name
				# We do the shift that Lava/Loihi needs (no check for "silenced elements" necessary
				# since we do left shifting).
				shifted_value = check_convert_to_int32(value * 2**bit_shift, var_info)
				# Check for correct range of decay constants (and possibly clip to ensure that the maximum
				# bit width is not exceeded)
				if var_name[:6] == 'delta_':
					if np.any(shifted_value > LOIHI2_SPECS.Max_Deltas):
						device.logger.warn(f"The timescale given by '{tau_name}' is too large ({var_info} = {np.max(shifted_value)}). "
						                   f"Clipping '{var_info}' to the maximum ({LOIHI2_SPECS.Max_Deltas}).")
						shifted_value = LOIHI2_SPECS.Max_Deltas
				# Assign new value
				updated_value = shifted_value
					
			# Left-shifts for probability variables/parameters
			if var_name in msb_align_prob:
				# Get number of bits for shift
				bit_shift = LOIHI2_SPECS.MSB_Alignment_Prob
				device.logger.debug(f"Variable '{var_name}' will be aligned by factor 2^{bit_shift} (left-shifted).")
				# We do the shift that Lava/Loihi needs (no check for "silenced elements" necessary
				# since we do left shifting).
				shifted_value = check_convert_to_int32(value * 2**bit_shift, var_name)
				# Check for correct range of probability variables/parameters (and possibly clip to ensure that the maximum
				# bit width is not exceeded)
				if np.any(shifted_value > LOIHI2_SPECS.Max_Random):
					device.logger.warn(f"The probability array '{var_name} = {shifted_value}' has values that are too "
					                   f"large. Clipping them to the maximum ({LOIHI2_SPECS.Max_Random}).")
					shifted_value = np.clip(shifted_value, a_min=None, a_max=LOIHI2_SPECS.Max_Random, dtype=np.int32)
				# Assign new value
				updated_value = shifted_value

			# Extraction of mantissa and exponent for eligible variables/parameters
			if obj_name in LavaParameters.mantissa_exp_vars and \
			   var_name in LavaParameters.mantissa_exp_vars[obj_name]:
				device.logger.debug(f"Variable '{var_name}' (abs. value in [{np.min(np.abs(updated_value)):e}:" +
						            f"{np.max(np.abs(updated_value)):e}]) will be represented by mantissa and exponent.")
				obj_mantissa_exp = LavaParameters.mantissa_exp_vars[obj_name]
				mant_name = obj_mantissa_exp[var_name]['mant']
				exp_name = obj_mantissa_exp[var_name]['exp']
				params_out[mant_name], params_out[exp_name] \
				  = LavaParameters.param_to_mantissa_exponent(updated_value, var_name=var_name, obj_name=obj_name)
			else:
				# Assign after doing integer check (even if it has been done before)
				params_out[var_name] = check_convert_to_int32(updated_value, var_name)

		return params_out
	
	@staticmethod
	def add_mantissa_and_exp_param(param: str, owner_name : str, mant_name : str = None, exp_name : str = None):
		"""
		Add a parameter to the list of parameters that require a mantissa-and-exponent representation.
		This will be used later to distinguish them from common parameters, as the conversion process is 
		different.

		Parameters
		----------
		param : `str`
			Name of the parameter to be added.
		owner_name : `str`
			Name of the owner object.
		mant_name : `str`, optional
			Name of the mantissa part.
		exp_name : `str`, optional
			Name of the exponent part.
		"""
		if not isinstance(param,str):
			raise ValueError(f"Parameter name should be given as a string, not {type(param)}")
		
		mant_name = mant_name if mant_name else param + '_mant'
		exp_name = exp_name if exp_name else param + '_exp'
		
		# Create the dict the first time a var is added for this object
		if not owner_name in LavaParameters.mantissa_exp_vars:
			LavaParameters.mantissa_exp_vars[owner_name] = {}
		# Potentially, the user might have already defined this parameter manually as requiring 
		# mantissa-and-exponent representation
		if not param in LavaParameters.mantissa_exp_vars[owner_name]:
			LavaParameters.mantissa_exp_vars[owner_name][param] = {'mant' : mant_name, 'exp' : exp_name, 'exp_val': 0}
		
	@staticmethod
	def param_to_mantissa_exponent(val, var_name : str, obj_name : str):
		"""
		Convert a parameter value to mantissa-and-exponent representation.

		This method can also be called by the user, but then an argument should be given to store the exponent
		for the inverse transformation in the ``mantissa_exp_vars`` attribute.

		Note that the method is also able to handle arrays of exponents (one individual exponent for each value).
		However, this requires the use of customized Lava processes (see the documentation on ``use_exp_array``).

		TODO The current method is only optimal for static parameters. More consideration will
		be needed for dynamic variables and their growth, which with the current method could
		easily result in overflows.

		Parameters
		----------
		val : `any`
			Any type of numeric value(s) (may also be a list or an array).
		var_name : `str`
			Name of the variable.
		obj_name : `str`
			Name of the owner object of the variable.
		
		Returns
		-------
		mantissa : `any`
			Mantissa(s) of the given value(s). May also be a list or an array.
		exponent : `any`
			Exponent(s) of the given value(s). May also be a list or an array.
		"""
		device = get_device()
		logger = device.logger

		if np.all(val == 0):
			mant = np.zeros(np.shape(val)) if isinstance(val,(list,np.ndarray)) else 0
			# Needed for inverse mant-exp to param method
			LavaParameters.mantissa_exp_vars[obj_name][var_name]['exp_val'] = 0
			return mant, 0

		# Find out if the weights are larger than the 8 bit maximum allowed and by how many bits
		max_val = LOIHI2_SPECS.Max_Mantissa_Weights if var_name == 'weights' else LOIHI2_SPECS.Max_Mantissa_Others
		with np.errstate(divide='ignore'):
			# For each weight value individually, if using an array of exponents
			if device.use_exp_array:
				max_bit_to_weight_ratio = np.nan_to_num(np.log2(max_val/np.abs(val)), posinf=0)
			# For all weight values at once, if using a single exponent
			else:
				max_bit_to_weight_ratio = np.nan_to_num(np.log2(max_val/np.max(np.abs(val))), posinf=0)
		logger.diagnostic(f"max_bit_to_weight_ratio({var_name}) = {max_bit_to_weight_ratio}")

		# Shift the weights by the necessary number of bits (only if the previous calculation returned a negative value)
		# For each weight value individually, if using an array of exponents
		if device.use_exp_array:
			mantissa_shift = np.int32(np.floor(max_bit_to_weight_ratio * (max_bit_to_weight_ratio < 0)))
			mantissa = check_convert_to_int32(val * np.power(2*np.ones_like(val), mantissa_shift), var_name + "_mant")
		# For all weight values at once, if using a single exponent
		else:
			mantissa_shift = np.floor(np.min(max_bit_to_weight_ratio, 0))
			mantissa = check_convert_to_int32(val * np.power(2, mantissa_shift), var_name + "_mant")
		logger.diagnostic(f"mantissa({var_name}) = {mantissa}")

		# Determine the exponent (only > 0 if we had to downscale our weights, i.e., mantissa_shift < 0)
		# For each weight value individually, if using an array of exponents
		if device.use_exp_array:
			exponent = check_convert_to_int32(-mantissa_shift * (mantissa_shift < 0), var_name + "_exp")
		# For all weight values at once, if using a single exponent
		else:
			exponent = check_convert_to_int32(np.max(-mantissa_shift, 0), var_name + "_exp")
		logger.diagnostic(f"exponent({var_name}) = {exponent}")

		# If this parameter was not yet in the list, we add it to the parameters that require this representation.
		# Only needed when this function is called by the user. 
		if not obj_name in LavaParameters.mantissa_exp_vars or not var_name in LavaParameters.mantissa_exp_vars[obj_name]:
			LavaParameters.add_mantissa_and_exp_param(var_name,obj_name)
		LavaParameters.mantissa_exp_vars[obj_name][var_name]['exp_val'] = exponent

		return mantissa, exponent
	
	@staticmethod
	def mantissa_exponent_to_param(val, var_name: str, obj_name: str):
		"""
		Converting these types of parameters/variables requires first a shift by the exponent
		to get back to their true value(s).

		Note that the method is also able to handle arrays of exponents (one individual exponent for each value).
		However, this requires the use of customized Lava processes (see th documentation on ``use_exp_array``).

		Parameters
		----------
		val : `any`
			Any type of numeric value(s) (may also be a list or an array).
		var_name : `str`
			Name of the variable.
		obj_name : `str`
			Name of the owner object of the variable.
		
		Returns
		-------
		resulting_val : `any`
			Value(s) resulting from re-combining mantissa and exponent. May also be a list or an array.
		"""
		device = get_device()
		logger = device.logger

		if not var_name in LavaParameters.mantissa_exp_vars[obj_name]:
			raise ValueError(f"The parameter '{var_name}' you are trying to convert is not listed as one of the "
					"parameters that require mantissa-and-exponent representation. Use simple 'fixed_to_float' "
					"instead.")
		exponent = LavaParameters.mantissa_exp_vars[obj_name][var_name]['exp_val']
		#logger.diagnostic(f"val({var_name}) = {val}, exponent({var_name}) = {exponent}")

		# For each weight value individually, if using an array of exponents
		if device.use_exp_array:
			resulting_val = val * np.power(2*np.ones_like(val), exponent)
		# For all weight values at once, if using a single exponent
		else:
			resulting_val = val * np.power(2., exponent)

		return resulting_val
	