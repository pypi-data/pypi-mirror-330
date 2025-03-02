import numpy as np

from brian2.memory.dynamicarray import DynamicArray, DynamicArray1D
from brian2.core.variables import ArrayVariable, DynamicArrayVariable

from brian2.monitors.spikemonitor import SpikeMonitor
from brian2.monitors.statemonitor import StateMonitor
from brian2lava_test.utils.math import F2F
from brian2lava_test.utils.const import HARDWARE

def get_value(self, var, access_data=True):
    """
    Get a value from an array. Returning a value from the device arrays depends on the type of array, 
    which can either be a dynamic array (of the class DynamicArrayVariable) or a static array (of the 
    super class ArrayVariable).

    Parameters
    ----------
    var : `ArrayVariable`
        The array to get
    access_data : `bool`
        A flag that indicates if it is intended to access only the data of the dynamic array (True)
        or the whole dynamic array (False)

    Returns
    -------
    `any`
        Values of the array variable as list
    """

    # Log that a value was requested from arrays
    self.logger.diagnostic(f'get_value {var.name}')

    # Simple numpy runtime way
    if self.mode == 'preset':
        if isinstance(var, DynamicArrayVariable) and access_data:
            return self.arrays[var].data
        else:
            return self.arrays[var]

    # The variable should be stored in self.arrays, if it's None then the device hasn't been run yet.
    if self.arrays.get(var, None) is not None:
        return self.arrays[var]
    
    raise NotImplementedError(
                "Cannot retrieve the values of state "
                "variables in standalone code before the "
                "simulation has been run."
            )

def get_dtype_name(var):
    """
    Get the data type of a variable and return its name as a string. Serves to avoid expressions like 'np.bool' that
    are deprecated since NumPy 1.24. In the case of a NumPy data type, returns the name with the prefix 'np.'.

    Parameters
    ----------
    var : `any`
        The variable to consider (can also be a data type object itself)

    Returns
    -------
    `string`
        Name of the dtype
    """
    # DynamicArrays are special
    if isinstance(var,DynamicArray):
        dtype = np.dtype(var)
    # If 'var' is an array
    elif np.ndim(var) > 0:
        dtype = var.dtype
    # If 'var' is a scalar variable
    else:
        dtype = np.dtype(type(var))

    # Check if Python or NumPy data type is used
    if dtype in [bool, int, float, complex, str, np.int32, np.int64, np.float32, np.float64]:
        ret = dtype.name.replace('32', '').replace('64', '')
    else:
        ret = "np." + dtype.name

    return ret


def get_monitor_var_name(self, var):
    """
    Get a variable name for a monitor variable. This is a bit more nuanced because
    we have to look at the actual BrianObject that owns the variable.

    Parameters
    ----------
    var : `ArrayVariable`
        An array variable

    Returns
    -------
    `string`
        The corresponding lava variable name

    Notes
    -----
    TODO This can possibly be hamrmonized with `get_array_name`.
    """
    # For the sake of clarity we keep the different hardware implementations separate.
    if self.mode == 'flexible':
        if isinstance(var.owner, StateMonitor):
            # The t variable is generally owned by a Clock object (for now only defaultclock is supported)
            source_name = 'defaultclock' if var.name == 't' else var.owner.source.name
            lava_var_name = f'_{source_name}_{var.name}'
        elif isinstance(var.owner, SpikeMonitor):
            if var.name == 't': 
                lava_var_name = '_defaultclock_t' 
            elif var.name == 'i': 
                lava_var_name = var.owner.source.name +'_s_out'
            # Manage the case of additional variables in the SpikeMonitor
            else: 
                lava_var_name = f'_{var.owner.source.name}_{var.name}'
        else:
            raise ValueError("The owner of this variable is not a monitor. Please use 'device.get_array_name()' instead.")
        
    else:
        if not isinstance(var.owner, (StateMonitor,SpikeMonitor)):
            raise ValueError("The owner of this variable is not a monitor. Please use 'device.get_array_name()' instead.")
        if var.name == 'i' and isinstance(var.owner,SpikeMonitor):
            lava_var_name = 's_out'
        else:
            lava_var_name = var.name
        

    return lava_var_name



def get_array_name(self, var, access_data=True, prefix='self.'):
    """
    Gets the name of an array variable.

    Parameters
    ----------
    var : `ArrayVariable`
        The array to get.
    access_data : `bool`
        A flag that indicates if it is intended to access only the data of the dynamic array (True)
        or the whole dynamic array (False)
    prefix : `string`
        A string that is added as a prefix to the array name
        Default is 'self.', in case of 'None', no prefix is added

    Returns
    -------
    `string`
        The corresponding variable name as it is used in Brian

    Notes
    -----
    TODO This can possibly be harmonized with `get_lava_var_name`.
    """
    
    # The name of the array is part of the owner attribute
    # The owner is a `Nameable`, e.g. `NeuronGroup` or `Synapses`
    # If no owner name is available, 'temporary' is assigned
    owner_name = getattr(var.owner, 'name', 'temporary')
    # We treat the Loihi2 hardware a bit differently, we use the get_array_name method
    # from brian2's RuntimeDevice
    if self.mode == 'preset':
        if isinstance(var, DynamicArrayVariable):
            if access_data:
                return f"_array_{owner_name}_{var.name}"
            else:
                return f"_dynamic_array_{owner_name}_{var.name}"
        # Keep consistent naming with numpy code generator
        prefix = '_array'

    # Redefine prefix to empty string if it was set to 'None'
    if prefix is None:
        prefix = ''
    
    return f'{prefix}_{owner_name}_{var.name}'

def add_monitor_var(self, var):
    """
    Add a variable to the list of variables to monitor. Particularly, we create dictionary entries
    with the required information to set up Lava Monitors or StateProbes to monitor the required variables.
    If a variable is pointed at by multiple monitors (not allowed in Lava), this will be taken care later on in the pipeline,
    in the methods of 'run.py'.

    Parameters
    ----------
    var : `ArrayVariable`
        The variable to be added to the monitor dictionary
    """
    if isinstance(var.owner.record, bool):
        # We only add a monitor if the record flag is not set to False, which means that the
        # monitor is not used for recording.
        if var.owner.record == False:
            if isinstance(var.owner, SpikeMonitor):
                self.logger.warn("Currently, setting 'record=False' in the SpikeMonitor is being ignored. This will be implemented in a future release (see https://gitlab.com/brian2lava/brian2lava/-/issues/37).")
            else:
                return   
    else:
        msg = """[EFFICIENCY]: Recording specific indices is currently not supported by Lava. Thus,
                the monitor will record all indices, and then the data will be filtered by Brian2Lava
                so that the output is compatible with the outcome expected from Brian. This can cause
                the current setting to be significantly slower than known from Brian."""
        # Check if the user is trying to record specific indices
        try:
            # TODO Possibly introduce in `set_brian_monitor_values()` a check which indices are specified
            #     and only do the filtering if not all possible indices are specified.
            if len(var.owner.record) < len(var.owner.source) and var.name != 't':
                self.logger.warn(msg)
        # This error is raised in case len(source) is not defined yet (we need to run the simulation first), 
        # in this case the warning still applies, though.
        except NotImplementedError:
            self.logger.warn(msg)
    monitor = var.owner

    # We don't need a monitor for spike timings since this measurement is 
    # handled differently.
    if var.name == 't' and isinstance(monitor, SpikeMonitor):
        return

    # Define monitor name and Lava variable name
    spike_or_state = 'spike' if isinstance(monitor, SpikeMonitor) else 'state'
    # The name of this monitor. 
    monitor_name = f'_{spike_or_state}_{monitor.name}'
    # Spike monitors don't need variable names, this is to allow monitoring additional variables. NOTE the '+='! The definition is above!
    monitor_name += f'_{var.name}' if isinstance(monitor, StateMonitor) else ''
    # The name of the Lava variable
    lava_var_name = self.get_monitor_var_name(var)

    # Set up the additional monitors if they were not yet defined.
    if not monitor_name in self.additional_monitors:
        self.additional_monitors[monitor_name] = []
        self.logger.diagnostic(f"Additional monitor '{monitor_name}' added for variable '{var.name}' (Lava: '{monitor.source.name}.{lava_var_name}').")

    # Collect Lava variable names that shall be monitored by Lava.
    # Mainly for debug purposes
    self.lava_variables_to_monitor.add(lava_var_name)

    # Special case: If the monitor already exists then we are dealing with an additional variable for SpikeMonitor
    if isinstance(monitor,SpikeMonitor) and var.name != 'i':
        monitor_dict = {
                'name' : monitor_name + f"_add_{var.name}", # The name of this monitor, mainly for debugging
                'source': monitor.source.name,
                'var': var,  # Brian variable
                'indices': monitor.record,  # The indices of the variable to record
                'lava_var_name': lava_var_name,  # The variable name used in Lava
                'lava_monitor': None,  # The Lava Monitor or StateProbe object, is added later during 'run_processes'
                'process_name': None # The name of the process that is monitored, will be set during 'run_processes'
            }
        # Add this monitor to the additional monitors
        self.additional_monitors[monitor_name].append(monitor_dict)
        try:
            # Add the additional monitors to the existing monitor
            self.lava_monitors[monitor_name]['additional_var_monitors'] = self.additional_monitors[monitor_name]
        except KeyError:
            # This happens if the monitor was not added yet, so the additional monitors will be added 
            # when the monitor is defined through the 'i' variable.
            self.logger.debug(f"Monitor {monitor_name}_{var.name} not added yet, will add the additional var monitor for {lava_var_name} later.")
        return

    # This is the general purpose case. We are dealing with a new monitor (or, in fact, a StateProbe if Loihi 2 is being used).
    self.lava_monitors[monitor_name] = {
        'name' : monitor_name, # The name of this monitor, mainly for debugging
        'source': monitor.source.name,
        'var': var,  # Brian variable
        'indices': monitor.record,  # The indices of the variable to record
        'lava_var_name': lava_var_name,  # The variable name used in Lava
        'type': SpikeMonitor if isinstance(monitor,SpikeMonitor) else StateMonitor, # The monitor type 
        'additional_var_monitors': self.additional_monitors[monitor_name],  # Additional variables to monitor, e.g. 'v' for SpikeMonitor
        'lava_monitor': None,  # The Lava Monitor or StateProbe object, is added later during 'run_processes'
        'process_name': None # The name of the process that is monitored, will be set during 'run_processes'
    }
    self.logger.diagnostic(f"Monitor '{monitor_name}' added for variable '{var.name}' (Lava: '{monitor.source.name}.{lava_var_name}').")


def add_array(self, var):
    """
    Add an (empty) array variable to the `arrays` list of the device.
    It can either be added as static NumPy array or as a `DynamicArrayVariable` object.
    The `DynamicArrayVariable` can dynamically be extended (in contrast to a static array).

    We separate between monitors and all other owner types of the variable to add.
    Monitors are added to the `lava_monitors` dictionary; other variables are added to the
    `lava_variables` dictionary.
    
    TODO Add monitored variables to the `lava_variables` dictionary as well?

    Parameters
    ----------
    var : `ArrayVariable`
        The array variable to add
    """

    # NOTE only for preset mode, on flexible mode this is not necessary
    # Only add array if owner is of class SpikeMonitor or StateMonitor
    #if not isinstance(var.owner, (SpikeMonitor, StateMonitor)):
    #    return
    # TODO: Should all of the commented part above be deleted?

    # Log that a value was added to arrays
    self.logger.diagnostic(f'add_array {var.name}')

    # DynamicArrays need a special treatment to manage resizing
    if isinstance(var, DynamicArrayVariable):
        if var.ndim == 1:
            arr = DynamicArray1D(var.size, dtype=var.dtype)
        else:
            arr = DynamicArray(var.size, dtype=var.dtype)
    else:
        arr = np.empty(var.size, dtype=var.dtype)

    self.arrays[var] = arr

    # If this variable belongs to a monitor, we have to add it to the `lava_monitors` dictionary for tracking it.
    if isinstance(var.owner, (SpikeMonitor, StateMonitor)):
        # NOTE Currently only dynamic array variables of a monitor (like v, t, etc.) are added
        #      Constant values like N or __indices are currently ignored
        if isinstance(var, DynamicArrayVariable):
            self.add_monitor_var(var)
    # Add the variable to the `lava_variables` dictionary for tracking it.
    else:
        dtype_name = get_dtype_name(arr)
        type_name = dtype_name

        # Add the definition of a numpy array as string for Lava
        # By default we initialize to zero, as it's generally a safe value.
        var_definition = f'np.zeros({var.size}, dtype={type_name})'

        # TODO is the key unique?
        # See also: https://github.com/brian-team/brian2/pull/304
        name = self.get_array_name(var, prefix=None)
        self.lava_variables[name] = {
            'name': var.name,
            'owner': var.owner.name,
            'definition': var_definition,
            'size': var.size,
            'shape': np.shape(arr),
            'type': type_name,
            'dtype': dtype_name
        }


def init_with_zeros(self, var, dtype):
    """
    Initialize an array with zeros and adds it to the `arrays` list.

    Parameters
    ----------
    var : `ArrayVariable`
        The array variable to initialize with zeros
    dtype : `dtype`
        The data type to use for the array
    """

    # Redefine variable definition for Lava variables
    name = self.get_array_name(var,prefix=None)
    if name in self.lava_variables.keys():
        lv = self.lava_variables[name]
        lv['definition'] = f"np.zeros({lv['size']}, dtype={lv['dtype']})"
    
    # Log that an empty array was initialized
    self.logger.diagnostic(f'init_with_zeros {var.name}')
    
    self.arrays[var][:] = 0


def init_with_arange(self, var, start, dtype):
    """
    Initializes an array using the numpy arange function and adds it to the `arrays` list.
    The `start` value defines the start of the range, the length is given by the length of the `var` array.
    
    Parameters
    ----------
    var : `ArrayVariable`
        The array to initialize is based on the length of this `var` array
    start : `int`
        Start value of the range
    dtype : `dtype`
        The data type to use for the array
    """

    # Redefine variable definition for Lava variables
    name = self.get_array_name(var,prefix=None)
    if name in self.lava_variables.keys():
        lv = self.lava_variables[name]
        lv['definition'] = f"np.arange({start}, {lv['size']+start}, dtype={lv['dtype']})"
    
    # Log that an array was created based on numpy arange
    self.logger.diagnostic(f'init_with_arange, arange from {start} to {var.get_len()+start}')
    
    self.arrays[var][:] = np.arange(start, stop=var.get_len()+start, dtype=dtype)


def fill_with_array(self, var, arr):
    """
    Fill array variable `var` with the values given in an array `arr` and add it to the `arrays` list.
    Instead of modifying the definition of the variable itself, we add a line of code to the init queue
    which will be executed at initialization of the process. This allows the user to modify variables
    seamlessly any number of times without incurring into bugs.
    The methodology we use is compatible with the one used in the CPPStandaloneDevice:
    https://github.com/brian-team/brian2/blob/master/brian2/devices/cpp_standalone/device.py#L415
    
    Parameters
    ----------
    var : `ArrayVariable`
        The array variable to fill
    arr : `ndarray`
        The values that will be copied to `var`
    """

    # For preset mode we use the simple Numpy pipeline
    if self.mode == 'preset':
        self.arrays[var][:] = arr
        return

    arr = np.asarray(arr)
    if arr.size == 0:
        return # nothing to do
    
    # Redefine variable definition for Lava variables
    array_name = self.get_array_name(var,prefix=None)
    # Set array value
    if isinstance(var, DynamicArrayVariable):
        # Following CPPStandalone example, we can't correctly know the 
        # value of a dynamic array, so for now we don't save it at all
        self.arrays[var] = None
    else:
        new_arr = np.empty(var.size, dtype=var.dtype)
        new_arr[:] = arr
        self.arrays[var] = new_arr
    
    if arr.size == 1:
        if var.size == 1:
            value = arr.item()
            # For a single assignment, generate a code line instead of storing the array
            self.proc_init_queue[var.owner.name].append(("set_by_single_value", (array_name, 0, value)))
        else:
            self.proc_init_queue[var.owner.name].append(
                (
                    "set_by_constant",
                    (array_name, arr.item()),
                )
            )
    else:
        # Using the std::vector instead of a pointer to the underlying
        # data for dynamic arrays is fast enough here and it saves us some
        # additional work to set up the pointer
        arr_str = np.array2string(np.array(arr), separator=', ')
        self.proc_init_queue[var.owner.name].append(("set_by_array",(array_name,arr_str)))

    # Log that an array was filled with given values
    self.logger.diagnostic(f'fill_with_array, add {arr} to {var.name}')
    

def resize(self, var, new_size):
    """
    Method called most times a DynamicArray variable is created. Updates the size of a DynamicArray.
    We add this operation to the initialization queue for the lava processes in order to keep the ordering consistent.

    Parameters
    ----------
    var : `ArrayVariable`
        The array variable to be resized
    new_size : `int`
        The new size of the array
    """
    # For preset mode we don't actually use an init queue.
    if self.mode == 'preset':
        self.arrays[var].resize(new_size)
        return
    
    # This is an operation we can still manage with the array cache (useful for synaptic numbers such as N_incoming and N_outgoing)
    if self.arrays.get(var,None) is not None:
        self.arrays[var] = np.resize(self.arrays[var], new_size)
    # Change the size of the variable in our init_queue
    name = self.get_array_name(var,prefix=None)
    if name in self.lava_variables.keys() and self.mode == 'flexible':
        self.proc_init_queue[var.owner.name].append(('resize_array', (name,new_size)))


def set_array_data(self, var, data, owner_name):
    """
    Used to set the values of a variable in the arrays dictionary after retrieving them from the Lava monitors or StateProbes.
    Accounts for the fact that in some instances `self.arrays[var]` is `None` for DynamicArrays, so we first
    create a DynamicArray to contain the data and then assign it.
    Also, may automatically convert the values back to floating-point if the simulation was run in fixed-point
    representation. 

    Parameters
    ----------
    var : `ArrayVariable`
        The array variable to set
    data : `ndarray`
        The values that will be copied to `var`
    owner_name : `str`
        Name of the owner process of `var`. Used to determine if conversion from fixed-point back to floating-point
        representation is to be done.
    """
    # Fixed-to-float conversion
    f2f_var_name = owner_name + '.' + var.name
    if self.is_using_f2f() and f2f_var_name in F2F.parameters:
        if var.name in F2F.mantissa_exp_vars:
            data = F2F.mantissa_exponent_to_float(data)
        else:
            data = F2F.fixed_to_float(data)
        
    # Just in case a non-dynamic variable gets passed to it.
    if not isinstance(var, DynamicArrayVariable) or self.mode == 'flexible':
        self.arrays[var] = data
        return

    # Update the size to contain the data
    if var.ndim == 1:
        arr = DynamicArray1D((len(data),), dtype=var.dtype)
    else:
        arr = DynamicArray(data.shape, dtype=var.dtype)
    arr.data = data
    self.arrays[var] = arr


# To make Runtime pipeline work for Loihi implementation ========================

def set_value(self, var, value):
    """
    Setting a value to an array variable.
    Only required for the Loihi 2 implementation.
    
    Parameters
    ----------
    var : `any`
        The array variable to set
    value : `any`
        The values to assign to the variable
    """
    if self.mode == 'preset':
        self.arrays[var][:] = value
    else:
        raise NotImplementedError

def resize_along_first(self, var, new_size):
    """
    Resizing an array variable along the first dimension of the given shape (see 
    https://brian2.readthedocs.io/en/stable/_modules/brian2/memory/dynamicarray.html#DynamicArray.resize_along_first).
    Only required for the Loihi 2 implementation.   
    
    Parameters
    ----------
    var : `any`
        The array variable to resize
    new_size : tuple of `int`
        Shape determining the new size of the variable
    """
    if self.mode == 'preset':
        self.arrays[var].resize_along_first(new_size)
    else:
        raise NotImplementedError

    

