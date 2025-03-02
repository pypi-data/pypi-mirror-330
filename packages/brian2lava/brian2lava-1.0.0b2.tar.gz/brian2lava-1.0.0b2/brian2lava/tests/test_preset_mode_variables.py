from brian2 import NeuronGroup, StateMonitor, ms, second, mV, run, Synapses, defaultclock, seed
import numpy as np
import pytest
from brian2lava.tests.utils import *
from brian2lava.utils.const import HARDWARE

# Uncomment the following to run tests with standard model repo.
#@pytest.mark.parametrize("config", [{"hardware" : "CPU", "use_synapses" : False}, 
#                                    {"hardware" : "CPU", "use_synapses" : True}])
# Uncomment the following to run tests with custom model repo.
#@pytest.mark.parametrize("config", [{"hardware" : "CPU", "use_synapses" : False, "models_dir" : "/homes/jlubo/brian2lava-models/models"}, 
#                                    {"hardware" : "CPU", "use_synapses" : True, "models_dir" : "/homes/jlubo/brian2lava-models/models"}])
# Uncomment the following to run tests on Loihi as well.
@pytest.mark.parametrize("config", [{"hardware" : "CPU", "use_synapses" : False, "models_dir" : "/homes/jlubo/brian2lava-models/models"}, 
                                    {"hardware" : "CPU", "use_synapses" : True, "models_dir" : "/homes/jlubo/brian2lava-models/models"},
                                    {"hardware" : "Loihi2", "use_synapses" : False, "models_dir" : "/homes/jlubo/brian2lava-models/models", "lava_proc_dir" : "/homes/jlubo/brian2lava-models/lava_proc"}, 
                                    {"hardware" : "Loihi2", "use_synapses" : True, "models_dir" : "/homes/jlubo/brian2lava-models/models", "lava_proc_dir" : "/homes/jlubo/brian2lava-models/lava_proc"}])
@use_lava_device_preset_mode
def test_preset_mode_ng_variables(config):
    """
    Make sure that variable assignment works properly for NeuronGroup objects. Includes
    simple tests for Synapses object as well. Tests are similar to those in 'test_variables.py'.
    """
    device = get_device()
    print(f"Test config: {config}")
    # Import LIF_rp_delta_v_input neuron model from library
    from brian2lava.preset_mode.model_loader import lif_rp_delta_v_input
    ## Define fixed-point conversion factor
    cf = 1000
    # Define random seed
    seed(1)
    # Define parameters whose values are scaled up to be integers. The voltage time constant `tau_v`
    # is set to a very large value so that the initial setting does not significantly change
    # over time.
    N = 20
    defaultclock.dt = 1 * cf * ms
    bias = 0 * mV/ms
    tau_v = 10000 * cf * ms
    v_th = 100 * cf * mV
    v_rs = -5 * cf * mV
    t_ref = 2 * cf * ms
    ng = NeuronGroup(N, lif_rp_delta_v_input.equations, 
                     threshold=lif_rp_delta_v_input.conditions["th"], 
                     reset=lif_rp_delta_v_input.conditions["rs"], 
                     refractory='t_ref',
                     method='euler')
    ng.v = "1 * cf*mV"
    ng.v[3:8] = np.arange(5) * cf*mV
    ng.v[9:15] = 0 * cf*mV
    ng.v[15:] = "rand() * cf*mV"
    ng_mon = StateMonitor(ng, "v", record = True)
    
    # Consider synapses only if requested
    if config.get('use_synapses'):
        # Create Synapses object and all-to-all connections
        syn = Synapses(ng, ng, model = 'w : volt', on_pre = 'v_post += w')
        syn.connect()
        # First set weights for all neurons to very small value.
        w_n = 0.001
        syn.w = w_n * mV/ms * tau_v
        # Set weights of the first 2 neurons to somewhat larger value.
        w_0 = 0.05
        syn.w[:2*N] = w_0 * mV/ms * tau_v
    # Run the simulation
    run(30*cf*ms)
    # Direct readout of NeuronGroup variables
    assert (ng.v[:3] == np.ones((3))*cf*mV).all()
    assert (ng.v[3:8] == np.arange(5)*cf*mV).all()
    assert (ng.v[9:15] == np.zeros((6))*mV).all()
    assert (ng.v[15:] != np.ones((5))*cf*mV).any()

    # Monitor values at last timestep
    assert (ng_mon.v[:3,-1] == np.ones((3))*cf*mV).all()
    assert (ng_mon.v[3:8,-1] == np.arange(5)*cf*mV).all()
    assert (ng_mon.v[9:15,-1] == np.zeros((6))*mV).all()
    assert (ng_mon.v[15:,-1] != np.ones((5))*cf*mV).any()

    # Consider synapses only if requested; not doing this on Loihi 2 because it internally optimizes/alters
    # the mantissa-and-exponent representation (cf. 'dense/ncmodels.py', also cf. 'test_preset_mode_general.py')
    if config.get('use_synapses') and not device.hardware == HARDWARE.Loihi2:
        # Direct readout of Synapses variables
        #print(f"syn.w = {syn.w}")
        #print(f"w_n * np.ones((N*N))*cf*mV/ms = {w_n * np.ones((N*N))*cf*mV/ms}")
        assert (syn.w[2*N:] == w_n * np.ones(((N-2)*N))*mV/ms * tau_v).all()
        assert (syn.w[:2*N] == w_0 * np.ones((2*N))*mV/ms * tau_v).all()


# Uncomment the following to run tests with standard model repo.
@pytest.mark.parametrize("config", [{"hardware" : "CPU", "w_0" : 0.05, "w_n" : 0.01}, 
                                    {"hardware" : "CPU", "w_0" : 0.05, "w_n" : 0}])
# Uncomment the following to find that high weight values break it.
#@pytest.mark.parametrize("config", [{"hardware" : "CPU", "w_0" : 0.05, "w_n" : 0.001}, 
#                                    {"hardware" : "CPU", "w_0" : 0.05, "w_n" : 0}, 
#                                    {"hardware" : "CPU", "w_0" : 1, "w_n" : 0.001}, 
#                                    {"hardware" : "CPU", "w_0" : 1, "w_n" : 0}])
# Uncomment the following to run tests with custom model repo.
#@pytest.mark.parametrize("config", [{"hardware" : "CPU", "w_0" : 0.05, "w_n" : 0.01, "models_dir" : "/homes/jlubo/brian2lava-models/models"},
#                                    {"hardware" : "CPU", "w_0" : 0.05, "w_n" : 0, "models_dir" : "/homes/jlubo/brian2lava-models/models"}])
# Uncomment the following to run tests on Loihi as well (but currently these will be skipped anyway).
#@pytest.mark.parametrize("config", [{"hardware" : "CPU", "w_0" : 0.05, "w_n" : 0.01, "models_dir" : "/homes/jlubo/brian2lava-models/models", "lava_proc_dir" : "/homes/jlubo/brian2lava-models/lava_proc"},
#                                    {"hardware" : "CPU", "w_0" : 0.05, "w_n" : 0, "models_dir" : "/homes/jlubo/brian2lava-models/models", "lava_proc_dir" : "/homes/jlubo/brian2lava-models/lava_proc"},
#                                    {"hardware" : "Loihi2", "w_0" : 0.05, "w_n" : 0.01, "models_dir" : "/homes/jlubo/brian2lava-models/models", "lava_proc_dir" : "/homes/jlubo/brian2lava-models/lava_proc"},
#                                    {"hardware" : "Loihi2", "w_0" : 0.05, "w_n" : 0, "models_dir" : "/homes/jlubo/brian2lava-models/models", "lava_proc_dir" : "/homes/jlubo/brian2lava-models/lava_proc"}])
@use_lava_device_preset_mode
def test_preset_mode_syn_variables(config):
    """
    Make sure that variable assignment works properly for Synapses objects. All-to-all as well as sparse
    connectivity is tested.
    """
    device = get_device()
    # print(f"Test config: {config}")
    # Import LIF_rp_delta_v_input neuron model from library
    from brian2lava.preset_mode.model_loader import lif_rp_delta_v_input
    ## Define fixed-point conversion factor
    cf = 1000
    # Define random seed
    seed(1)
    # Define parameters whose values are scaled up to be integers. The voltage time constant `tau_v`
    # is set to a very large value so that the initial setting does not significantly change
    # over time.
    N = 20
    defaultclock.dt = 1 * cf * ms
    bias = 0 * mV/ms
    tau_v = 100 * cf * ms
    v_th = 100 * cf * mV
    v_rs = -5 * cf * mV
    t_ref = 2 * cf * ms
    ng = NeuronGroup(N, lif_rp_delta_v_input.equations, 
                     threshold=lif_rp_delta_v_input.conditions["th"], 
                     reset=lif_rp_delta_v_input.conditions["rs"], 
                     refractory='t_ref',
                     method='euler')
    ng.v = "1 * cf*mV"
    
    # Create Synapses object and specific connections
    #syn = Synapses(ng, ng, model = 'w : volt/second', on_pre='j_post += w')
    #syn.connect(i=[0], j=[0,1,2])
    # Create Synapses object and all-to-all connections
    syn = Synapses(ng, ng, model = 'w : volt', on_pre='v_post += w')
    syn.connect()
    # Set weights for the first 2 neurons, using the initial weight value 0.05, 
    # unless another value is provided.
    w_0 = config.get('w_0', 0.05)
    syn.w[:2*N] = w_0 * mV/ms * tau_v
    # Set weights for the remaining neurons to small value (if this is zero, 
    # the synapses will be removed).
    w_n = config.get('w_n', 0.001)
    syn.w[2*N:] = w_n * mV/ms * tau_v
    # print(syn.w)
    # Set monitor
    #syn_mon = StateMonitor(syn, 'w', record = True)
    #syn_mon = StateMonitor(syn, 'w', record = [0])
    # Run the simulation
    run(30*cf*ms)
    # Direct readout of Synapses variables; not doing this on Loihi 2 because it internally optimizes/alters
    # the mantissa-and-exponent representation (cf. 'dense/ncmodels.py', also cf. 'test_preset_mode_general.py')
    if device.hardware == HARDWARE.Loihi2:
        pytest.skip("not applicable to Loihi 2")
    # print(f"syn.w = {syn.w}, expected = {w_0 * cf*mV/ms}")
    #print(f"w_n * np.ones((N*N))*cf*mV/ms = {w_n * np.ones((N*N))*cf*mV/ms}")
    assert (syn.w[:2*N] == w_0 * np.ones((2*N,))*mV/ms * tau_v).all()
    # If `w_n` is zero, the synapses will have been removed.
    if w_n > 0:
        print(f"len(syn.w) = {len(syn.w)}")
        assert (syn.w[2*N:] == w_n * np.ones(((N-2)*N))*mV/ms * tau_v).all()
    else:
        assert len(syn.w) == 2*N

    # Monitor values at last timestep
    #assert (syn_mon.w[:2*N,-1] == w_0 * np.ones((N,N))*cf*mV/ms).all()


if __name__ == '__main__':
    # test_preset_mode_ng_variables({})
    test_preset_mode_syn_variables({})
