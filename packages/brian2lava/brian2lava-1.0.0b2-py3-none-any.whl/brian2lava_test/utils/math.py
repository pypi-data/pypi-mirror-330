import numpy as np
from brian2lava_test.utils.const import LOIHI2_MAX_BIT_RANGE, LOIHI2_MANTISSA_MAX_VALUE, EPSILON
from typing import List
import warnings
from brian2 import get_logger

logger = get_logger(__name__)

def sparse_to_dense(i,j,values, n_rows = None, n_cols = None):
    """
    Take row and column indices from a sparse matrix and generate a full matrix
    containing the corresponding values.
    """
    if n_rows is None:
        n_rows = max(i) + 1
    if n_cols is None:
        n_cols = max(j) + 1
    
    m = np.zeros((n_rows,n_cols))

    m[i,j] = values

    return m

def dense_to_sparse(matrix): 
	"""
	Take a dense matrix and convert it into brian-compatible sparse representation 
	(we don't need to specify the indices i and j since those won't have changed)
	"""

	one_dim_array = matrix[np.nonzero(matrix)]

	return one_dim_array

def generate_spikes(neuron_index, _timebins, _period_bins, num_neurons, N_timesteps):
	"""
	Generate a spike raster from the variables contained in a brian2.SpikeGeneratorGroup.
	Basically it's an implementation of the spikegenerator.py_ template with some minor changes.
	"""
	period = _period_bins
	_n_spikes = 0
	_lastindex = 0
	# Initialize a raster to contain the spikes
	spikes = np.zeros((num_neurons, N_timesteps), dtype=int)

	for t in range(N_timesteps):
		_lastindex_before = _lastindex

		if period > 0:
			t %= period
			if _lastindex_before > 0 and _timebins[_lastindex_before - 1] >= t:
				_lastindex_before = 0

		_n_spikes = np.searchsorted(_timebins[_lastindex_before:], t, side='right')
		_indices = neuron_index[_lastindex_before:_lastindex_before + _n_spikes]
		spikes[_indices , t] = 1

		_lastindex = _lastindex_before + _n_spikes

	return spikes

def check_convert_int(values, name = ""):
	"""
	Check if all given values are integers, if not, throw a warning. Rounds and
	converts the values to 32-bit integers.

	Parameters
	----------
	values : ndarray, list of float
		NumPy array or list of numbers.
	name : str, optional
		Name of the considered variable.
	
	Returns
	-------
	values_int : ndarray
		NumPy array of rounded 32-bit integers
	"""
	values_int = np.int32(np.round(values))
	if np.any(np.abs(values - values_int) > EPSILON):
		warnings.warn(f"Correct fixed-point representation requires integer values, " +
					f"but the values given by '{name} = {values}' contain decimal places.")
	return values_int


class F2F:
	"""
	Static class that handles the conversions between floating point and fixed point numbers required to run
	fixed point simulations in Lava. If parameters are already given in floating point representation (i.e. as ints),
	then the functions in this class will simply act as the identity operator.
	"""

	# Set internally
	_binary_shift = None

	# Set manually through the setter method
	additional_accuracy = 0

	# Updated by the device
	parameters = {}
	mantissa_exp_vars = {}

	def __init__(self):
		raise Exception("Instances of the F2F class are not allowed, use it as a fully static class.")

	@staticmethod
	def update_parameters(parameters : dict, owner_name : str, exceptions : List[str] = []):
		"""
		Use this function to add all the simulation parameters into the converter.
		After having added all the necessary parameters, we will perform the conversion 
		at a later stage.
		"""
		for key,val in parameters.items():
			# Some checks to make sure only numbers are considered
			if key in exceptions:
				continue
			if not isinstance(val,(list,np.ndarray,int,float)):
				continue
			if isinstance(val,list) and len(val):
				# Assume that lists only have consistent data types in them
				if isinstance(val[0],str):
					continue

			name = owner_name + '.' + key
			F2F.parameters[name] = val
	
	@staticmethod
	def add_mantissa_and_exp_param(param: str, mant_name:str = None, exp_name:str = None):
		"""
		Add a parameter to the list of parameters requiring a mantissa and exponent representation.
		This will be used later to distinguish them from common parameters, as the conversion process is 
		different.
		"""
		if not isinstance(param,str):
			raise ValueError(f"Parameter name should be given as a string, not {type(param)}")
		
		mant_name = mant_name if mant_name else param + '_mant'
		exp_name = exp_name if exp_name else param + '_exp'
		# Potentially, the user might have already defined this parameter manually as requiring 
		# mantissa and exponent representation
		if not param in F2F.mantissa_exp_vars:
			F2F.mantissa_exp_vars[param] = {'mant' : mant_name, 'exp' : exp_name, 'exp_val': None}
	
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

	@staticmethod
	def determine_shift_factor():
		"""
		Determine the range of values of our parameters
		"""
		min_value = np.inf
		max_value = -np.inf
		# Only for debugging
		var_max = None
		var_min = None
		add_accuracy = F2F.additional_accuracy
		# First find the min and the max in our parameters
		for varname,var in F2F.parameters.items():
			# We only care about nonzero values of arrays (empty arrays are handled in the try-except)
			if hasattr(var,"shape") and var.shape:
				var = var[np.nonzero(var)]
			# Catch errors if var is empty array (we just skip it then)
			try:
				var_min = np.min(np.abs(var))
				var_max = np.max(np.abs(var))
			except:
				continue
			if var_min < min_value and var_min != 0:
				min_value = var_min
				varname_min = varname
			if var_max > max_value and var_max != 0:
				max_value = var_max
				varname_max = varname
		
		# Check that loihi can handle the max value
		if max_value*2**add_accuracy > LOIHI2_MAX_BIT_RANGE:
			raise ValueError(f"Parameter value exceeds Loihi2 range of values: {var_max} * accuracy(2^{add_accuracy})>{LOIHI2_MAX_BIT_RANGE}")

		# Set the decimal shift accounting for the smallest value
		F2F._binary_shift = max(-int(np.floor(np.log2(abs(min_value)))), 0) + add_accuracy

		logger.debug(f"Found binary shift for F2F converter: {F2F._binary_shift}, min {varname_min}={min_value}, max {varname_max}={max_value}")

		# Make sure loihi can handle the range of scales of the parameters
		param_range = max_value/min_value
		if param_range*2** add_accuracy > LOIHI2_MAX_BIT_RANGE:
			raise ValueError("The range of your parameters exceeds the maximum range of values supported by Loihi2. "\
					f"Please make sure that the range does not exceed {LOIHI2_MAX_BIT_RANGE}. Currently:"\
					f" {var_max}/{var_min} * accuracy(2^{add_accuracy}) = {param_range * 2**add_accuracy}.")
	
	@staticmethod
	def float_to_fixed(value):
		"""
		Convert floating point representation to a consistent fixed point number which accounts
		for the whole range of parameters and the intended decimal accuracy.

		Params:
		-------
			value : floating point value to be converted to fixed point
		
		Returns:
			(int) : converted fixed point representation of the input value
		"""
		# Decimal shift accounting for parameter values is computed in determine_minmax()
		shift_factor = 2 ** F2F._binary_shift
		shifted_val = value * shift_factor
		# Use numpy functions to allow conversion of arrays and matrices
		fixed_val = np.int32(np.round(shifted_val))
		
		return fixed_val
	
	@staticmethod
	def float_to_mantissa_exponent(array, param_name = None):
		"""
		Convert floating point values to fixed point representation but including both the mantissa
		and exponent terms. This is done differently than what we do for simple conversion,
		because we have the additional limit of the reduced number of bits that weights are assigned (typically 8).
		This method can also be called by the user, but then an argument should be given to store the exponent
		for the inverse transformation in the F2F.mantissa_exp attribute.

		Notes:
		------
			The current method is only optimal for static parameters. With dynamic parameters more 
			consideration has to be taken to allow for parameter growth, which with the current method
			could easily result in overflows.
		"""
		# Calculate the shift in the mantissa which maximizes the values of the array within
		# the allowed range.
		std_fixed_num = F2F.float_to_fixed(array)
		if np.all(std_fixed_num == 0):
			return 0, 0

		# Find out if the weights are larger than the 8 bit maximum allowed and by how many bits
		max_val = LOIHI2_MANTISSA_MAX_VALUE.weights if param_name == 'weights' else LOIHI2_MANTISSA_MAX_VALUE.other
		max_bit_to_weight_ratio = np.log2(max_val/np.max(abs(std_fixed_num)))

		# Only shift the weights if the previous calculation returned a negative value (use floor for extra safety)
		mantissa_shift = np.floor(min(max_bit_to_weight_ratio,0))
		mantissa = np.int32(std_fixed_num * 2**mantissa_shift)

		# Only need the exponent if we had to downscale our weights (so sign(mantissa_shift)==-1)
		exponent = np.int32(max(-mantissa_shift,0))
		if param_name:
			# If this parameter was not yet in the list, we add it to the
			# parameters that require this representation. Only needed when this function is 
			# called by the user. 
			if not param_name in F2F.mantissa_exp_vars:
				F2F.add_mantissa_and_exp_param(param_name)
			F2F.mantissa_exp_vars[param_name]['exp_val'] = exponent

		return mantissa, exponent
	
	@staticmethod
	def fixed_to_float(value):
		"""
		Convert fixed point back to floating point in a way compatible with the previous transformation.
		"""

		shift_factor = 2**(-F2F._binary_shift)
		
		return value*shift_factor
	
	@staticmethod
	def mantissa_exponent_to_float(data, param_name: str):
		"""
		Converting these types of parameters requires a first extra shift by the exponent parameter
		to get back to their true value.
		"""
		if not param_name in F2F.mantissa_exp_vars:
			raise ValueError(f"The parameter you are trying to convert {param_name} is not listed in the "
					"parameters that require mantissa and exponent representation. Use simple fixed_to_float instead.")
		
		extra_shift = 2 ** F2F.mantissa_exp_vars[param_name]['exp_val']
		return F2F.fixed_to_float(data*extra_shift)

	
	@staticmethod
	def params_float_to_fixed(params : dict, exceptions: List[str] = []):
		"""
		Converts all the internal parameters to fixed point. Note that we don't need a reverse of this operation
		because parameter values will have changed after running the simulation, so we will need to retrieve them
		directly from the Lava Process one by one.
		Params:
		-------
		params: dict
				A dictionary of the parameters to be converted from floating point to fixed point representation
		exceptions: List(str)
				A list containing names of some parameters which should not be converted (for example array shape or indices).
		
		Notes:
		------
			This method uses the mantissa_exponent static attribute.
			mantissa_exponent: List(str)
				A list containing the names of the parameters that need to be converted in a binary mantissa-exponent 
				representation. This is only required for a few parameters on Loihi2 (for example synaptic weights),
				probably due to the fact that you can save memory in this way.

		"""
		# To avoid 'dictionary changed size during iteration' error
		params_out = params.copy()
		for arg, param in params.items():
			# Some checks to make sure only the right parameters are considered
			if arg in exceptions:
				continue
			if not isinstance(param,(list,np.ndarray,int,float)):
				continue
			if isinstance(param,list) and len(param):
				# Only check first element: assume that lists only have consistent data types in them
				if isinstance(param[0],str):
					continue
			if arg in F2F.mantissa_exp_vars:
				mantissa = F2F.mantissa_exp_vars[arg]['mant']
				exponent = F2F.mantissa_exp_vars[arg]['exp']
				params_out[mantissa], params_out[exponent] = F2F.float_to_mantissa_exponent(param,arg)
			else:
				params_out[arg] = F2F.float_to_fixed(param)
		return params_out

