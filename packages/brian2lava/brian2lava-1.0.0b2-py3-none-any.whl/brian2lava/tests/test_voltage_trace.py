import pytest
import numpy as np
from brian2 import ms, mV, defaultclock, prefs, set_device, device, seed, \
                   Network, NeuronGroup, StateMonitor, SpikeGeneratorGroup, Synapses

# Set working directory path such that packages and tempates can be found
# NOTE that it only works if you start the script from the base directory
#os.chdir(os.path.abspath(os.path.join(os.getcwd(), 'brian2lava')))
#sys.path.append(os.getcwd())

# Import the b2l device
from brian2lava.device import LavaDevice

# Import models to test
# Ignore the Pylance warning because the script is called from the base directory
# TODO: This is not very elegant, so we should 
from brian2lava.tests.models.simple_decay import simple_decay # type: ignore
from brian2lava.tests.models.white_noise import white_noise # type: ignore
from brian2lava.tests.models.cuba import cuba # type: ignore
from brian2lava.tests.models.loihi1 import loihi1 # type: ignore

# Defines model to use in parametrized test
NEURON_MODEL_DEFINITIONS = [
    simple_decay,
    white_noise,
    cuba
    #loihi1
]

def run_voltage_simulation(neuron_model, use_lava=False, random_seed=1):

    # Set lava device
    if use_lava:
        set_device('lava', debug=True)
    # If we run code in pure Brian, make sure we use the numpy backend, as these simulations
    # are very small and compiling with cython takes much longer than running with numpy
    # directly
    else:
        set_device('runtime')
        prefs.codegen.target = 'numpy'

    # Make sure that the device is clean
    device.reinit()
    device.activate(**device.build_options)

    # Set defaultclock
    defaultclock.dt = 1*ms

    # Set seed
    seed(random_seed)

    # Define network object holding everything
    net = Network(name='Network_0')

    # Extract the model name/key
    model_name = list(neuron_model.keys())[0]

    # Create neuron group
    # FIXME: name='neurongroup_prefix' is needed since the brian2lava device
    # will create a template for every neurongroup_prefix.
    # If the name is the same it however fails to overwrite it
    # Therefore this name must be unique for every test
    neuron = NeuronGroup(
        1,
        neuron_model[model_name]['equation'],
        threshold=neuron_model[model_name]['threshold_condition'],
        reset=neuron_model[model_name]['reset_condition'],
        refractory=neuron_model[model_name]['refractory_time'],
        method=neuron_model[model_name]['method'],
        namespace=neuron_model[model_name]['neuron_variables'],
        name='neurongroup_' + str(model_name)
    )

    # Initialize variables
    for key in neuron_model[model_name]['initialize_variables']:
        tup = neuron_model[model_name]['initialize_variables'][key]
        exec(f'neuron.{key} = {tup[0]} * {tup[1]}')

    # Add neuron to networks
    net.add(neuron)
    
    # If neuron should receive external input stimulation trough a generator
    if neuron_model[model_name]['external_stimulation']:
        # Excitatory generator definition
        stimulator_ex = SpikeGeneratorGroup(
            1,
            indices=neuron_model[model_name]['stimulation_ex']['indices'],
            times=neuron_model[model_name]['stimulation_ex']['times']
        )

        # Connection to input variable
        synaptic_weight_ex = neuron_model[model_name]['synaptic_weight_ex']
        conn_ex = Synapses(
            stimulator_ex,
            neuron,
            on_pre=neuron_model[model_name]['synaptic_input_variable_ex'] + '+= synaptic_weight_ex'
        )
        conn_ex.connect()

        # Add generator and synapses to network
        net.add(stimulator_ex)
        net.add(conn_ex)

        # Inhibitory generator definition
        stimulator_in = SpikeGeneratorGroup(
            1,
            indices=neuron_model[model_name]['stimulation_in']['indices'],
            times=neuron_model[model_name]['stimulation_in']['times']
        )

        # Connection to input variable
        synaptic_weight_in = neuron_model[model_name]['synaptic_weight_in']
        conn_in = Synapses(
            stimulator_in,
            neuron,
            on_pre=neuron_model[model_name]['synaptic_input_variable_in'] + '+= synaptic_weight_in'
        )
        conn_in.connect()

        # Add generator and synapses to network
        net.add(stimulator_in)
        net.add(conn_in)
    
    # Define trace monitor
    state_variable_to_monitor = neuron_model[model_name]['state_variable_to_compare']
    tm = StateMonitor(neuron, state_variable_to_monitor, record=True)
    net.add(tm)

    # Run simulation
    net.run(neuron_model[model_name]['simulation_runtime'])

    # Return monitor data
    # TODO is there a better workaround for dynamic variable readout?
    r = {'tm' : tm}
    exec(f'data = tm.{state_variable_to_monitor}', r)

    return np.array([1,1])

    #return r['data']


@pytest.mark.parametrize('neuron_models', NEURON_MODEL_DEFINITIONS)
def test_voltage_trace(neuron_models):
    """
    This test compares if the voltage traces between a Brian2Lava
    and a pure Brian simulation are equal
    """

    # Brian2Lava simulation
    # NOTE
    # It is critical to first run lava as otherwise the name of the
    # neurongroup will be taken by the brian object and the name
    # for lava will be different and brian2lava device can not handle it
    # and will fail to retrieve any data since it will search for the
    # wrong name. Its weired but I dunno what is going on behind the scenes
    # and it is a brian problem I think.
    # Anyway this fix solves it.
    tm_lava = run_voltage_simulation(neuron_models, use_lava=True)

    # Pure Brian simulation
    tm_brian = run_voltage_simulation(neuron_models, use_lava=False)
    #tm_brian = tm_brian[0]  # for some reason brian will give a nested array

    # Compare results
    is_equal = np.array_equal(tm_brian, tm_lava)
    assert is_equal
