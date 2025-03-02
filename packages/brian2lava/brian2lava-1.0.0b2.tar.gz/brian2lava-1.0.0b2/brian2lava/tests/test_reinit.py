from brian2 import NeuronGroup, get_device, set_device, run, ms, StateMonitor, Synapses

def test_device_reinit():
    """
    Test that the device can be reinitialized and run multiple simulations
    without running into problems. The problems that could arise are some leftover
    references to previously defined objects that are not cleaned up properly.
    """

    set_device('lava', hardware = 'CPU')
    device = get_device()
    for k in range(4,16):
        device.reinit()
        # Build options have to be passed dedicatedly, otherwise they are lost
        device.activate(**device.build_options)

        G = NeuronGroup(k, "v:1", threshold='v>1', reset='v = 0', method='exact')

        S = Synapses(G, G, 'w : 1')
        S.connect(i=0, j=[1, 2])

        M = StateMonitor(G, 'v', record=True)

        run(10*ms)
            
    assert True


if __name__ == '__main__':
    test_device_reinit()