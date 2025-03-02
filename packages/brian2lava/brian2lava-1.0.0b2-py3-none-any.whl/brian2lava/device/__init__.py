import jinja2
import os
import shutil
import numpy as np
from collections import defaultdict

# Import Brian2 modules
from brian2.devices.device import all_devices, Device
from brian2.utils.logger import get_logger
from brian2lava.utils.writer import PyWriter
from weakref import WeakKeyDictionary
import sys

__all__ = ['LavaDevice']


class LavaDevice(Device):
    """
    This Lava device class for Brian 2 combines most of the functionality of Brian2Lava. It activates
    the Brian 2 device, transforms all variables (to and from Lava), builds and executes the generated
    Lava code.

    In 'flexible' mode, the generation of Lava Python code based on the abstract code from Brian
    is performed mostly in ``LavaCodeGenerator`` and partly in ``LavaCodeObject``, however, also
    the ``code_object`` method within this ``LavaDevice`` class takes part in generating Lava code.

    The ``LavaDevice`` class is split into several files. The code of the different files is included
    into the class via the given import statements.
    """
    
    def __init__(self):

        #print("Initializing LavaDevice...")
        super(LavaDevice, self).__init__()

        # BRIAN SPECIFIC DEVICE SETUP -------------------------
        # Make logger available to all methods in this class
        self.logger = get_logger('brian2.devices.lava')

        # FIXME Defines the network schedule, if None, the user can choose the schedule
        self.network_schedule = None
        # NOTE Brian2Loihi used: ['start', 'synapses', 'groups', 'thresholds',  'resets', 'end']

        # Random number buffer
        self.randn_buffer_index = np.zeros(1, dtype=np.int32)
        self.rand_buffer_index = np.zeros(1, dtype=np.int32)

        # Predefines a default clock, which will be set inside the `activate` method
        self.defaultclock = None

        # Define an empty set to store clocks
        self.clocks = set([])

        # DIRECTORY MANAGEMENT ---------------------------------------
        self.package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # The project dir is fixed in the Lava device. This is important, since a reinit
        # otherwise doesn't know which directory to clean. The directory will be set by the
        # settings parser via the `set_project_directory()` method.
        self.project_dir = None
        
        # Instantiate python file writer
        self.writer = PyWriter()

        # CODEOBJECT AND VARIABLE MANAGEMENT ----------------------------------------------
        # Stores weak references from a `Variable` objects to the containing value(s)
        # Methods to handle the arrays are provided in `arrays.py`
        self.arrays = WeakKeyDictionary()
        self.proc_init_queue = defaultdict(list) # In CPP device 'main_queue' a list, but we need a queue for each process
        self.proc_model_add_code = defaultdict(set) # Additional code for process models. Defaults to set to avoid duplicates, ordering shouldn't matter.

        # Stores names of indices that are used to initialize variables
        # e.g. _group_idx_1_v, _group_idx_2_ge, etc.
        self.set_variable_index_names = []

        # Define empty dicts to store code objects and abstract code
        self.code_objects = {}

        # Brian network objects
        self.net_objects = set()

        # Store Lava variables
        # Key: variable name, Value: variable definition (e.g. 'np.empty(...)')
        self.lava_variables = {}
        
        # Store the ports required to connect processes
        self.spike_queues = {}
        self.lava_ports = {}

        # Brian template functions that belong to the process,
        # instead of the process model, e.g. 'group_variable_set'
        self.init_template_functions = [
            'group_variable_set',
            'group_variable_set_conditional',
            'synapses_create_generator',
            'synapses_create_array'
        ]

        # SUPPORTED OBJECTS AND HARDWARE ----------------------------
        # Variables that represent our current support for generated processes
        from brian2 import SpikeGeneratorGroup, NeuronGroup, Synapses, PoissonGroup
        from brian2 import PoissonInput, PopulationRateMonitor, SpatialNeuron
        from brian2.synapses.synapses import SummedVariableUpdater
        all_objects = set([SpikeGeneratorGroup,NeuronGroup,Synapses,PoissonGroup,PoissonInput,PopulationRateMonitor,
                         SpatialNeuron,SummedVariableUpdater])
        # Here we only list those BrianObjects that would require generating a Lava Process, so it's not indicative
        # of the full scope of our current supported features.
        self.supported_processes = {
            'flexible' : {NeuronGroup,
                          Synapses,
                          SpikeGeneratorGroup,
                          PoissonGroup},
            'preset'   : {NeuronGroup,
                          Synapses,
                          SpikeGeneratorGroup
                          }
        }
        # Use set algebra to determine the unsupported processes
        self.unsupported_processes = {mode: all_objects - processes for mode,processes in self.supported_processes.items()}

        # Set the runtime configuration and tag used to run the simulation in Lava (done in activate.py)
        self.runtime_config = None
        self.runtime_tag = None

        # MONITORS---------------------------------------------
        # NOTE Some variables shall be probed only once by Lava, but are required
        #      for different Brian monitors, e.g. time
        self.lava_variables_to_monitor = set()
        self.lava_monitors = {}
        # Add monitors for additional variables (only for SpikeMonitors)
        self.additional_monitors = {}
        #self.brian_monitors = {}

        # Variable indicating if the network did run before.
        # This is needed because previously run objects can cause unwanted behavior.
        # Calling the methods `device.reinit()` and `device.activate()`` will run the
        # whole build process again.
        self.did_run = False

        # Add super to self to make it available in sub-files
        self.super = super(LavaDevice, self)

        self.cleanup_tmp_dirs()
        #print("Initialized LavaDevice.")
    
    def cleanup_tmp_dirs(self):
        # Cleanup any tmp folder that might have been created previously by StateProbes
        # TODO: If tmp folder problem gets fixed in lava this should be changed
        tmp_folder = os.path.join(os.getcwd(), 'tmp')
        if os.path.exists(tmp_folder):
            shutil.rmtree(tmp_folder)
    
    def is_using_f2f(self):
        """
        Simple boolean flag function to make the code more readable and less
        error prone.

        Returns
        -------
        `bool`
            ``True if F2F is used, ``False`` if not.
        """
        return self.num_repr == 'fixed' and self.f2f
    
    def set_project_directory(self, dir_path = ''):
        """
        Create the directory to which all the generated files will be written.
        By default this is a directory named 'lava_workspace' in the current working
        directory.

        Parameters
        ----------
        dir_path : `str`, optional
            The root path of the intended project directory. 
            If ``None``, the current working directory will be used.
        """
        dir_full_path = os.getcwd() if dir_path == '' else dir_path
        # Set the new workspace directory
        project_dir_new = os.path.join(dir_full_path, 'lava_workspace')
        self.logger.debug(f"Changing project directory from '{self.project_dir}' "
                          f"to '{project_dir_new}'")
        self.project_dir = project_dir_new
        
        # Update the project directory of the writer, too.
        self.writer.set_project_directory(self.project_dir)

        # Clear the contents of the workspace if it already existed and create it anew
        if os.path.exists(self.project_dir):
            shutil.rmtree(self.project_dir)
        os.makedirs(self.project_dir)

        # In order to properly run simulations, we need to import classes
        # from files stored in the project directory.
        # Put it at the first place in the path so we avoid possible naming conflicts.
        if not dir_full_path in sys.path:
            sys.path.insert(0, dir_full_path)

        # Create an __init__ file so that this folder is treated like a package
        init_path = os.path.join(self.project_dir,'__init__.py')
        if not os.path.exists(init_path):
            with open(init_path,'w') as f:
                pass
    

    # DIRECTORY ORGANIZATION WITH LIST OF ALL DEVICE METHODS-------------------------------
    # Device activation
    from .activate import (
        activate, seed, reinit
    )

    # Build the network
    from .build import (
        build, render_templates, get_compiled_code, get_jinja_environment,
        get_lava_proc_variables, get_lava_proc_model_variables, get_single_process_and_kwargs,
        get_processes_and_kwargs,
        get_lava_function_calls, get_lava_ports_definitions, generate_init_queue,
        generate_additional_code, get_proc_model_init_code, get_lrn_guard_code
    )

    # Writer for writing rendered templates
    from .writer import (
        prepare_directory, write_templates
    )

    # Define code objects
    from .codeobject import (
        code_object, code_object_flexible, code_object_preset
    )

    # Run the network
    from .run import (
        network_run,
        run_processes,
        set_brian_monitor_values,
        init_lava_monitors,
        connect_lava_ports,
        connect_lava_ports_flexible,
        connect_lava_ports_preset,
        select_root_processes,
        instantiate_processes,
        get_state_probe_values,
        get_monitor_values,
        update_brian_class_attributes
    )

    # Handle storage
    from .arrays import (
        add_array, get_value, get_array_name, init_with_zeros,
        init_with_arange, fill_with_array,
        get_monitor_var_name, resize, add_monitor_var, set_array_data
    )

    # Handle setter and getter for variables
    from .variables import (
        variableview_set_with_index_array,
        variableview_set_with_expression,
        variableview_set_with_expression_conditional
    )

    # Handle synapses
    from .synapses import (
        synapses_connect,
        spike_queue,
        determine_lava_ports,
        _add_spiking_synapses_vars
    )


# Initialize `LavaDevice` object and add it to the global `all_devices` list
# to make it available to Brian 2
lava_device = LavaDevice()
all_devices['lava'] = lava_device
