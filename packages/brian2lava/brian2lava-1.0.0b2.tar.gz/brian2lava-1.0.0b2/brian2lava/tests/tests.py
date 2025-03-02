import pytest
import numpy as np
from brian2 import ms, defaultclock, NeuronGroup, SpikeMonitor, run, set_device
from brian2.core.preferences import prefs

# adding the script directory into the PATH as
# the brian2lava device will add its workspace
# here and this has to be known by the lava processes
# called in run.py - instantiate_processes() -
import sys
import os
#sys.path.append(os.path.abspath(os.getcwd()))

# ----------------------------
#         definitions
# ----------------------------
@pytest.fixture
def neuron_model_equations():
    return [
    '''
    dv/dt = 1/ms : 1 (unless refractory)
    ''',
        
    '''
    dv/dt = 1/ms : 1 (unless refractory)
    ''',
    ]


# ----------------------------
#         functions
# ----------------------------


def run_voltage_test(use_lava=False):
    
    # Set lava device
    if use_lava:
        set_device('lava', debug=True)
    else:
        set_device('runtime')
        prefs.codegen.target = 'numpy'

    # Set defaultclock
    defaultclock.dt = 0.5*ms

    # Define parameters
    v_thresh = 10

    # Define equation
    eqs = '''
        dv/dt = 1/ms : 1 (unless refractory)
    '''

    # Create neuron group
    # FIXME: name='neurongroup' is only needed until the hard coded code in lava is changed, this will happen
    # once lava multi processes are implemented. Until then we can only run one Neurongroup with the name 'neurongroup'
    ng = NeuronGroup(10, eqs, threshold='v > v_thresh', reset='v = 0', refractory=1.5*ms, method='euler', name='neurongroup')

    # Preset variable value
    ng.v = 7

    # Define spike monitor
    sm = SpikeMonitor(ng)

    # Run simulation
    run(50*ms)

    # Return spike monitor data
    # If you return the full monitor it will held in memory
    # and hence brian will not be able to run
    # the next sim since the magic network will find the object
    # residing in RAM and does not know if it should run again.
    return np.array(sm.t)





def run_model_simple(use_lava=False):
    
    # Set lava device
    if use_lava: set_device('lava', debug=True)

    # Set defaultclock
    defaultclock.dt = 0.5*ms

    # Define parameters
    v_thresh = 10

    # Define equation
    eqs = '''
        dv/dt = 1/ms : 1 (unless refractory)
    '''

    # Create neuron group
    # FIXME: name='neurongroup' is only needed until the hard coded code in lava is changed, this will happen
    # once lava multi processes are implemented. Until then we can only run one Neurongroup with the name 'neurongroup'
    ng = NeuronGroup(10, eqs, threshold='v > v_thresh', reset='v = 0', refractory=1.5*ms, method='euler', name='neurongroup')

    # Preset variable value
    ng.v = 7

    # Define spike monitor
    sm = SpikeMonitor(ng)

    # Run simulation
    run(50*ms)

    # Return spike monitor data
    # If you return the full monitor it will held in memory
    # and hence brian will not be able to run
    # the next sim since the magic network will find the object
    # residing in RAM and does not know if it should run again.
    return np.array(sm.t)


# ----------------------------
#         tests
# ----------------------------

def test_model_simple():
    
    sm_lava = run_model_simple(use_lava=True)
    sm_brian = run_model_simple()
    

    #assert True if (np.array_equal(sm_lava.t, sm_lava.t)) else (assert False)
    if np.array_equal(sm_brian, sm_lava):
        assert True
    else:
        assert False
    
    # Print results are only shown if test fails (= assert False)
    # assert False
    #assert True
