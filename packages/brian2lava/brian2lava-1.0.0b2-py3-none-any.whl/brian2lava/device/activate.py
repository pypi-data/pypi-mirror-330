import numpy as np
import os
import shutil

from brian2.codegen.targets import *

import importlib
from brian2lava.preset_mode.handler import PresetProcessHandler
from brian2lava.preset_mode.lava_parameters import LavaParameters
from brian2lava.utils.settings_parser import SettingsParser
import sys


def activate(self, **kwargs):
    """
    Activates Brian2Lava ('lava') device.
    The method adds the ``LavaCodeObject`` as code generation target, if this is requested (by setting
    ``mode='flexible'``).
    Call with ``**kwargs = **device.build_options`` to reinstate the original build options from the
    ``set_device`` call.

    Parameters
    ----------
    kwargs : `dict`
        Dictionary of keyword arguments.
    """
    # Log that activate method was called
    self.logger.debug("Activating Lava device.")

    # Log used device and code object (CAUTION: this causes the initialization of a code object and can
    # thereby elicit unnecessary warnings from Cython, for instance)
    #self.logger.debug(f'Using code object class: {self.code_object_class().__name__} with Device: {self}')

    # Parse and set settings
    parser = SettingsParser(self)
    parser.parse_settings(kwargs)
    parser.apply_settings()

    # Call parent activate function
    self.super.activate(**kwargs)


def seed(self, seed=None):
    """
    Set the seed for the random number generator.

    Parameters
    ----------
    seed : `int`, optional
        The seed value for the random number generator, or ``None`` (the default) to set a random seed.
    """
    np.random.seed(seed)
    self.rand_buffer_index[:] = 0
    self.randn_buffer_index[:] = 0


def reinit(self):
    """
    Reinitializes the device, which is necessary if multiple ``run()`` calls
    are performed within a single script. The main steps are:

    *   initialize device and call parent's ``reinit()`` method,
    *   reset ``did_run`` flag.
    *   set network schedule and ``build_on_run`` flag to previously chosen values.
    """
    # Store network schedule and 'build_on_run' flag
    tmp_network_schedule = self.network_schedule
    build_on_run = self.build_on_run
    build_options = self.build_options

    # It's essential to remove previously cached modules in the workspace folder,
    # this only causes errors when reinitializing the device.
    project_dir_module = os.path.basename(self.project_dir)
    module_names = list(sys.modules.keys())
    for module_name in module_names:
        if module_name.startswith(project_dir_module) and not module_name == project_dir_module:
            self.logger.diagnostic(f"Removing modules from cache at reinit {module_name}")
            sys.modules.pop(module_name)
    
    # Just for extra safety: clear importlib and py caches
    importlib.invalidate_caches()
    pycache_directory = os.path.join(self.project_dir, '__pycache__')
    if os.path.exists(pycache_directory):
        shutil.rmtree(pycache_directory)
    self.logger.debug("Cleaned cache for new session")

    # Reset the copy flag for the additional Lava processes directory
    PresetProcessHandler.copied_lava_proc_files = False

    if self.is_using_f2f():
        self.f2f.reset()

    # Empty the dicts stored in the static class LavaParameters
    LavaParameters.reset()
    
    # Initialize the device (which also resets `did_run`)
    self.__init__()

    # Set network schedule and 'build_on_run' flag to previously chosen values
    self.network_schedule = tmp_network_schedule
    self.build_on_run = build_on_run
    self.build_options = build_options
