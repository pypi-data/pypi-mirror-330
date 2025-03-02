import os
import importlib
import numpy as np

from brian2.core.namespace import get_local_namespace
from brian2.groups.neurongroup import NeuronGroup, StateUpdater
from brian2.synapses.synapses import Synapses
from brian2.input.spikegeneratorgroup import SpikeGeneratorGroup
from brian2.units import second
from brian2 import StateMonitor,SpikeMonitor

from lava.magma.core.run_conditions import RunSteps

from brian2lava.utils.files import get_module_name
from brian2lava.utils.f2f import ModelWiseF2F as F2F
from brian2lava.utils.math import dense_to_sparse
from brian2lava.utils.utils import mode_dependent, make_runtime_config_map
from brian2lava.utils.const import HARDWARE
from brian2lava.utils.monitors import init_monitor
from brian2lava.preset_mode.lava_parameters import LavaParameters

def network_run(
        self,
        net,
        duration,
        report=None,
        report_period=10 * second,
        namespace=None,
        profile=False,
        level=0,
        **kwds
    ):
    """
    Performs first preparations and checks, assembles the list of Lava objects to be generated,
    and finally calls the ``build()`` method of the device.

    Overwrites the ``run()`` method from ``brian2.core.Network.run()``. For reference, see:
    https://brian2.readthedocs.io/en/stable/reference/brian2.core.network.Network.html#brian2.core.network.Network.run

    Note that in the current implementation, the following arguments are not supported and will thus be ignored or raise an error:

        - report -> ignored
        - report_period -> ignored
        - profile -> error

    Parameters
    ----------
    net : `Network`
        The Brian network object.
    duration : `Value`
        The duration of this run (with time unit).
    report : `str`, optional
        The report type (currently not supported by Brian2Lava).
    report_period : `Value`, optional
        Brian value specifying the reporting period (currently not supported by Brian2Lava).
    namespace : `any`, optional
        The local namespace.
    profile : `bool`, optional
        Flag for profiling (currently not supported by Brian2Lava).
    level : `int`, optional
        The local namespace level.
    kwds : dict, optional
        Further keyword arguments (currently not supported by Brian2Lava).
    """
    # Before doing anything check that the objects used by the user 
    # are supported by Lava/Brian2Lava.
    check_for_brian2lava_support(net)
    
    # Store duration in device
    self.duration = duration
    
    # Log that the network run method was called
    self.logger.diagnostic("Network run is executing.")
    
    # If keyword arguments are given, notify the user that these arguments are not used in Brian2Lava
    if kwds:
        self.logger.warn(
            'Unsupported keyword argument(s) provided for run: {}'.format(', '.join(kwds.keys()))
        )
        
    # FIXME Show an error if user enabled profiling, since it is not supported
    if profile is True:
        raise NotImplementedError('Brian2Lava does not yet support detailed profiling.')
    
    # FIXME Set clocks
    net._clocks = {obj.clock for obj in net.sorted_objects}
    t_end = net.t+duration
    for clock in net._clocks:
        clock.set_interval(net.t, t_end)
    
    # Manage Spike Queues. TODO: Move this in a better place if possible
    # For now I put it here because I want this to happen as soon as possible during the
    # run call. (But still after any variable definition has been made (e.g. setting delays.))
    for obj in net.sorted_objects:
        if isinstance(obj,Synapses):
            for pathway in obj._pathways:
                # The spike queue is only added if delays are defined.
                has_spike_queue = False
                try:
                    if len(pathway._delays.get_value()):
                        has_spike_queue = True
                # The device will raise this error if the delay variable was modified 
                # and requires to be manipulated during runtime (e.g. S.delays = 'expression').
                except NotImplementedError:
                    has_spike_queue = True
                                
                if has_spike_queue:
                    spike_queue = f'{obj.name}_{pathway.objname}_spike_queue'
                    # In case no delay was specified, we use an empty array
                    delays = self.get_array_name(pathway._delays)
                    self.spike_queues[spike_queue] = {
                        'name' : 'self.'+spike_queue,
                        'delays': delays,
                        'dt': str(pathway.source.clock.dt_),
                        'sources': self.get_array_name(pathway.synapse_sources),
                        'start': pathway.source.start,
                        'stop': pathway.source.stop,
                        'owner': obj
                    }
    
    # Get the local namespace, if no namespace was given
    if namespace is None:
        namespace = get_local_namespace(level=level+2)

    # Set default integration method for neuron groups, if in preset mode
    # This has no real effect except avoiding to print a warning. (I'm 95% sure)
    if self.mode == 'preset':
        for obj in net.sorted_objects:
            if isinstance(obj, NeuronGroup):
                # Overwrite method in neuron group
                obj.method_choice = 'euler'
                for co in obj.contained_objects:
                    if isinstance(co, StateUpdater):
                        # Overwrite method in related state updater
                        co.method_choice = 'euler'
                        co.method_options = None

    # Call before_run with namespace
    net.before_run(namespace)
    
    # Update device clocks by network clocks
    self.clocks.update(net._clocks)
    if len(self.clocks) > 1:
        raise NotImplementedError("Multiple clocks are currently not supported by Brian2Lava.")
    
    # Set current time to end time (FIXME why? and whyt is the difference between self.t and self.t_?)
    # NOTE by carlo: self.t is with unit, self.t_ is without unit
    net.t_ = float(t_end)
    
    # FIXME Taken from CPPStandaloneDevice, but unclear what it means
    # In the CPP device it is noted that this is a hack
    # https://github.com/brian-team/brian2/blob/master/brian2/devices/cpp_standalone/device.py#L1404
    for clock in self.clocks:
        if clock.name == 'clock':
            clock._name = '_clock'
    
    # Collect code objects in general, and objects to generate Lava processes, from network objects.
    code_objects = []
    self.lava_objects = {}
    self.logger.diagnostic(f"net.sorted_objects = {net.sorted_objects}")
    for obj in net.sorted_objects:
        if obj.active:
            # Only the objects that generate a Lava process are added to the `lava_objects` dict 
            # (so we avoid children of objects like `StateUpdater` and so on).
            if any([isinstance(obj, supp_obj) for supp_obj in self.supported_processes[self.mode]]):
                self.lava_objects[obj.name] = obj
            for codeobj in obj._code_objects:
                # NOTE: For code cleanup, this is never actually used anywhere. Interesting that they save the objects as tuples of (clock,object)
                code_objects.append((obj.clock, codeobj))
    
    self.logger.debug(f"lava_objects = {self.lava_objects}")
    self.logger.diagnostic(f"code_objects = {code_objects}")

    # FIXME This may require an update, similar to how CPPStandalone handles the report
    # https://github.com/brian-team/brian2/blob/master/brian2/devices/cpp_standalone/device.py#L1465
    #if report is not None:
    #    report_period = float(report_period)
    #    next_report_time = start_time + report_period
    #    if report == 'text' or report == 'stdout':
    #        report_callback = TextReport(sys.stdout)
    #    elif report == 'stderr':
    #        report_callback = TextReport(sys.stderr)
    #    elif isinstance(report, str):
    #        raise ValueError(f'Do not know how to handle report argument "{report}".')
    #    elif callable(report):
    #        report_callback = report
    #    else:
    #        raise TypeError(f"Do not know how to handle report argument, "
    #                        f"it has to be one of 'text', 'stdout', "
    #                        f"'stderr', or a callable function/object, "
    #                        f"but it is of type {type(report)}")
    #    report_callback(0*second, 0.0, t_start, duration)

    # TODO? At least in the CPPStandaloneDevice, there is some more code here,
    # that seems to generate some basic code lines ...

    # Call network after_run method
    net.after_run()

    # Call build method
    if self.build_on_run:
        if self.did_run: # Building a network with previously run objects still in it can cause unwanted behavior
            raise RuntimeError("The network has already been built and run "
                               "before. Use `set_device` with "
                               "`build_on_run=False` and an explicit "
                               "`device.build` call to use multiple `run` "
                               "statements with this device.")
        self.build(direct_call=False)


def check_for_brian2lava_support(net):
    """
    Checks that the objects defined by the user are supported by Brian2Lava.
    If it's not the case, throws ``NotImplementedError``.

    Parameters
    ----------
    net : `brian2.network.Network`
        The Brian network object.
    """
    from brian2 import get_device, Synapses
    device = get_device()
    # Raise an error if the user is trying to implement unsupported objects
    objects = []
    mode = device.mode
    for obj in net.sorted_objects:
        # Make a list of the unsupported objects present in the network (if any)
        if any([isinstance(obj,unsupp_obj) for unsupp_obj in device.unsupported_processes[mode]]):
            obj_type = type(obj).__name__
            objects.append(obj_type)
        for contained_obj in obj.contained_objects:
            if any([isinstance(contained_obj,unsupp_obj) for unsupp_obj in device.unsupported_processes[mode]]):
                obj_type = type(contained_obj).__name__
                objects.append(obj_type)
        
        # Check that no (event-driven) equations are defined in synapses, since these are not good for brian2lava.
        if isinstance(obj,Synapses):
            if obj.event_driven is not None:
                device.logger.warn(
                    """Using the (event-driven) specifier in synaptic models will most likely lead to 
                    unwanted behavior, because event-driven effects in lava are handled at the END of a timestep 
                    (so after synapses have already propagated the incoming signals).
                    This is due to the intrinsic asynchronicity present in Lava and particularly in neuromorphic hardware. 
                    For this reason, we recommend using the (clock-driven) specifier instead.
                    """
                )
        
    if len(objects):
        objects_repr = '\n\t\t'.join(objects)
        msg = (f"The following objects or functionalities are not yet supported by Brian2Lava "
               f"(in '{device.mode}' mode):\n"
               f"    {objects_repr}\n"
               "You can expect them in future releases. You might also want to visit the "
               "official Brian2Lava repo on GitLab: "
               "https://gitlab.com/brian2lava/brian2lava/-/tree/main")
        raise NotImplementedError(msg)
        

def instantiate_processes(self, process_objects, process_kwargs = None):
    """
    Imports the rendered templates (in flexible mode) or the predefined modules (in preset mode),
    instantiates Lava processes, and returns a dictionary containing the instantiated processes.

    Parameters
    ----------
    process_objects : list of `Network`
        Network objects that will be related to Lava processes.
    process_kwargs : dict of dict of `any`
        A dictionary of dictionaries containing keyword arguments for each network object; definition of the "class_name" key is required.
    
    Returns
    -------
    instantiated_processes : dict of `AbstractProcess`
        The instatianted Lava processes.
    runtime_exception_map : `dict`
        Exceptions to the runtime tag (Lava structure for Loihi 2).
    """
    if process_kwargs is None:
        raise ValueError('process_kwargs argument should at least contain a dictionary for each object with the "class_name" key defined.')

    # Exceptions to the runtime tag are stored here
    runtime_exception_map = {}

    instantiated_processes = {}
    for obj in process_objects:
        # Name of the Brian object
        name = obj.name

        # Only for Loihi hardware, we have to instantiate an additional adapter process to send the spikes to the chip
        if isinstance(obj, SpikeGeneratorGroup) and self.hardware == HARDWARE.Loihi2:
            # Pop the dictionary entries to avoid TypeError for unexpected arguments later
            adapter_module = process_kwargs[name].pop('adapter_module')
            adapter_class_name = process_kwargs[name].pop('adapter_class')
            module = importlib.import_module(adapter_module)
            adapter_class = getattr(module,adapter_class_name)
            adapter_name = name + '_adapter'
            instantiated_processes[adapter_name] = adapter_class(shape = (process_kwargs[name]['data'].shape[0],))
            instantiated_processes[adapter_name].name = adapter_name
        
        # Import the module that contains the required Lava process.
        # In flexible mode, we enforce folder scrap to find the generated files.
        module_to_import = get_module_name(obj, self, name, force_scrap=(self.mode == 'flexible'))
        module = importlib.import_module(module_to_import)

        # It's crucial to reload the module in case the device has been reinitialized with `device.reinit()`,
        # otherwise, previously cached simulation classes could be used instead of the newly generated ones.
        # This only applies to flexible mode, where each process possesses its own module. In preset mode, 
        # importing previously imported models would cause an error.
        if self.mode == 'flexible':
            importlib.reload(module)

        # Get the process class from the module
        class_name = process_kwargs[name].pop('class_name')
        process_class = getattr(module, class_name)

        # Output for debugging
        self.logger.debug(f"Initializing process '{name}' of class '{class_name}' "
                          f"from module '{module_to_import}'.")
        arg_log = ""''""
        for k,v in process_kwargs[name].items():
            arg_log += f"{' '*8}{k} = {v}\n"
        if 'weights' in process_kwargs[name].keys():
            arg_log += f"{' '*8}weights.shape = {process_kwargs[name]['weights'].shape}"
        self.logger.debug(f"Arguments for process '{name}':\n{arg_log}")

        # Instantiate the process and add it to the compiled processes (already add the process name to be available
        # in process model constructors - unless we consider a SpikeGeneratorGroup, where we have to do this later)
        if not isinstance(obj, SpikeGeneratorGroup):
            # Alternative:
            #   process_kwargs[name].update({'name' : name})
            instantiated_processes[name] = process_class(**process_kwargs.get(name, {}), name = name)
        else:
            instantiated_processes[name] = process_class(**process_kwargs.get(name, {}))
            instantiated_processes[name].name = name

        # Update `runtime_exception_map`
        runtime_exception_map.update(make_runtime_config_map(obj,
                                                             instantiated_processes[name],
                                                             self.hardware,
                                                             self.mode,
                                                             self.num_repr,
                                                             self.use_exp_array))

    return instantiated_processes, runtime_exception_map


def run_processes(self, process_kwargs = {}):
    """
    Executes the Lava simulation.
    We first instantiate the Lava processes and add configured monitors. Next, we 
    select the root process(es) and run the simulation. Finally, we extract the 
    monitor data and update the values of Brian objects.

    Parameters
    ----------
    process_kwargs : dict of dict of ``any``
        A dictionary of dictionaries containing keyword arguments for each network object; definition of the "class_name" key is required.
    """
    # Retrieve dict of instantiated processes, as well as exception map
    processes, exception_map = self.instantiate_processes([obj for obj in self.lava_objects.values()],
                                                          process_kwargs = process_kwargs)

    # NOTE adding one step is necessary such that spikes are evaluated
    #      correctly by Lava and match Brian results
    num_steps = int(self.duration/self.defaultclock.dt)

    # Dict of lists of StateProbe objects to be passed to the runtime config for callback
    probe_objects = {}
                
    # Initialize state probes for every process and store the StateProbe objects in a dictionary
    for process in processes.values():
        probe_objects[process.name] = self.init_lava_monitors(process, num_steps)

    # Connect the ports of connected processes
    self.connect_lava_ports(processes)

    # Select the root process(es) and related probes
    root_processes, subnetwork_probes = self.select_root_processes(processes, probe_objects)
    self.logger.debug(f"Root process(es): {root_processes}")

    # Log and print that the run method was called
    msg = f'Running Lava simulation for {self.duration} ({num_steps} steps)'
    self.logger.info(msg)
    
    # Run the simulation
    for process, probes in zip(root_processes, subnetwork_probes):
        self.logger.debug(f"Running process: {process.name}, {type(process)}")
        # Prepare runtime configuration; add possible state probe callbacks if Loihi 2 is used
        if self.hardware == HARDWARE.Loihi2:
            run_cfg = self.runtime_config(select_tag = self.runtime_tag, exception_proc_model_map = exception_map, callback_fxs=probes)
        else:
            run_cfg = self.runtime_config(select_tag = self.runtime_tag, exception_proc_model_map = exception_map)
        process.run(condition=RunSteps(num_steps=num_steps), run_cfg=run_cfg)
    self.logger.debug("Successfully run simulation")

    # After running the simulation, transfer the monitored values from the Lava processes to Brian monitors.
    msg = "Retrieving monitor values"
    self.logger.info(msg)
    for process in processes.values():
        # Set monitor values
        self.set_brian_monitor_values(process)
    self.logger.info("Successfully retrieved monitor values")

    # Update the class attributes of BrianObjects, so that the user can get their values in the usual way.
    if not self.variable_updating_disabled:
        msg = "Updating Brian variables"
        self.logger.info(msg)
        self.update_brian_class_attributes(processes)
        self.logger.info("Successfully updated Brian variables")

    # Stop processes to terminate execution
    for process in root_processes:
        process.stop()

    # Indicate that the network simulation did run
    self.did_run = True

    for process in processes.values():
        del process
    
    self.cleanup_tmp_dirs()


@mode_dependent
def connect_lava_ports(self, processes):
    """
    This is just a dummy function, the real implementations are given below.
    """
    raise NotImplementedError()


def connect_lava_ports_flexible(self, processes):
    """
    Connect the ports of the connected processes.

    Parameters
    ----------
    processes : dict of `AbstractProcess`
        Dictionary of instantiated Lava processes.
    """

    for var in self.lava_ports.values():
        portname = var['portname']
        pathway = var['pathway']

        # First connect the spiking sources to the synapses
        source = processes[var['sender']]
        synapses = processes[pathway.synapses.name]

        # To avoid the DuplicateConnection error from Lava
        syn_spikes_in = synapses.in_ports._members['s_in_' + pathway.prepost]
        # Only reshape the spike port once
        if syn_spikes_in.size == 0:
            # Here we shape the InPort of synapses to accomodate the spikes
            neur_spike_port = processes[source.name].out_ports._members[source.name + '_s_out']
            syn_spikes_in.shape = neur_spike_port.shape
            # Connect the spike ports
            neur_spike_port.connect(syn_spikes_in)
            self.logger.debug(f"Connected spiking source '{source.name}' to synapses object '{synapses.name}'.")

        # Then connect the synapses to the neurons, here we only require the name
        target = var['receiver']

        # Again, first reshape the ports as needed
        # TODO: not sure this is the intended use of the _members attribute of the Collection class:
        # https://github.com/lava-nc/lava/blob/4283428c3dda02ea6c326d5660a952cafcdd2c03/src/lava/magma/core/process/process.py
        syn_out_port = processes[synapses.name].out_ports._members[portname + '_out']
        neur_in_port = processes[target].in_ports._members[portname + '_in']

        # Reshape the input port of the neuron 
        neur_in_port.shape = syn_out_port.shape
        # Connect the port
        syn_out_port.connect(neur_in_port)

        self.logger.debug(f"Connected '{portname}' of '{synapses.name}' to target neuron '{target}'.")
    
def connect_lava_ports_preset(self, processes):
    """
    Connect the lava ports for the preset mode implementation. The mechanisms are similar to the ones
    in `connect_lava_ports_flexible`.

    Parameters
    ----------
    processes : dict of `AbstractProcess`
        Dictionary of instantiated Lava processes.
    """
    for port_var in self.lava_ports.values():
        pathway = port_var['pathway']

        # First connect the spiking sources to the synapses
        source = processes[port_var['sender']]
        target = processes[port_var['receiver']]
        synapses = processes[pathway.synapses.name]

        # We have to account for the presence of adapters in case we're using a SpikeGenerator.
        # Since the port naming convention is not consistent in this case, we have to hard code these statements.
        if 'adapter' in target.name:
            # Connect the spike generator output to the adapter input
            source.s_out.connect(target.inp)
            self.logger.debug(f"Connected '{source.name}' to intermediate adapter '{target.name}'.")
            continue

        # Diagnostic output of main properties
        self.logger.diagnostic(f"source.name = {source.name}")
        if not 'adapter' in source.name:
            self.logger.diagnostic(f"source.s_out.shape = {source.s_out.shape}")
        self.logger.diagnostic(f"synapses.name = {synapses.name}")
        self.logger.diagnostic(f"synapses.s_in.shape = {synapses.s_in.shape}")
        self.logger.diagnostic(f"synapses.a_out.shape = {synapses.a_out.shape}")
        self.logger.diagnostic(f"target.name = {target.name}")
        self.logger.diagnostic(f"target.a_in.shape = {target.a_in.shape}")

        # Connect the spike output of the source object to the input of the synapses object.
        if not 'adapter' in source.name:
            source.s_out.connect(synapses.s_in)
        else:
            # Resize the adapter to have a shape compatible with the synapses object.
            source.shape = synapses.s_in.shape
            source.out.connect(synapses.s_in)

        # Connect the activations from the synapses to the target neuron group
        synapses.a_out.connect(target.a_in)
        self.logger.debug(f"Connected spiking source '{source.name}' to receiver '{target.name}' through synapses object '{synapses.name}'.")
        

def select_root_processes(self, processes, probes):
    """
    This is a helper function to determine which processes to run, in order to avoid running 
    processes connnected to each other twice. Lava automatically runs connected processes together,
    so if we have A-->B-->C we only need to run A.
    This function selects one node from each isolated subnetwork in the ``lava_ports`` dictionary through
    a breadth-first search algorithm.

    Parameters
    ----------
    processes : dict of `AbstractProcess`
        A list of the initialized processes in the simulation.

    Returns
    -------
    list of `AbstractProcess`
        A list of root processes, one from each isolated subnetwork.
    """
    # TODO: Make sure this works and maybe substitute sets with maps so the order is preserved
    # Build the graph of connected processes
    graph = {}
    for node in self.lava_ports.values():
        sender = node['sender']
        receiver = node['receiver']
        synapses = node['pathway'].synapses.name
        if sender not in graph:
            graph[sender] = set()
        if receiver not in graph:
            graph[receiver] = set()
        graph[sender].add(receiver)
        # Also add the synapses to the sender graph
        graph[sender].add(synapses)
        graph[receiver].add(sender)
    
    # Check for processes which don't require lava ports (isolated components)
    for process in processes:
        if not process in list(graph.keys()):
            graph[process] = set()

    # Log the whole graph to know that everything is working out correctly
    self.logger.diagnostic(graph)

    # Traverse the graph to find connected components
    visited = set()
    components = []
    subnetwork_probes = []
    # BFS algorithm: https://en.wikipedia.org/wiki/Breadth-first_search
    for node in graph:
        if node not in visited:
            component = set()
            queue = [node]
            component_probes = []
            while queue:
                curr_node = queue.pop(0)
                if curr_node not in visited:
                    visited.add(curr_node)
                    component.add(curr_node)
                    # Add the neighboring nodes to the queue
                    queue.extend(graph[curr_node])
            components.append(component)
            # We add the component probes here because lists are unhashable so can't use sets before.
            for node in component:
                component_probes.extend(probes[node])
            subnetwork_probes.append(component_probes)
    # Select one node from each component
    root_nodes = []
    for component in components:
        root_nodes.append(processes[list(component)[0]])


    return root_nodes, subnetwork_probes


def init_lava_monitors(self, process, num_steps):
    """
    Initializes Lava monitors as required by the monitors defined by the user in Brian.
    In case a monitor has additional variables to be monitored, the function wrapped by this method
    will call itself recursively (see ``brian2lava.utils.monitors``).

    Parameters
    ----------
    process : `AbstractProcess`
        Lava process. If the process possesses a variable which is to be monitored, the monitor is initialized.
    num_steps : `int`
        Number of steps for which the monitor shall be active. In the current implementation this is set to
        the number of steps in the simulation.

    Notes
    -----
    Lava variables can only be accessed by one ``Monitor`` object at a time. This means that if a variable is probed
    by multiple Brian monitors, it will be probed only once by Lava. The reference to the variable values is then 
    handled by referencing the same monitor object in the different Brian monitors.
    """
    probes = []
    for mon in self.lava_monitors.values():
        # Only look at the right monitors
        if not process.name == mon['source']:
            continue
        init_monitor(mon, process, num_steps, self.lava_monitors)
        
        if self.mode == 'preset' and mon['lava_monitor']:
            probes.append(mon['lava_monitor'])
        for add_mon in mon['additional_var_monitors']:
            probes.append(add_mon['lava_monitor'])
    return probes



def set_brian_monitor_values(self, process):
    """
    Transfer values from Lava monitors or ``StateProbe`` objects to Brian monitor format.

    Parameters
    ----------
    process : `AbstractProcess`
        Lava process that is provided with a monitor.
    """
    # Iterate over Lava monitors
    for mon in self.lava_monitors.values():

        # Only do this if the monitor refers to this process and we actually have a monitor
        # (e.g. StateMonitor.t doesn't have a lava_monitor, it's computed manually).
        if not process.name == mon['process_name'] or mon['lava_monitor'] is None:
            continue
        
        # Get monitor variable
        var = mon['var']

        # Define empty data variable
        # NOTE Lava monitors do not probe the inital values while Brian does
        #      We need to manually prepend the initial values to the monitored data
        init_data = None  # Contains initial values
        data = None  # Contains all other values

        # In case of a spike monitor, we need a more specific handling to get the time/spike indices
        if mon['type'] == SpikeMonitor:
            if var.name == 'i':
                # Get the data ------------------------------------------------
                init_raw = np.array([])
                i_init_data = np.array([],dtype = int)
                t_init_data = np.array([])
                # Get initial values from process, this is not required for the Loihi implementation.
                if self.mode == 'flexible':
                    init_raw = getattr(process, f'_{getattr(process,"name")}__spikespace').init
                    i_init_data = np.nonzero(init_raw)[0]
                    t_init_data = np.nonzero(init_raw)[0]*self.defaultclock.dt
                # Get the data from the monitor or RingBuffer, for both i and t the data is the same
                if self.hardware == HARDWARE.Loihi2:
                    raw = self.get_state_probe_values(mon)
                else:
                    raw = self.get_monitor_values(mon)

                i_data = np.concatenate((i_init_data, np.nonzero(raw)[1]))
                
                t_data = (np.nonzero(raw)[0] * self.defaultclock.dt)
                t_data = np.concatenate((t_init_data, t_data))
                
                # Get monitor indices  
                      
                if isinstance(mon['indices'], (np.ndarray,list)): #NOTE: I think it used to be a np.ndarray but now is a list.   
                    # This case happens for variables that were not defined before calling the run() method
                    if len(mon['indices']) == (0,):
                        mon['indices'] = np.arange(data.shape[1])
                    if not self.hardware == HARDWARE.Loihi2:
                        # Only select the indices that the monitor cares about.
                        selected_indices = np.where(np.isin(i_data, mon['indices']))[0]
                        i_data = i_data[selected_indices]
                        t_data = t_data[selected_indices]
                
                count = np.bincount(i_data, minlength = mon['var'].owner.source.N)
                
                # Store the data --------------------------------------------------
                # Only if monitor was supposed to track i and t data
                if not mon['indices'] is False:
                    # Store the monitor data into the device arrays (no fixed-to-float translation)
                    self.set_array_data(var, i_data, process.name)
                    self.set_array_data(var.owner.variables['count'], count, process.name)

                    # Time array (no fixed-to-float translation)
                    self.set_array_data(var.owner.variables['t'], t_data, process.name)

                # Also set the N variable of the SpikeMonitor in order to be able to use indices properly
                self.set_array_data(var.owner.variables['N'], np.array([len(t_data)]), process.name)

                # Additional variables ---------------------------------------------

                # Deal with the additional variables
                for additional_monitor in mon['additional_var_monitors']:
                    # New variable to update in the arrays
                    add_var = additional_monitor['var']
                    #if "loihi" in self.hardware.lower():
                    if self.hardware == HARDWARE.Loihi2:
                        data = self.get_state_probe_values(additional_monitor)
                    else:
                        data = self.get_monitor_values(additional_monitor)[:-1,:]

                    # Get initial values from process and prepare to concatenate
                    init_data = getattr(process, additional_monitor['lava_var_name']).init
                    init_data = np.expand_dims(init_data, 0)
                    # Select only the correct time points for the spiking neurons
                    time_indices = np.nonzero(raw)[0]
                    if isinstance(mon['indices'],(np.ndarray,list)) and not self.hardware == HARDWARE.Loihi2:
                        # This if is a twin of the one above, so we can use the variables defined there
                        time_indices = time_indices[selected_indices]
                    data = np.concatenate((init_data, data), axis=0)[time_indices, i_data]
                    self.set_array_data(add_var, data, process.name)

        # In case of a state monitor, just take the raw data from Lava
        elif mon['type'] == StateMonitor:

            # Get initial values from process
            init_data = getattr(process, mon['lava_var_name']).init
            
            # Get data from Lava monitor or StateProbe
            # NOTE Removing last simulation step to match Brian simulation
            #if "loihi" in self.hardware.lower():
            if self.hardware == HARDWARE.Loihi2:
                data = self.get_state_probe_values(mon)[:-1,:]
            else:
                data = self.get_monitor_values(mon)[:-1,:]
                
            # Add extra dimension for the concatenation
            init_data = np.expand_dims(init_data, 0)

            # Concatenate initial data and simulated data
            if len(init_data) > 0:
                data = np.concatenate((init_data, data), axis=0)
            #self.logger.diagnostic(f"data('{mon['process_name']}', '{var.name}')\n= {data}")
            
            # Just formatting to make sure that we always have two dimensions
            # as used in Brian for state monitor values (only for variables other than time)
            if var.name == 't':
                self.set_array_data(var, np.squeeze(data),process.name)
                continue

            # Manage other variables
            if np.ndim(data) == 1:
                data = np.array([data])

            # If record is set to some specific indices, we only store the data at those indices
            # Note that this is very inefficient, but in Lava it's impossible to select indices
            # to record from a monitor. This is only to keep the results consistent with Brian.
            if isinstance(mon['indices'], (np.ndarray,list)):
                # This case happens for variables that were not defined before calling the run() method
                if len(mon['indices']) == (0,):
                    mon['indices'] = np.arange(data.shape[1])
                data = data[:,mon['indices']]

            # Set the values (fixed-to-float conversion is done internally if required)
            self.set_array_data(var, data, process.name)


def get_state_probe_values(self, monitor):
    """
    Get data from a Lava ``StateProbe`` object.

    Parameters
    ----------
    monitor
        A monitor as defined in the device.
    """
    # Define variables
    lava_state_probe = monitor['lava_monitor']
    lava_var_name = monitor['lava_var_name']
    process_name = monitor['process_name']

    # Get the total number of elements (e.g., number of neurons) - from monitored Brian variable
    N_tot = len(monitor['var'].owner.source)
    # Special case for indices on SpikeMonitors on Loihi2
    indices = monitor['indices']
    if self.hardware == HARDWARE.Loihi2 and not isinstance(indices, bool) and len(indices) !=0 and monitor['type'] == SpikeMonitor:
        N_tot = len(monitor['indices'])

    self.logger.debug(f"Got data from state probe referring to '{process_name}.{lava_var_name}' (N_tot = {N_tot})")
    # Get the StateProbe data and reshape it
    try:
        data_reshaped = np.array(lava_state_probe.time_series.reshape(N_tot,-1).T)
    except Exception as e:
        raise RuntimeError(f"Getting data from state probe referring to '{process_name}.{lava_var_name}' failed ({type(e).__name__}: {str(e)}). "
                           f"Please check if your Lava version still contains this issue: https://github.com/lava-nc/lava/issues/799.")
        # TODO Since Python 3.11, the following is supported and should be used at some point
        # e.add_note("Getting data from...")
        # raise
    
    # Return reshaped time series values
    return data_reshaped
    # TODO Return data for selected indices only (has to be harmonized with `set_brian_monitor_values()` and `get_monitor_values()`)
    # indices = monitor['indices']
    # return data_reshaped[indices]
    
    
def get_monitor_values(self, monitor):
    """
    Get data from a Lava ``Monitor`` object.

    Parameters
    ----------
    monitor
        A monitor as defined in the device.
    """
    # Define variables
    lava_monitor = monitor['lava_monitor']
    lava_var_name = monitor['lava_var_name']
    process_name = monitor['process_name']
    
    # Get and return Lava monitor values
    try:
        data = np.array(lava_monitor.get_data()[process_name][lava_var_name])
    except Exception as e:
        raise RuntimeError(f"Getting data from monitor referring to '{process_name}.{lava_var_name}' failed ({type(e).__name__}: {str(e)}).")
        # TODO Since Python 3.11, the following is supported and should be used at some point
        #e.add_note("Getting data from...")
        #raise
    return data


def update_brian_class_attributes(self, processes):
    """
    Updates class attributes of Brian objects after running a simulation.
    This allows the user to access attributes of Brian objects as they would in normal Brian.
    We do this by going through the processes and finding their corresponding Brian objects.
    Then we update the array variable held by the device with the new values so that when ``get_value()`` gets called
    the correct, most recent, values are displayed.

    Parameters
    ----------
    processes : dict of `AbstractProcess`
        Dictionary of Lava processes.
    """
    # Iterate over processes
    for proc in processes.values():
        proc_obj = self.lava_objects.get(proc.name)
        # If the process name is not in `lava_objects` it's an auxiliary object (like the PyToNxAdapter)
        if proc_obj is None:
            continue
        # We have to check for variables also in the objects contained in each of our objects (e.g. SynapticPathway inside Synapses)
        objs_to_consider = [o for o in proc_obj.contained_objects if hasattr(o, "variables")]
        objs_to_consider.append(proc_obj)
        for obj in objs_to_consider:
            for var in obj.variables.values():
                # SpikeQueue is a variable, but has no owner (and should not be accessed anyways)
                if not hasattr(var, 'owner'):
                    continue
                # Skip the `dt` variable (for synapses there is the issue that Lava's `LearningConnectionProcess`
                # class contains an attribute named `dt` that has nothing to do with the timestep; in other cases,
                # there can be issues as well, and we usually won't have to read this out anyway)
                elif var.name == 'dt':
                    continue
                # Get the name of the variable
                # In flexible mode, this is simply the array name
                if self.mode == 'flexible':
                    var_name = self.get_array_name(var, prefix = None)
                # For weights, there is a defined name
                elif var.name == 'w' and isinstance(obj, Synapses):
                    var_name = 'weights'
                # For bias in mantissa-and-exponent representation, use the mantissa name (not available on Loihi)
                elif obj.name in LavaParameters.mantissa_exp_vars \
                                            and var.name in LavaParameters.mantissa_exp_vars[obj.name]:
                    if self.hardware == HARDWARE.Loihi2:
                        var_name = var.name
                        if not hasattr(proc, var_name):
                            self.logger.warn(f"The value of variable '{var.name}' cannot be updated. Reading "
                                             f"out variables in mantissa-and-exponent representation is not "
                                             f"seamlessly possible from microcode.")
                    else:
                        var_name = LavaParameters.mantissa_exp_vars[obj.name][var.name]['mant']
                # Otherwise, use the value of the `name` attribute
                else:
                    var_name = var.name
                        
                # Set array variable, if the current process has it
                if hasattr(proc, var_name):
                    # Get the name of the variable with the name of the superior process
                    proc_var_name = proc.name + "." + var_name
                    # Assign an empty array because empty variables cannot be handled by Lava's `get()` method.
                    if getattr(proc, var_name).shape == (0,):
                        value = []
                    # Get data from Lava variable.
                    else:
                        try:
                            value = getattr(proc, var_name).get()
                        except:
                            self.logger.error(f"Error reading value of '{var_name}' from process '{proc.name}'.")
                            raise

                    # Readout of altered (optimized) weight exponent from NcProcessModel
                    # TODO With current version of Lava-Loihi not possible
                    #if var_name == 'weights' and self.hardware == HARDWARE.Loihi2:
                    #    try:
                    #        value = getattr(proc, 'weights_exp').get()
                    #    except:
                    #        self.logger.error(f"Error reading value of 'weights_exp' from process '{proc.name}'.")
                    #        raise
                    #    self.logger.info(f'weights_exp = {weights_exp}')
                    
                    # Set the values
                    # TODO at some point might have to do conversion to sparse for all synaptic variables
                    convert_to_sparse = True if var_name == 'weights' else False
                    self.set_array_data(var, np.array(value, dtype=var.dtype), proc.name, to_sparse=convert_to_sparse)
                    self.logger.diagnostic(f"Set {proc_var_name} = {value}")

            # Synapse-related variables
            if isinstance(obj, Synapses):
                # Update the variables counting the number of synapses
                # TODO Verify that this is not needed during the simulation, as right now, 
                #      we only update these variables AFTER running a simulation..
                obj._update_synapse_numbers(len(obj))
