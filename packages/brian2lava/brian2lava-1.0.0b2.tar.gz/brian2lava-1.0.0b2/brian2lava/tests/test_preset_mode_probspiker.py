from brian2 import NeuronGroup, SpikeMonitor, StateMonitor, ms, Hz, run, get_device, Synapses, defaultclock, seed
import numpy as np
from numpy.testing import assert_allclose
from brian2lava.tests.utils import *

# Uncomment the following to run tests with custom model repo.
#@pytest.mark.parametrize("config", [{"hardware" : "CPU", "models_dir" : "/homes/jlubo/brian2lava-models/models"}])
# Uncomment the following to run tests on Loihi as well.
@pytest.mark.parametrize("config", [{"hardware" : "CPU", "num_repr" : "fixed", "models_dir" : "/homes/jlubo/brian2lava-models/models"}, 
                                    {"hardware" : "Loihi2", "num_repr" : "fixed", "models_dir" : "/homes/jlubo/brian2lava-models/models", "lava_proc_dir" : "/homes/jlubo/brian2lava-models/lava_proc"}])
@use_lava_device_preset_mode
def test_preset_mode_probspiker(config):
    """
    Specific tests to ensure the correctness of the properties of the probspiker neuron.
    """
    from brian2lava.preset_mode.model_loader import probspiker

    # Define group of `probspiker` neurons
    N = 10
    freq = 50.0 * Hz
    defaultclock.dt = 0.5 * ms
    t_duration = 1000 * ms
    p_spike_0 = np.clip(freq * defaultclock.dt, 0, 1)  # spiking probability per time bin
    P = NeuronGroup(N,
                    probspiker.equations,
                    threshold = probspiker.conditions['th'],
                    reset = probspiker.conditions['rs'])
    P.p_spike = p_spike_0

    # Add monitors for spikes
    spmP = SpikeMonitor(P, variables='rnd', record=True)

    # Add monitor for rnd state
    stmP = StateMonitor(P, variables=['rnd', 'p_spike'], record=True)

    # Run the simulation
    run(t_duration)

    # Test for mean of the uniformly distributed random numbers
    assert_allclose(np.mean(stmP.rnd, axis=1), 0.5*np.ones(stmP.rnd.shape[0]), atol=0.03)
    
    # Test for variance of the uniformly distributed random numbers
    assert_allclose(np.var(stmP.rnd, axis=1), 1/12*np.ones(stmP.rnd.shape[0]), atol=0.03)

    # Test for expected number of spikes
    assert_allclose(len(spmP.i), N*freq*t_duration, rtol=0.15)
    

if __name__ == '__main__':
    test_preset_mode_probspiker({})