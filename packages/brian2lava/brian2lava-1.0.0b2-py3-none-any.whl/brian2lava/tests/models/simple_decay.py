from brian2 import ms

simple_decay = {
	'to_1': {
		# -------------------------------
		# equation section
		# -------------------------------
		'equation':
			'''
			dv/dt = (1-v)/taum : 1
			''',

		'threshold_condition':
			'v > Vt',

		'reset_condition':
			'v = Vr',

		'refractory_time':
			2*ms,

		'method':
			'euler',
		# -------------------------------
		# input stimuly section
		# -------------------------------
		'external_stimulation':
			False,
		# -------------------------------
		# variable section
		# -------------------------------
		'neuron_variables': {
			'taum':  20*ms,
			'Vt'  :  1,
			'Vr'  :  0
		},
		'initialize_variables': {
			'v'   :  (0, '1')
		},
		# -------------------------------
		# simulation section
		# -------------------------------
		'simulation_runtime':
			200*ms,
		'state_variable_to_compare':
			'v'
	}
}
