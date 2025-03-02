from brian2 import NeuronGroup, StateMonitor, SpikeMonitor, ms, second, mV, run, get_device, Synapses, defaultclock, BrianLogger
import numpy as np
from numpy.testing import assert_array_equal, assert_allclose
from brian2lava.tests.utils import *
from brian2lava.utils.const import HARDWARE

# Uncomment the following to run tests with custom model repo.
#@pytest.mark.parametrize("config", [{"hardware" : "CPU", "models_dir" : "/homes/jlubo/brian2lava-models/models"}])
# Uncomment the following to run tests on Loihi as well.
@pytest.mark.parametrize("config", [{"hardware" : "CPU", "models_dir" : "/homes/jlubo/brian2lava-models/models"}, 
                                    {"hardware" : "Loihi2", "models_dir" : "/homes/jlubo/brian2lava-models/models", "lava_proc_dir" : "/homes/jlubo/brian2lava-models/lava_proc"}])
@use_lava_device_preset_mode
def test_preset_mode_general(config):
    """
    Make sure that the preset mode is initialized properly.
    TODO Check the Lava processes.
    """
    print(f"Test config: {config}")
    # Check that the device has been set properly
    device = get_device()
    assert device.mode == "preset"
    assert device.num_repr == "fixed"
    assert device.f2f is None

# Uncomment the following to run tests with custom model repo.
#@pytest.mark.parametrize("config", [{"hardware" : "CPU", "models_dir" : "/home/jlubo/brian2lava-models/models"}])
# Uncomment the following to run tests on Loihi as well.
@pytest.mark.parametrize("config", [{"hardware" : "CPU", "models_dir" : "/homes/jlubo/brian2lava-models/models"}, 
                                    {"hardware" : "Loihi2", "models_dir" : "/homes/jlubo/brian2lava-models/models", "lava_proc_dir" : "/homes/jlubo/brian2lava-models/lava_proc"}])
@use_lava_device_preset_mode
def test_preset_mode_variable_consistency_after_run(config):
    """
    In fixed point models we manipulate some values **before** running the simulation.
    This tests that we retrieve consistent parameter values **after** running the simulation.
    Main recipients:
        - Synaptic weights use mantissa/exp representation
        - Probabilistic spiker uses probabilities, which are converted to range (0,2**12)
    """
    from brian2lava.preset_mode.model_loader import probspiker
    from brian2lava.preset_mode.model_loader import lif

    device = get_device()
    
    N = 5
    cf = 1000
    defaultclock.dt = 1 * cf * ms
    tau_j = 0 * cf * ms
    tau_v = 81.92 * cf * ms
    v_th = 100 * cf * mV
    v_rs = -5 * cf * mV
    ps = NeuronGroup(N, probspiker.equations,
                     threshold = probspiker.conditions['th'],
                     reset=probspiker.conditions['rs'])
    ps.p_spike = 0.6
    p_before = np.asarray(ps.p_spike)
    ng = NeuronGroup(N, lif.equations,
                     threshold=lif.conditions['th'],
                     reset=lif.conditions['rs'],
                     method='euler')
    ng.bias = 1 * mV/ms
    ng.v = "1 * cf*mV"
    
    syn = Synapses(ps, ng, model = 'w : volt/second', on_pre='j_post += w')
    syn.connect()
    bias_before = np.asarray(ng.bias)
    syn.w = 0.3 * cf*mV/ms
    w_before = np.asarray(syn.w)
    run(10*cf*ms)
    # Loihi 2 internally optimizes/alters the mantissa-and-exponent representation (cf. 'dense/ncmodels.py'),
    # therefore, we can only check if the weights after running are a multiple of the weights before (both have
    # base 2 representation)
    # TODO The weight exponents may be read out at some point, cf. 'run.py'
    if device.hardware == HARDWARE.Loihi2:
        assert_array_equal(w_before % np.array(syn.w_), np.zeros_like(w_before))
    else:
        assert_array_equal(w_before, syn.w_)
    assert_allclose(p_before, ps.p_spike)
    assert_allclose(bias_before, ng.bias_)

# Uncomment the following to run tests with custom model repo.
#@pytest.mark.parametrize("config", [{"hardware" : "CPU", "models_dir" : "/home/jlubo/brian2lava-models/models"}])
# Uncomment the following to run tests on Loihi as well.
@pytest.mark.parametrize("config", [{"hardware" : "CPU", "models_dir" : "/homes/jlubo/brian2lava-models/models"}, 
                                    {"hardware" : "Loihi2", "models_dir" : "/homes/jlubo/brian2lava-models/models", "lava_proc_dir" : "/homes/jlubo/brian2lava-models/lava_proc"}])
@use_lava_device_preset_mode
def test_preset_mode_spike_transmission(config):
    """
    This tests the correct transmission of spikes in preset mode, using the LIF model.
    The presynaptic neuron is expected to fire at maximal rate, the postsynaptic neuron
    is expected to follow with a latency of one timestep.
    """
    from brian2lava.preset_mode.model_loader import lif

    #BrianLogger.log_level_debug()
    cf = 1000
    defaultclock.dt = 1 * cf * ms
    tau_j = 0 * cf * ms
    tau_v = 81.92 * cf * ms
    v_th = 100 * cf * mV
    v_rs = -5 * cf * mV

    # Add a presynaptic neuron group (of 1 neuron)
    ng0 = NeuronGroup(1, lif.equations, 
                         threshold=lif.conditions["th"], 
                         reset=lif.conditions["rs"], 
                         method='euler')
    ng0.bias = 50 * mV/ms
    ng0.v = 0 * cf * mV
    
    # Add a postsynaptic neuron group (of 1 neuron)
    ng1 = NeuronGroup(1, lif.equations, 
                          threshold=lif.conditions["th"], 
                          reset=lif.conditions["rs"], 
                          method='euler')
    ng1.bias = 0 * mV/ms
    ng1.v = 0 * cf * mV
    
    # Add a synapses group
    syn = Synapses(ng0, ng1, model = 'w : volt/second', on_pre='j_post += w')
    syn.connect()
    syn.w = 40.96 * cf*mV/ms
    
    # Add spike monitors (recording from all neurons - on Loihi, currently only one spike monitor can be used)
    #spm0 = SpikeMonitor(ng0, variables='v', record=[0])
    spm1 = SpikeMonitor(ng1, variables='v', record=[0])
    
    # Run the simulation
    run(10*cf*ms)
    
    # Test spike indices and times
    spike_times = np.array([3, 6, 9])*cf*ms
    #print(f"spm0.i = {spm0.i}")
    #print(f"spm0.t = {spm0.t}")
    #print(f"spm1.i = {spm1.i}")
    #print(f"spm1.t = {spm1.t}")
    #assert_array_equal(spm0.t, spike_times)
    assert_array_equal(spm1.t, spike_times)

# Uncomment the following to run tests with custom model repo.
#@pytest.mark.parametrize("config", [{"hardware" : "CPU", "models_dir" : "/homes/jlubo/brian2lava-models/models"}])
# Uncomment the following to run tests on Loihi as well.
#@pytest.mark.parametrize("config", [{"hardware" : "CPU", "models_dir" : "/homes/jlubo/brian2lava-models/models"}, 
#                                    {"hardware" : "Loihi2", "models_dir" : "/homes/jlubo/brian2lava-models/models", "lava_proc_dir" : "/homes/jlubo/brian2lava-models/lava_proc"}])
@use_lava_device_preset_mode
def test_device_reinit(config):
    """
    Test that the device can be reinitialized and run multiple simulations
    without running into problems. The problems that could arise are some leftover
    references to previously defined objects that are not cleaned up properly.
    """
    from brian2.core.network import Network
    for k in range(4,16):
        old_device = get_device()
        set_device('lava', **old_device.build_options)
        device = get_device()
        device.reinit()
        # Build options have to be passed dedicatedly, otherwise they are lost
        device.activate(**device.build_options)

        from brian2lava.preset_mode.model_loader import lif
        from brian2lava.preset_mode.model_loader import probspiker

        cf = 1000
        defaultclock.dt = 1 * cf * ms
        bias = 0 * mV/ms
        tau_j = 0 * cf * ms
        tau_v = 81.92 * cf * ms
        v_th = 100 * k * cf * mV
        v_rs = -5 * cf * mV

        # Have to use a custom network because of MagicError 
        net = Network()

        G = NeuronGroup(k, lif.equations,
                        threshold=lif.conditions['th'],
                        reset=lif.conditions['rs'])
        net.add(G)
        # This should reproduce the error: when simulations contain different models,
        # but the model is loaded from cache due to naming conflicts, then these
        # inconsistencies should cause errors.
        if k < 6:
            P = NeuronGroup(k, probspiker.equations,
                            threshold=probspiker.conditions['th'],
                            reset=probspiker.conditions['rs'])
            P.p_spike = k/16
            net.add(P)
        
        S = Synapses(G, G, model = 'w : volt/second', on_pre='j_post += w')
        S.connect(i=0, j=range(k))
        S.w = 1 * mV/ms
        net.add(S)

        M = StateMonitor(G, 'v', record=True)

        net.run(1*cf*ms)
            
    assert True


if __name__ == '__main__':
    # test_preset_mode_general({})
    # test_preset_mode_variable_consistency_after_run({})
    test_device_reinit({})
