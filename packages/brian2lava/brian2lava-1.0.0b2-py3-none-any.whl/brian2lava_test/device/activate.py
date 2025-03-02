import numpy as np
import os
import shutil

from brian2.codegen.targets import *
from brian2.core.clocks import Clock
from brian2.core.preferences import prefs
from brian2.units import ms

from brian2lava_test.codegen.codeobject import LavaCodeObject
from enum import Enum
from brian2lava_test.utils.const import runtime_configs, HARDWARE
import importlib
from warnings import warn 
from brian2lava_test.utils.math import F2F
from brian2lava_test.preset_mode.model_loader import ModelLoader


def activate(self, **kwargs):
    """
    Activates Brian2Lava device.

    The method adds the `LavaCodeObject` as code generation target
    """
    # Log that activate method was called
    self.logger.debug("Activating Lava device.")

    # Log used device and code object
    self.logger.debug(f'Using code object class: {self.code_object_class().__name__} with Device: {self}')

    # Find the selected hardware in the enumeration class of available hardware, and 
    # let device know which hardware is used (small overhead for case insensitivity)
    selected_hardware = kwargs.get('hardware', '').lower()
    self.hardware = None
    for available_hw_name in HARDWARE.get_names():
        if selected_hardware == available_hw_name.lower():
            self.hardware = getattr(HARDWARE, available_hw_name)
            break
    if not self.hardware:
        # Default: CPU
        self.hardware = HARDWARE.CPU

    # Let device know which model mode is used (small overhead for case insensitivity)
    self.mode = kwargs.get('mode', '').lower()    
    if not self.mode:
        # Default for CPU backend: flexible mode
        if self.hardware == HARDWARE.CPU:
            self.mode = 'flexible'
        # Default for Loihi2 backend: preset mode (Loihi2 only supports this)
        elif self.hardware == HARDWARE.Loihi2:
            self.mode = 'preset'

    # Let device know which number representation is used (small overhead for case insensitivity)
    self.num_repr = kwargs.get('num_repr', '').lower()
    if not self.num_repr:
        # Default for flexible mode: floating-point representation
        if self.mode == 'flexible':
            self.num_repr = 'float'
        # Default for preset mode: fixed point representation (Loihi2 only supports this)
        elif self.mode == 'preset':
            self.num_repr = 'fixed'

    # Let device know whether to use F2F translation or not (if not, all values should be integers)
    self.use_f2f = kwargs.get('use_f2f', False)

    # Places to account for when converting to fixed point (first use binary accuracy if provided, 
    # then use decimal accuracy if provided)
    if kwargs.get('binary_accuracy') is not None:
        F2F.set_binary_accuracy(int(kwargs.get('binary_accuracy')))
    elif kwargs.get('decimal_accuracy') is not None:
        F2F.set_decimal_accuracy(int(kwargs.get('decimal_accuracy')))
    else:
        F2F.set_binary_accuracy(0)
        
    # Set the runtime configuration for this hardware
    # Raises an exception if the user has selected an unsupported mode or unsupported hardware
    try:
        self.runtime_config, self.runtime_tag = runtime_configs[(self.mode, self.hardware, self.num_repr)]
    except KeyError:
        raise NotImplementedError(f"The selected combination of model mode/hardware/number representation " +
                                  f"'({self.mode}, {self.hardware}, {self.num_repr})' is not implemented (yet). " +
                                  f"The available combinations are: {list(runtime_configs.keys())}. Choices are "+
                                  f"case-insensitive but correct spelling is required.")
    # Set codegen targets
    if self.mode == 'flexible':
        prefs.codegen.target = 'lava'
        prefs.codegen.string_expression_target = 'lava'
        
    # For Loihi2 we use the runtime configuration. This is because we want 
    # to use Brian2 to execute code and define variables before runtime.
    # These variables can then be fed to the Lava process as kwargs.
    # For more info see Release Notes for the first Loihi release.
    elif self.mode == 'preset':
        prefs.codegen.target = 'numpy'
        prefs.codegen.string_expression_target = 'numpy'

        if kwargs.get('models_path'):
            raise ValueError("The argument 'models_path' has been deprecated, please use 'models_dir' instead")
        
        # Read models from package and from user defined path; tell if a list of the models should be printed
        ModelLoader.read_models(self, kwargs.get('models_dir', None), kwargs.get('models_print', True))

    # Create the workspace directory
    project_path = kwargs.get('models_path','')
    self.set_project_directory(project_path)

    # Call parent activate function
    self.super.activate(**kwargs)


def seed(self, seed=None):
    """
    Set the seed for the random number generator.

    Parameters
    ----------
    seed : int, optional
        The seed value for the random number generator, or ``None`` (the default) to set a random seed.
    """
    np.random.seed(seed)
    self.rand_buffer_index[:] = 0
    self.randn_buffer_index[:] = 0


def reinit(self):
    """
    Reinitializes the device, which is necessary if multiple `run()` calls
    are performed within a single script.

    *   Initialize device and call parent's `reinit`
    *   Reset `did_run` flag 
    *   Set network schedule and 'build_on_run' flag to previously chosen values
    """
    # Store network schedule and 'build_on_run' flag
    tmp_network_schedule = self.network_schedule
    build_on_run = self.build_on_run
    build_options = self.build_options

    # Remove any reference to previously imported modules
    importlib.invalidate_caches()
    pycache_directory = os.path.join(self.project_dir,'__pycache__')
    if os.path.exists(pycache_directory):
        shutil.rmtree(pycache_directory)
    self.logger.debug("Cleaned cache for new session")


    # Initialize the device
    self.__init__()

    # Set network schedule and 'build_on_run' flag to previously chosen values
    self.network_schedule = tmp_network_schedule
    self.build_on_run = build_on_run
    self.build_options = build_options