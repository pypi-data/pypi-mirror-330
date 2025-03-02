import pytest
import numpy as np
from numpy.testing import assert_array_equal
from brian2.tests.utils import assert_allclose
from brian2 import NeuronGroup, SpikeMonitor, SpikeGeneratorGroup, Synapses, \
                   ms, mV, run, second, Hz, defaultclock
from brian2lava.tests.utils import *

@use_lava_device
def test_spike_monitor(config):
    G_without_threshold = NeuronGroup(5, "x : 1")
    G = NeuronGroup(
        3,
        """
        dv/dt = rate : 1
        rate: Hz
        """,
        threshold="v>1",
        reset="v=0",
    )
    # We don't use 100 and 1000Hz, because then the membrane potential would
    # be exactly at 1 after 10 resp. 100 timesteps. Due to floating point
    # issues this will not be exact,
    G.rate = [101, 0, 1001] * Hz

    mon = SpikeMonitor(G)

    with pytest.raises(ValueError):
        SpikeMonitor(G, order=1)  # need to specify 'when' as well
    with pytest.raises(ValueError) as ex:
        SpikeMonitor(G_without_threshold)
    assert "threshold" in str(ex)

    # Creating a SpikeMonitor for a Synapses object should not work
    S = Synapses(G, G, on_pre="v += 0")
    S.connect()
    with pytest.raises(TypeError):
        SpikeMonitor(S)

    run(10 * ms)

    spike_trains = mon.spike_trains()

    assert_allclose(mon.t[mon.i == 0], [9.9] * ms)
    assert len(mon.t[mon.i == 1]) == 0
    assert_allclose(mon.t[mon.i == 2], np.arange(10) * ms + 0.9 * ms)
    assert_allclose(mon.t_[mon.i == 0], np.array([9.9 * float(ms)]))
    assert len(mon.t_[mon.i == 1]) == 0
    assert_allclose(mon.t_[mon.i == 2], (np.arange(10) + 0.9) * float(ms))
    assert_allclose(spike_trains[0], [9.9] * ms)
    assert len(spike_trains[1]) == 0
    assert_allclose(spike_trains[2], np.arange(10) * ms + 0.9 * ms)
    assert_array_equal(mon.count, np.array([1, 0, 10]))

    i, t = mon.it
    i_, t_ = mon.it_
    assert_array_equal(i, mon.i)
    assert_array_equal(i, i_)
    assert_array_equal(t, mon.t)
    assert_array_equal(t_, mon.t_)

    with pytest.raises(KeyError):
        spike_trains[3]
    with pytest.raises(KeyError):
        spike_trains[-1]
    with pytest.raises(KeyError):
        spike_trains["string"]

    # Check that indexing into the VariableView works (this fails if we do not
    # update the N variable correctly)
    assert_allclose(mon.t[:5], [0.9, 1.9, 2.9, 3.9, 4.9] * ms)

# Uncomment the following to run tests with custom model repo.
#@pytest.mark.parametrize("config", [{"hardware" : "CPU", "models_dir" : "/homes/jlubo/brian2lava-models/models"}])
# Uncomment the following to run tests on Loihi as well.
@pytest.mark.parametrize("config", [{"hardware" : "CPU", "models_dir" : "/homes/jlubo/brian2lava-models/models"}, 
                                    {"hardware" : "Loihi2", "models_dir" : "/homes/jlubo/brian2lava-models/models", "lava_proc_dir" : "/homes/jlubo/brian2lava-models/lava_proc"}])
@use_lava_device_preset_mode
def test_spike_monitor_preset(config):
    # Import LIF_rp_delta_v_input model from library
    from brian2lava.preset_mode.model_loader import lif_rp_delta_v_input
    ## Define conversion factor
    scf = 1000
    # Set defaultclock
    defaultclock.dt = 1 * scf * ms #0.5*ms

    # Define parameters
    N = 3
    bias = 0.015 * scf * mV/ms
    tau_v = 10 * scf * ms
    v_th = 100 * scf * mV
    v_rs = -5 * scf * mV
    ref = 2 * scf

    # Add a spike generator group
    S = SpikeGeneratorGroup(N, [0, 0, 0], np.array([2, 6, 10])*scf*ms) # <--- only works with N neurons!

    # Add another neuron group (which does not receive a background input)
    Q = NeuronGroup(N, lif_rp_delta_v_input.equations,
                    threshold=lif_rp_delta_v_input.conditions["th"],
                    reset=lif_rp_delta_v_input.conditions["rs"],
                    refractory='ref*ms',
                    method='euler')
    #Q.j = "0.1*mV/ms"
    Q.v = "2 * scf * mV"

    # Add synapses
    syn = Synapses(S, Q, model = 'w : volt', on_pre='v_post += w')
    syn.connect(i=[0], j=[0,1,2])
    syn.w = 40 * mV/ms * tau_v

    # Add spike monitors - one for all neurons, one for a specific neuron,
    # and one for the total number of spikes only
    spm = SpikeMonitor(Q, variables='v', record=True)
    spm_w_indices = SpikeMonitor(Q, variables='v', record=[0])
    spm_no_indices = SpikeMonitor(Q, variables='v', record=False)

    run(30 * scf * ms)
    # Normal spike monitor
    spikes = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert len(spm.i) == 9
    assert len(spm.t) == 9
    assert_array_equal(spm.i,spikes)

    # Spike monitor with selected indices
    assert len(spm_w_indices.i) == 3
    assert len(spm_w_indices.t) == 3

    # Spike monitor with record = False
    # Make sure that i and t are not defined
    with pytest.raises(AttributeError):
        _ = spm_no_indices.i
    with pytest.raises(AttributeError):
        _ = spm_no_indices.t
    # Check that the variable is still being recorded correctly
    assert len(spm_no_indices.v) == 9


if __name__ == '__main__':
    test_spike_monitor_preset({})
