import numpy as np
from brian2lava.utils.const import EPSILON
from brian2 import get_device

def sparse_to_dense(i, j, values, n_rows = None, n_cols = None):
	"""
	Take row and column indices from a sparse matrix and generate a full matrix
	containing the corresponding values.
	For weight matrices: the weight matrix should be (out_size,in_size):
	e.g. 2 sources, 3 targets
						| 0 0 | 
		s_in (2) -> W = | 0 0 | * s_in -> a_out (3)
						| 0 0 |
	In this function (and brian) in_idx = i and out_idx = j

	Parameters
	----------
	i : `list` of `int`
		Row indices (synaptic sources).
	j : `list` of `int`
		Column indices (synaptic targets).
	values : `list` of `float`
		Values of the sparse representation.
	n_rows : `int`, optional
		Number of rows in the full matrix. If `None`, 
		the maximum of the row indices is used.
	n_cols : `int`, optional
		Number of columns in the full matrix. If `None`, 
		the maximum of the column indices is used.

	Returns
	-------
	`ndarray`
		Full matrix	containing the values from the sparse representation
		(transposed because Lava requires this).
	"""
	if n_rows is None:
		n_rows = max(i) + 1
	if n_cols is None:
		n_cols = max(j) + 1
	
	m = np.zeros((n_rows,n_cols))

	m[i,j] = values

	return m.T

def dense_to_sparse(matrix): 
	"""
	Take a dense matrix and convert it into Brian-compatible sparse representation.

	Parameters
	----------
	matrix : `ndarray`
		Full matrix representation (transposed because Lava requires this).

	Returns
	-------
	`ndarray`
		Sparse matrix representation in a one-dimensional array.
	"""

	matrix_T = matrix.transpose()
	one_dim_array = matrix_T[np.nonzero(matrix_T)]

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

def check_convert_to_int32(values, name = ""):
	"""
	Checks if all given values are integers, if not, throws a warning. Then, rounds and
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
	test_mask = np.abs(values - values_int) > EPSILON
	if np.any(test_mask):
		# Throw a warning and provide print the affected value (in case of an array, one of 
		# the affected values only).
		if isinstance(values, np.ndarray):
			values_output = values[test_mask][0]
			#values_output = values[test_mask] # all values
		else:
			values_output = values
		logger = get_device().logger
		logger.warn(f"Fixed-point representation requires integer values, but the " +
                    f"value of '{name} = {values_output}' contains decimal places. " +
                    f"These will be lost due to conversion, causing a certain imprecision.")
	return values_int
