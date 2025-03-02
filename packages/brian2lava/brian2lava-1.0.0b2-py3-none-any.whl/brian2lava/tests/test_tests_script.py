# Here since the lava process keeps running and is never closed.
# So if you run this script it will never finish and give back control to the command line.
# How to fix this ?
# adding 
import sys
import os

#sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

import pytest
import numpy as np
from brian2 import ms, defaultclock, NeuronGroup, SpikeMonitor, run, set_device, device
from brian2lava.device import LavaDevice

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
    ng = NeuronGroup(10, eqs, threshold='v > v_thresh', reset='v = 0', refractory=1.5*ms, method='euler')

    # Preset variable value
    ng.v = 7

    # Define spike monitor
    sm = SpikeMonitor(ng)

    # Run simulation
    run(50*ms)

    # Return spike monitor spikes
    return np.array(sm.t)


if __name__ == "__main__":

    sm_brian = run_model_simple(use_lava=False)

    device.reinit()
    device.activate(**device.build_options)
    
    sm_lava = run_model_simple(use_lava=True)    
    
    device.reinit()
    device.activate(**device.build_options)
    
    
    sm_lava = run_model_simple(use_lava=True)
    
    
    
    
    
    if np.array_equal(sm_brian, sm_lava):
        pass
    else:
        raise Exception()