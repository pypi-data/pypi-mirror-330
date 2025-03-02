import brian2lava
from brian2 import set_device, get_device
import pytest
import os.path
import warnings


@pytest.fixture
def config():
    """
    Just a dummy fixture that may be redefined by fixtures or parametrization, if needed.
    Some items of the dictionary are set, for instance, in `use_lava_device_preset_mode`.
    """
    return {}

def use_lava_device(test_func):
    """
    A custom decorator for tests, initializing the device with flexible mode.
    """
    def set_lava_device(config):
        set_device('lava', hardware = 'CPU', mode = 'flexible')
        # The following is needed due to some magic bug in pytest for which the device has the 'has_been_run' attribute still set to 
        # True after running the previous test..
        device = get_device()
        device.reinit()
        device.activate(**device.build_options)
        test_func(config)

    return set_lava_device

def use_lava_device_preset_mode(test_func):
    """
    A custom decorator for tests, initializing the device with preset mode. The used hardware can be selected via the `config`
    fixture (default is 'CPU').
    """
    # To enable parametrization while keeping the function call generic, using a fixture named `config` which may be redefined.
    def set_lava_device(config):
        # Set hardware
        hardware = config.get('hardware')
        if hardware:
            config['hardware'] = hardware
        else:
            config['hardware'] = 'CPU'

        # Set number representation
        num_repr = config.get('num_repr')
        if num_repr:
            config['num_repr'] = num_repr
        else:
            config['num_repr'] = 'fixed'

        # Set models directory
        models_dir = config.get('models_dir')
        if models_dir is not None and os.path.exists(models_dir):
            config['models_dir'] = models_dir
        else:
            # For Loihi 2 hardware, external model repository has to be defined
            if config['hardware'].lower() == 'loihi2':
                warnings.warn("An existing models directory has to be set (via 'models_dir') when using Loihi 2 hardware. "
                              "Skipping this test.")
                pytest.skip("missing Loihi 2 configuration")
            # For CPU hardware, we can fall back to the standard models library
            elif models_dir is not None:
                warnings.warn("The models directory set via 'models_dir' could not be found. "
                              "Falling back to standard models directory.")
            # Set standard models directory
            config['models_dir'] = None

        # Set directory for other adapted Lava processes
        lava_proc_dir = config.get('lava_proc_dir')
        if lava_proc_dir is not None and os.path.exists(lava_proc_dir):
            config['lava_proc_dir'] = lava_proc_dir
            #print(f"FOUND 'lava_proc_dir = {lava_proc_dir}'")
        else:
            # For Loihi 2 hardware, external processes repository has to be defined
            if config['hardware'].lower() == 'loihi2':
                warnings.warn("An existing processes directory has to be set (via 'lava_proc_dir') when using Loihi 2 hardware. "
                              "Skipping this test.")
                pytest.skip("missing Loihi 2 configuration")
            # For CPU hardware, we can fall back to the standard processes library
            elif lava_proc_dir is not None:
                warnings.warn("The processes directory set via 'lava_proc_dir' could not be found. "
                              "Falling back to standard processes directory.")
            # Unset processes directory
            config['lava_proc_dir'] = None

        # Initialize the device
        set_device('lava', mode = 'preset', hardware = config['hardware'], num_repr = config['num_repr'], models_dir = config['models_dir'],
                   lava_proc_dir = config['lava_proc_dir'], use_f2f = False)

        # The following is needed due to some magic bug in pytest for which the device has the 'has_been_run' attribute still set to 
        # True after running the previous test..
        device = get_device()
        device.reinit()
        device.activate(**device.build_options)

        # Return the function definition
        test_func(config)

    return set_lava_device
