from brian2 import NeuronGroup, StateMonitor, ms, run, Synapses
import numpy as np
from brian2lava.tests.utils import *

@use_lava_device
def test_variables(config):
    """
    Make sure that complex processes of variable assignment work properly
    """
    ng = NeuronGroup(20,"v:1")
    s = Synapses(ng,ng,model = 'w:1')
    s.connect()
    ng.v[:] = 1
    ng.v[:] = "rand()"
    ng.v[3:8] = np.arange(5)
    ng.v[9:15] = 0
    mon = StateMonitor(ng,"v", record = True)
    # The statemonitor for synapses has a special treatment for synaptic variables
    syn_mon = StateMonitor(s,'w', record = [0,1,5])
    run(0.5*ms)
    # Neurongroup variables
    assert (ng.v[3:8] == np.arange(5)).all()
    assert (ng.v[9:15] == np.zeros((6))).all()
    assert (ng.v[:3] != np.ones((3,))).all() and (ng.v[15:] != np.ones((5,))).all()

    # Monitor values at last timestep
    assert (mon.v[3:8,-1] == np.arange(5)).all()
    assert (mon.v[9:15,-1] == np.zeros((6))).all()
    assert (mon.v[:3,-1] != np.ones((3,))).all() and (ng.v[15:] != np.ones((5,))).all()

if __name__ == '__main__':
    test_variables({})
