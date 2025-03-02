from brian2 import SpikeMonitor, get_logger
from brian2lava.utils.utils import mode_dependent
from brian2lava.utils.const import HARDWARE
from lava.proc.monitor.process import Monitor
import os
try:
    from lava.utils.loihi2_state_probes import StateProbe # import here because this is only part of lava-loihi
    from lava.magma.core.callback_fx import NxSdkCallbackFx
    class SpikeProbe(NxSdkCallbackFx):
        def __init__(self, monitor_name, indices, project_dir = os.getcwd()):
            self.logger = get_logger('brian2.devices.lava')
            self.trace_probes = []
            self.syn_probes = []
            self.spike_probes = []
            self._time_series = None
            self.spike_series_file = os.path.join(project_dir , monitor_name + '_spikes_series.npy')
            self.indices = indices

        def pre_run_callback(self, board, var_id_to_var_model_map):
            # select core
            nxCores = board.nxChips[0].nxCores
            mon = board.monitor
            groups = nxCores[0].neuronInterface.group
            pCores = nxCores[0].parent.processorCores

            self.logger.diagnostic(f"board.nxChips = {board.nxChips}")
            self.logger.diagnostic(f"board.nxChips[0].nxCores = {board.nxChips[0].nxCores}")
            self.logger.diagnostic(f"groups = {groups}")
            self.logger.diagnostic(f"nxCores[0].parent.processorCores = {nxCores[0].parent.processorCores}")
            self.logger.diagnostic(f"len(pCores) = {len(pCores)}")
            for i in range(len(pCores)):
                self.logger.diagnostic(f"pCores[{i}] = {pCores[i]}")
                self.logger.diagnostic(f"pCores[{i}].spikeCounter.axons = {pCores[i].spikeCounter.axons}")
                self.logger.diagnostic(f"len(pCores[{i}].spikeCounter.axons) = {len(pCores[i].spikeCounter.axons)}")
            #self.logger.debug(f"var_id_to_var_model_map = {var_id_to_var_model_map}")
            self.logger.debug(f"self.indices = {self.indices}")
            
            # record post-synaptic spike raster
            for idx in self.indices:

                # Loop over available nx cores
                success = False
                for nxCore in nxCores:
                    self.logger.diagnostic(f"Initializing axon program on nx core {nxCore.coreId.id}...")
                    axonProg = nxCore.axonInterface.newProgram()
                    pCores = nxCore.parent.processorCores
                    groups = nxCore.neuronInterface.group
                    
                    # Loop over available processor cores
                    for pCore in pCores:
                        self.logger.diagnostic(f"Calling 'axon_core_send' on processor core {pCore.coreId.id}...")
                        axonProg.axon_core_send(core=pCore.coreId.id, axon=pCore.spikeCounter.axons[idx])
        
                        # Try to add program with one of the available groups
                        group_id = 0
                        while group_id < len(groups):
                            axonMap = groups[group_id].axonInterface._parent.axonMap                            
                            self.logger.diagnostic(f"Adding program with index {idx} in group {groups[group_id].groupIdx}...")
                            try:
                                # This test has to be done because the following command is executed within nxcore, 
                                # which runs separately from the current Python thread.
                                _ = axonMap[idx]
                                # Now we can safely add the program for the current index (otherwise, an exception would have
                                # been thrown before) and then exit the loops.
                                groups[group_id].axonInterface.addProgram(idx, axonProg)
                                success = True
                                break
                            except IndexError:
                                group_id += 1
        
                        # If program was added successfully, set spike probe
                        if success:
                            self.logger.debug(f"Added program with index {idx} on nx core {nxCore.coreId.id}, processor core {pCore.coreId.id}, "
                                              f"group {groups[group_id].groupIdx}...")
                            self.spike_probes.append(mon.probe(pCore.spikeCounter, [idx], 'spike_count')[0])
                            break
                            
                    # If program was added and spike probe was set, leave the loop
                    if success:
                        break

                # Notfication if index was not found
                if not success:
                    self.logger.debug(f"Index {idx} not found anywhere.")


        def post_run_callback(self, board, var_id_to_var_model_map):
            spike_data = [probe.data for probe in self.spike_probes]
            np.save(self.spike_series_file, spike_data)
            self.logger.debug(f"Saved spike series to {self.spike_series_file}")
        
        @property
        def time_series(self):
            try:
                self.logger.debug(f"Retrieving spike series from {self.spike_series_file}")
                self._time_series = np.load(self.spike_series_file, allow_pickle=True)
                os.remove(self.spike_series_file)
            except Exception as e:
                if self._time_series is not None:
                    pass
                else:
                    raise e
            return self._time_series

except ImportError:
    pass

from brian2.monitors import StateMonitor
from brian2 import get_device, get_logger

import numpy as np

@mode_dependent
def set_up_probe(mon, process, num_steps, all_monitors):
    raise NotImplementedError("The mode chosen for this mode dependent function was not found. Please"
                              " make sure to define the device mode correctly.")

def set_up_probe_preset(mon, process, num_steps, all_monitors):
    device = get_device()
    logger = get_logger(module_name='brian2.devices.lava')
    lava_var_name = mon['lava_var_name']
    # Processes in Lava (used in preset mode) don't contain a 't' variable.
    # Here we give Brian the variable directly, since we have all the required information.
    if lava_var_name == 't' and mon['type'] == StateMonitor:
        dt = mon['var'].owner.source.clock.dt
        t_0 = int(mon['var'].owner.source.clock.t/dt)
        # To avoid a strange "setting array elements with a sequence error" with np.arange()
        t_array = np.array(range(t_0, t_0+num_steps)*dt)
        # No need to do F2F translation here since we're using native Brian 2 values
        get_device().set_array_data(mon['var'].owner.variables['t'], t_array, process.name)
        return None
    
    # Init Lava monitor (depends on hardware) and define probe for variable
    if device.hardware == HARDWARE.Loihi2:
        if mon['type'] == SpikeMonitor:
            indices = mon['indices']
            if not isinstance(indices, (np.ndarray,list)):
                indices = np.arange(process.proc_params["shape"][0])
            probe = SpikeProbe(monitor_name=mon['name'],indices = indices,project_dir = device.project_dir)
        else:
            probe = StateProbe(getattr(process, lava_var_name))
    else:
        probe = Monitor()
        probe.probe(getattr(process,lava_var_name), num_steps)
    logger.debug(f"Setting state probe to: {process.name}.{lava_var_name}")

    # Allow probing of additional variables for spike monitors - if there is an 'additional_var_monitors' item 
    additional_monitors = mon.get('additional_var_monitors')
    if additional_monitors:
        for additional_monitor in additional_monitors:
            init_monitor(additional_monitor, process, num_steps,all_monitors)   
    return probe

def set_up_probe_flexible(mon, process, num_steps, all_monitors):
    lava_var_name = mon['lava_var_name']
    # Init Lava monitor and define probe for variable
    monitor = Monitor()
    monitor.probe(getattr(process, lava_var_name), num_steps)
    # Allow probing of additional variables for spike monitors - if there is an 'additional_var_monitors' item 
    additional_monitors = mon.get('additional_var_monitors')
    if additional_monitors:
        for additional_monitor in additional_monitors:
            init_monitor(additional_monitor, process, num_steps, all_monitors)
        
    return monitor

def init_monitor(monitor_dict, process, num_steps, all_monitors):
    """
    We define this extra method because it can be called recursively for additional variables in SpikeMonitors
    """    
    monitor_object = None
    # NOTE Lava allows only one monitor per variable, so we only create one if one was not already created
    try:
        # We isolate the mode-dependent code in this function
        monitor_object = set_up_probe(monitor_dict, process, num_steps, all_monitors)
    # If the monitor already exists, lava throws an AssertionError (This should not happen anymore from lava-nc-v0.9.0)
    # At some point we could deprecate this part of the code.
    except AssertionError:
        # Create a comprehensive list of all monitors:
        monitors_including_add_mon = [mon for mon in all_monitors.values()]
        for mon in all_monitors.values():
            monitors_including_add_mon.extend(mon['additional_var_monitors'])
        # If that's the case, we look for the monitor in the previously defined monitors
        for pre_mon in monitors_including_add_mon:
            if not pre_mon['lava_monitor'] is None and pre_mon['source'] == monitor_dict['source'] and pre_mon['lava_var_name'] == monitor_dict['lava_var_name']:
                monitor_object = pre_mon['lava_monitor']
                break
        if monitor_object is None: raise AssertionError(f"Something went wrong: the monitor for {monitor_dict['source']} and {monitor_dict['lava_var_name']} was not found.")

    monitor_dict['lava_monitor'] = monitor_object
    # Note that for the spike monitor additional variables this is redundant, but harmless.
    monitor_dict['process_name'] = process.name