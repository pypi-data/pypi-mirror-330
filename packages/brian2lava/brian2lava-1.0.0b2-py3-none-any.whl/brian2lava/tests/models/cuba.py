from brian2 import ms, mV

cuba = {
	'CUBA': {
		# -------------------------------
		# equation section
		# -------------------------------
		'equation':
			'''
			dv/dt  = (ge+gi-(v-El))/taum : volt (unless refractory)
			dge/dt = -ge/taue : volt
			dgi/dt = -gi/taui : volt
			''',

		'threshold_condition':
			'v > Vt',

		'reset_condition':
			'v = Vr',

		'refractory_time':
			5*ms,

		'method':
			'euler',
		# -------------------------------
		# input stimuli section
		# -------------------------------
		# should the neuron receive external input?
		# If yes a InputGnereator will be defined.
		# If false then you do not need to specifie all the
		# other parameters in this section.
		'external_stimulation':
			False,

		# defines the excitatory variable that will be used when
		# stimulating the neuron with an artrificial input
		'synaptic_input_variable_ex':
			'ge',

		'synaptic_input_variable_in':
			'gi',

		# defines the weight used for an artificial stimulation
		'synaptic_weight_ex':
			9*mV,

		'synaptic_weight_in':
			-7*mV,

		# stimulation indices, times
		# the neuron at indices will receive a stimulation on the respective
		# times table index.
		# you specify input times for excitatory ex
		# and inhibitory in.
		# if you specify just empty time lists, then no input will be given.
		# so:
		# {
		#    'indices': [0],
		#    'times'  : []
		# }
		#
		# otherwise specify a time which to long to reach for the simulation runtime.
		'stimulation_ex':{
			'indices': [0,0],
			'times'  : [1*ms, 50*ms]
		},

		'stimulation_in':{
			'indices': [0],
			'times'  : [30*ms]
		},
		# -------------------------------
		# variable section
		# -------------------------------
		#
		# dictionary with name, value and SI unit
		#    e.g {'v': 10*mV}
		#
		# IMPORTANT!:
		# do not forget to specify all static variables here.
		# this includes the firing threshold and all other variables
		# refereed to in any condition above and below.
		'neuron_variables': {
			'taum':  20*ms,
			'taue':  5 *ms,
			'taui':  10*ms,
			'Vt'  : -50*mV,
			'Vr'  : -60*mV,
			'El'  : -55*mV
		},
		# Initial variables
		# these variables will be initialized
		# with neuron.var_name = value
		# they need to be specify as tuple with their value as int
		# and their unit as string
		'initialize_variables': {
			'v'   :  (-55, 'mV')
		},

		# -------------------------------
		# simulation section
		# -------------------------------
		'simulation_runtime':
			200*ms,

		# defines which variable will be monitored via a TraceMonitor()
		'state_variable_to_compare':
			'v'
	}
}
