from brian2 import ms

# FIXME
# lava can not handle it for some reason the error is:
# Encountered Fatal Exception: issubclass() arg 1 must be a class
# Traceback: 
# Traceback (most recent call last):
#   File "/home/juppy/venv_b2l/lib/python3.8/site-packages/lava/magma/runtime/runtime.py", line 94, in target_fn
#     actor = builder.build()
#   File "/home/juppy/venv_b2l/lib/python3.8/site-packages/lava/magma/compiler/builders/py_builder.py", line 361, in build
#     if issubclass(lt.cls, np.ndarray):
# TypeError: issubclass() arg 1 must be a class

loihi1 = {
	'Loihi1CUBA': {

		'equation':
			'''
			rnd_v = int(sign(v)*ceil(abs(v*tau_v))) : 1
			rnd_I = int(sign(I)*ceil(abs(I*tau_I))) : 1
			dv/dt = -rnd_v/ms + I/ms: 1 (unless refractory)
			dI/dt = -rnd_I/ms: 1
			''',

		'threshold_condition':
			'v > Vt',

		'reset_condition':
			'v = Vr',

		'refractory_time':
			5*ms,

		'method':
			'euler',
		
		'external_stimulation':
			False,

		# defines the excitatory variable that will be used when
		'synaptic_input_variable_ex':
			'I',

		'synaptic_input_variable_in':
			'I',

		# defines the weight used for an artificial stimulation
		'synaptic_weight_ex':
			9,

		'synaptic_weight_in':
			-7,

		'neuron_variables': {
			'tau_v': (1024/2**12),
			'tau_I': (512/2**12),
			'Vt'  : 64*2**6,
			'Vr'  : 0
		},
		# Initial variables
		'initialize_variables': {
			'v'   :  (0, '1')
		},

		'simulation_runtime':
			150*ms,

		# defines which variable will be monitored via a TraceMonitor()
		'state_variable_to_compare':
			'v',

		# stimulation indices, times
		'stimulation_ex':{
			'indices': [0,0],
			'times'  : [1*ms, 50*ms]
		},

		'stimulation_in':{
			'indices': [0],
			'times'  : [30*ms]
		}
	}
}
