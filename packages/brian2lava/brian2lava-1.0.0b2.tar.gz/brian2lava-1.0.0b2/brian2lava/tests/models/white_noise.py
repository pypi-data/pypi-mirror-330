from brian2 import ms, mV

white_noise = {
	'white_noise_xi': {
		# -------------------------------
		# equation section
		# -------------------------------
		'equation':
			'''
			dv/dt  = (v-El)/taum + 2*mV*(xi*sqrt(ms) + 0.5)/ms: volt (unless refractory)
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
			'Vt'  : -50*mV,
			'Vr'  : -60*mV,
			'El'  : -52*mV
		},
		'initialize_variables': {
			'v'   :  (-60, 'mV')
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
