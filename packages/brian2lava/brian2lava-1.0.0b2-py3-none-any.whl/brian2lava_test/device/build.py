import os
import tempfile
import numpy as np
from jinja2 import FileSystemLoader, Environment

from lava.magma.core.run_configs import Loihi2SimCfg
from lava.magma.core.run_conditions import RunSteps

# Import Brian2 modules
# from brian2.units.allunits import second
# from brian2.core.functions import Function
# from brian2.core.variables import Constant, ArrayVariable, AuxiliaryVariable
from brian2.groups.neurongroup import NeuronGroup, StateUpdater, Resetter, Thresholder, SubexpressionUpdater
from brian2.input.poissongroup import PoissonGroup
from brian2.input.spikegeneratorgroup import SpikeGeneratorGroup
from brian2.monitors.spikemonitor import SpikeMonitor
from brian2.monitors.ratemonitor import PopulationRateMonitor
from brian2.monitors.statemonitor import StateMonitor
from brian2.synapses.synapses import Synapses, SpikeSource
# from brian2.units import second

from pprint import pprint

from brian2lava_test.utils.const import runtime_configs, HARDWARE
from brian2lava_test.preset_mode.handler import PresetProcessHandler
from brian2lava_test.utils.math import F2F


def build(
    self,
    direct_call=True
):
    """
    Builds the Lava executables.

    It contains the following steps:

    *   includes some checks
    *   initializes file write
    *   renders the templates
    
    Parameters
    ----------
    direct_call : `bool`, optional
        Whether this function was called directly. Is used internally to
        distinguish an automatic build due to the ``build_on_run`` option
        from a manual ``device.build`` call.
    """
    
    # Log that the build method was called
    self.logger.debug("Building Lava device.")
    
    # Check if direct_call was used properly
    if self.build_on_run and direct_call:
        raise RuntimeError("You used set_device with build_on_run=True "
                           "(the default option), which will automatically "
                           "build the simulation at the first encountered "
                           "run call - do not call device.build manually "
                           "in this case. If you want to call it manually, "
                           "e.g. because you have multiple run calls, use "
                           "set_device with build_on_run=False.")
    
    # Check if network was already running before (FIXME necessarry?)
    if self.did_run:
        raise RuntimeError("The network has already been built and run "
                           "before. To build several simulations in "
                           "the same script, call \"device.reinit()\" "
                           "and \"device.activate()\". Note that you "
                           "will have to set build options (e.g. the "
                           "directory) and defaultclock.dt again.")
    
    # Prepare working directory
    self.prepare_directory()
    
    # TODO Unique network object names necessary?
    # See: https://github.com/brian-team/brian2/blob/master/brian2/devices/cpp_standalone/device.py#L1238
    
    # Get dt in seconds without unit
    dt_ = self.defaultclock.dt_
    # For now the process_kwargs does not need to be a device attribute, so we keep it local.
    from collections import defaultdict
    process_kwargs = defaultdict(lambda: None)  
    if self.mode == 'flexible':
        # Add 'dt' to 'lava_variables' to make it available to Lava
        self.lava_variables['_defaultclock_dt']['definition'] = f'np.array([{dt_}])'
        # Render Lava templates
        for obj in self.lava_objects.values():
            # Set the class name so that we know what object to import from the generated files.
            process_kwargs[obj.name]= {'class_name': obj.name + '_P'}
            process_rendered, process_model_rendered = self.render_templates(obj)
            self.logger.diagnostic(
                f"Compiling templates:\nProcess:\n{process_rendered}\nProcess Model:\n{process_model_rendered}"
            )
            # Write to file
            self.write_templates(process_rendered, process_model_rendered,obj.name)

    elif self.mode == 'preset':
        processes_list = []
        for obj in self.lava_objects.values():
            # If the Brian object is a neuron group or a spike generator, we generate the lava process from it
            if not isinstance(obj,Synapses):
                process_kwargs[obj.name], proc = self.handle_process_kwargs(obj)
            else:
                # TODO: Currently only the 'pre' pathway is considered. If multiple pre->post pathways are defined, only one will actually be created.
                # So at the moment using pathways is not really necessary, it's only for the sake of UX to let the user know that on_post is not supported.
                for pathway in obj._pathways:
                    if pathway.prepost == 'pre':
                        process_kwargs[obj.name], proc = self.handle_process_kwargs(pathway)
                        # We don't need to feed any variable dictionary since know in advance the port names. (This is thanks to the mode_specific implementation!)
                        self.determine_lava_ports(pathway, {})
                    else:
                        self.logger.warn("Currently Brian2Lava only supports the 'on_pre' condition for synapses specifically with code of the type 'v+=w'.\
                                          Any other condition will be ignored.")
            processes_list.append(proc)
        
        # Now we can find out the optimal shift for the float to fixed transformation
        if self.is_using_f2f():
            F2F.determine_shift_factor()
            # Only after having seen all the parameter values can we perform the float-to-fixed transformation
            for obj in self.lava_objects.values():
                if PresetProcessHandler.requires_float2fixed_converter(obj, self):
                    kwargs = F2F.params_float_to_fixed(params=process_kwargs[obj.name], exceptions=['shape','delta_j','delta_v'])
                    process_kwargs[obj.name] = kwargs
            if self.hardware == HARDWARE.Loihi2:
                for process in processes_list:
                    # Depending on the user defined conditions, generate and save a ucode file
                    # from the template of this process.
                    process.generate_ucode()

    else:
        raise NotImplementedError(f"The selected mode '{self.mode}' does not exist. " +
                                  f"The available combinations of model mode/hardware/number representation are: " +
                                  f"{list(runtime_configs.keys())}. Choices are case-insensitive but correct spelling " +
                                  f"is required.")
    # Run the simulation
    self.run_processes(process_kwargs = process_kwargs)

def handle_process_kwargs(self, obj):
    """
    Gets keyword arguments for specified process object
    -- needed for using preset models (particularly, 
    to run on Loihi).

    Parameters
    ----------
    obj : `lava_object`
        Lava related network object

    Returns
    -------
    kwargs : `dict`
        A dictionary of keyword arguments
    """

    # Instantiate the handler class
    preset_process = PresetProcessHandler(self, obj)
    # Get the required kwargs for this process
    kwargs = preset_process.get_lava_process_kwargs()

    return kwargs, preset_process

# From here on, only useful for flexible mode!===========================================================

def render_templates(self, obj):
    """
    Renders Jinja templates based on Brian network objects that are used in the Lava templates.
    We call them `lava objects`.

    Parameters
    ----------
    obj : lava_object
        Lava related network object
    
    Returns
    -------
    process_rendered : `string`
        A rendered lava `process` template
    process_model_rendered : `string`
        A rendered lava `process model` template
    """
    
    # Extract variables and abstract code
    process_methods, process_model_methods = self.get_compiled_code(obj)
    
    # Log extracted lava code
    s = "Extracted process methods:\n"
    for item in process_methods:
        s += f'{item}\n'
    self.logger.diagnostic(s)

    s = "Extracted process model methods:\n"
    for item in process_model_methods:
        s += f'{item}\n'
    self.logger.diagnostic(s)

    # PROCESS-RELATED CODE ----------------------------------

    # Generate the code required by the init queue
    lava_init_function_calls = self.generate_init_queue(obj)

    # Get the port definitions for process and process model
    proc_ports, proc_model_ports = self.get_lava_ports_definitions(obj)
    
    # Get formatted variables for lava process
    proc_variables_init, proc_variables_lava = self.get_lava_proc_variables(obj)
    
    # Log extracted lava process variables
    s = "Extracted lava process variables:\n"
    for item in proc_variables_lava:
        s += f'{item}\n'
    self.logger.diagnostic(s)
    
    # PROCESS MODEL-RELATED CODE ---------------------------

    # Get formatted variables for lava process **model**
    lava_proc_model_variables = self.get_lava_proc_model_variables(obj)
    
    # Add the port initializations:
    proc_variables_lava = proc_ports + proc_variables_lava
    lava_proc_model_variables = proc_model_ports + lava_proc_model_variables

    # Get a list of ordered function calls to be implemented in
    # the 'run_spk' and 'run_lrn' methods.
    lava_run_function_calls, learning_function_calls = self.get_lava_function_calls(obj)

    # If any additional code for process models was defined, add it 
    additional_code = self.generate_additional_code(obj)

    # If some variables are exclusive to process model and they need initialization:
    proc_model_initialization_code = self.get_proc_model_init_code(obj)

    # If learning is enabled, define the learning guard function
    lrn_guard_code = self.get_lrn_guard_code(obj)

    # Add a single list of all the imports required for process and processmodels
    required_imports = set(collect_required_imports(process_methods))
    required_imports.update(collect_required_imports(process_model_methods))


    # Log extracted lava process variables
    s = "Extracted lava process model variables:\n"
    for item in lava_proc_model_variables:
        s += f'{item}\n'
    self.logger.diagnostic(s)
    
    # Get jinja environment
    env = self.get_jinja_environment()

    # Load and render 'process'
    process_template = env.get_template('process.py.j2')
    process_rendered = process_template.render(
        variables_init=proc_variables_init,
        variables_lava=proc_variables_lava,
        init_calls = lava_init_function_calls,
        init_methods=process_methods,
        required_imports=required_imports,
        name = obj.name
    )
    
    # Load and render 'process model'
    process_model_template = env.get_template('process_model.py.j2')
    process_model_rendered = process_model_template.render(
        additional_code = additional_code,
        proc_model_initialization_code = proc_model_initialization_code,
        methods=process_model_methods,
        run_functions=lava_run_function_calls,
        lrn_functions = learning_function_calls,
        variables=lava_proc_model_variables,
        lrn_guard_code = lrn_guard_code,
        name = obj.name
    )
    
    return process_rendered, process_model_rendered


def get_jinja_environment(self):
    """
    Creates a Jinja environment.

    The environment contains a loader which includes a path to the templates.
    
    Returns
    -------
    env : Environment
        A jinja environment that contains a loader with a path to the Jinja template files
    """
    
    # Get path to templates
    template_path = os.path.join(self.package_root, 'templates')
    
    # Defined Jinja file system loader based on a path to the template files
    loader = FileSystemLoader(searchpath=template_path)
    
    # Return the environment, containing the file loader
    return Environment(
        loader=loader,
        trim_blocks=True,
        lstrip_blocks=True
    )


def get_compiled_code(self, obj):
    """
    Collects the compiled code for lava process and lava process model

    Parameters
    ----------
    obj : lava_object
        Lava related network object

    Returns
    -------
    process_methods : `string[]`
        Process methods to include into the `process`
    process_model_methods : `string[]`
        Process methods to include into the `process model`
    """
    
    # Define variables to collect lava code
    process_methods = ''
    process_model_methods = ''
    
    # We don't want to only consider this 'obj' but also all of its contained objects
    # For example, if delays are defined with an expression, this codeobject is not directly owned by the Synapses.
    objects = [o for o in obj.contained_objects]
    objects.append(obj)
    # Iterate over code objects
    for code_object in self.code_objects.values():
        if code_object.owner in objects:
            lava_code_tmp = None
            for block in ['before_run','run','after_run']:
                # Get compiled code for specific code object and block
                lava_code_tmp = code_object.compiled_code[block]
                
                # Add the code collected from the code objects to either
                # the Lava process or the Lava process model
                if lava_code_tmp is not None:
                    if code_object.template_name in self.init_template_functions:
                        process_methods += lava_code_tmp + '\n\n'
                    else:
                        process_model_methods += lava_code_tmp + '\n\n'

    return process_methods.splitlines(), process_model_methods.splitlines()


def collect_required_imports(code):
    """
    Search for functions in abstract code that require an import (e.g. random function)
    and return these imports as array.
    
    Parameters
    ----------
    code : 'string''
        The whole genrated code as string
    
    Returns
    -------
    required_imports : `string[]`
        Array of strings that contain required imports
    """
    
    # Define potential imports
    potential_imports = {
        'random': 'from random import random',
        'timestep': 'from brian2.core.functions import timestep',
        'LazyArange': 'from brian2.codegen.runtime.numpy_rt.numpy_rt import LazyArange',
        'ceil': 'from brian2.codegen.generators.numpy_generator import ceil_func as ceil',
        'floor': 'from brian2.codegen.generators.numpy_generator import floor_func as floor',
        #'int': 'from numpy import int32 as int', # This is being dealt with by the generator.
        'rand': 'from brian2.codegen.generators.numpy_generator import rand_func as rand',
        'randn': 'from brian2.codegen.generators.numpy_generator import randn_func as randn',
        'poisson': 'from brian2.codegen.generators.numpy_generator import poisson_func as poisson',
        'exprel': 'from brian2.units.unitsafefunctions import exprel',
        'logical_not': 'from numpy import logical_not',
        'sign': 'from numpy import sign',
        'abs': 'from numpy import abs',
        'sqrt': 'from numpy import sqrt',
        'exp': 'from numpy import exp',
        'log': 'from numpy import log',
        'log10': 'from numpy import log10',
        'sin': 'from numpy import sin',
        'cos': 'from numpy import cos',
        'tan': 'from numpy import tan',
        'sinh': 'from numpy import sinh',
        'cosh': 'from numpy import cosh',
        'tanh': 'from numpy import tanh',
        'arcsin': 'from numpy import arcsin',
        'arccos': 'from numpy import arccos',
        'arctan': 'from numpy import arctan',
        'clip': 'from numpy import clip'   
    }
    
    # Create empty array to collect required imports
    required_imports = []
    # Check if relevant function is in the code and if yes, add import
    for func, imp in potential_imports.items():
        for line in code:
            if f'{func}(' in line:
                required_imports.append(imp)
                # avoid multiple imports of the same function
                break
    
    
    return required_imports     

def get_lava_ports_definitions(self, obj):
    """
    TODO

    Parameters
    ----------
    obj : lava_object
        Lava related network object
    
    Returns
    -------
    proc_ports : `string[]`
        A list of code lines that define process ports
    proc_model_ports : `string[]`
        A list of code lines that define process model ports
    """

    proc_ports = []
    proc_model_ports = []
    # Use the information contained in the objects to format the input and output ports
    if isinstance(obj, SpikeSource):
        # Add the spikes_out ports, NOTE that the name has to be compatible with the name used
        # in the SpikeMonitor.
        spike_port = obj.name + '_s_out'
        proc_ports.append(f"self.{spike_port} = OutPort(shape= ({obj.N},))")
        proc_model_ports.append(f"{spike_port}: PyOutPort = LavaPyType(PyOutPort.VEC_DENSE, bool, precision=1)")
        for var in self.lava_ports.values():
            if not obj.name == var['receiver']:
                continue
            portname = var['portname']
            proc_ports.append(f"self.{portname}_in = InPort(shape=(0,))",)
            port_type = 'float' if not 'idx' in portname else 'int,precision = 1'
            proc_model_ports.append(f"{portname}_in: PyInPort = LavaPyType(PyInPort.VEC_DENSE, {port_type})")  
            
    elif isinstance(obj,Synapses):
        # First receive the incoming spikes from the neurons
        for pathway in obj._pathways:
            # Even though we can have more than 2 pathways, source and target are only 2, so at best
            # we'll have one spiking port for presynaptic neurons and one for postsynaptic ones.
            # Since the ports are a set, having duplicates here is not a problem.
            prepost = pathway.prepost
            objname = pathway.objname
            proc_ports.append(f'self.s_in_{prepost} = InPort(shape=(0,))')
            proc_model_ports.append(f"s_in_{prepost}: PyInPort = LavaPyType(PyInPort.VEC_DENSE, bool, precision=1)")

            # Add the receiving mechanism to the process model
            self.proc_model_add_code[obj.name].add(('spike_port',(prepost)))

        # Then make ports for synaptic transmission to neurons
        for var in self.lava_ports.values():
            for pathway in obj._pathways:
                if not var['pathway'] == pathway:
                    continue
                portname = var['portname']
                shape_var = self.get_array_name(obj.variables['_synaptic_pre'], prefix = 'self.init')
                proc_ports.append(f"self.{portname}_out = OutPort(shape = {shape_var}.shape)")
                port_type = 'float' if not 'idx' in portname else 'int,precision = 1'
                proc_model_ports.append(f"{portname}_out: PyOutPort = LavaPyType(PyOutPort.VEC_DENSE, {port_type})")

    # If there are aliases of the same variable, make sure to initialize them only once
    proc_ports = list(set(proc_ports))
    # Add a return just to make the code slightly cleaner
    if len(proc_ports):
        proc_ports[-1] += '\n'
    proc_model_ports = list(set(proc_model_ports))
    if len(proc_model_ports):
        proc_model_ports[-1] += '\n'

    return proc_ports, proc_model_ports


def get_lava_proc_variables(self, obj):
    """
    Takes variable name/value pairs and generates a list of variables
    for the lava process

    Parameters
    ----------
    obj : lava_object
        Lava related network object
    lava_init_function_calls : `string[]`
        A list of strings containing function calls for the process
    
    Returns
    -------
    formatted_variables_init : `string[]`
        A list of code lines that contain variable declarations for the `process`
    formatted_variables_lava : `string[]`
        A list of code lines that contain variable declarations for the `process model`
    """
    
    # Store formatted init variables for a Lava process
    # This contains all variables again, but initialized as plain numpy arrays
    formatted_variables_init = []
    formatted_variables_lava = []

    for name, var_dict in self.lava_variables.items():
        if not var_dict['owner'] == obj.name and not var_dict['owner'] == obj.clock.name:
            continue
        elif var_dict['owner'] == obj.name:
            init_var_name = f'self.init{name}'
            numpy_definition = var_dict['definition']

            # Statement for the definition of an array variable in Lava
            formatted_variables_init.append(f'{init_var_name} = {numpy_definition}')
            
            # Check if Brian provides us with an init function for the variable,
            # that contains instructions to set user-defined initial values
            exp = f'Var(shape={init_var_name}.shape, init={init_var_name})'

        # NOTE: implementing multiple clocks will require checking on each obj.clock.name
        elif var_dict['owner'] == obj.clock.name:
            # Convoluted way to get these variables because from variableview we only get strings which are not usable
            value = obj.clock.variables[var_dict['name']].get_value()[0]
            exp = f'Var(shape= (1,), init = np.array([{value}]))'
        
        # Statement for the definition of an array variable in Lava
        formatted_variables_lava.append(f'self.{name} = {exp}')

    return formatted_variables_init, formatted_variables_lava


def get_lava_proc_model_variables(self, obj):
    """
    Takes variable name/value pairs and generates a list of variables for the lava process model.

    Parameters
    ----------
    obj : lava_object
        Lava related network object
    
    Returns
    -------
    formatted_variables : str[]
        A list of code lines that contain variable declarations
    """
    
    # Init variable to store formatted variables for a Lava process model
    formatted_variables = []
    
    # Then the variables themselves
    for name, var in self.lava_variables.items():
        if var['owner'] == obj.name or var['owner'] == obj.clock.name:
            # Check if array or not
            value_type_arr = 'np.ndarray' if var['size'] > 1 else var['type']

            # Format the expression to what a Lava process expects
            exp = f'LavaPyType({value_type_arr}, {var["type"]})'

            # Statement for the definition of an array variable in Lava
            formatted_variables.append(f'{name}: {value_type_arr} = {exp}')
        
    return formatted_variables


def get_lava_function_calls(self, obj):
    """
    Given the code objects we return an ordered list of function calls that should
    happend within our code. The ordering should be made more customizable

    Parameters
    ----------
    obj : lava_object
        Lava related network object

    Returns
    -------
    init_calls : `string[]`
        A list of code that describes methods for the `process`
    run_calls : `string[]`
        A list of code that describes methods for the `process model`
    """
    run_calls = []
    lrn_calls = []

    # Collect code objects for process
    code_objects = [c_o for c_o in list(self.code_objects.values()) if c_o.owner == obj]
    # Iterate over all code blocks and code objects
    # NOTE: The after_run code blocks are not really used at any point yet. 
    # FIXME: I take them out for now, because their behavior should be implemented differently!
    for block in ['_before_run()', '_run()']:
        for code_obj in code_objects:
            # If the codeobject is not empty, assign function names to related lists
            if code_obj.compiled_code[block[1:-2]] is not None:
                function_name = f'self.{code_obj.name}{block}'
                # These are handled later on by the init queue
                if code_obj.template_name in self.init_template_functions:
                    continue
                elif code_obj.template_name == 'synapses':
                    lrn_calls.append(function_name)
                # These functions handle the simulation and are part of the lava process model
                else:
                    run_calls.append(function_name)
    run_calls = schedule_sort(run_calls, obj)

    # Add a line to update the time variables at each time step
    obj_varnames = obj.variables.keys()
    if 't' in obj_varnames:
        # TODO: this has to be made more generalizable to multiple clocks
        run_calls.append('self._defaultclock_t += self._defaultclock_dt')
    if 't_in_timesteps' in obj_varnames:
        run_calls.append('self._defaultclock_timestep += 1')
    

    return run_calls, lrn_calls

def generate_init_queue(self,obj):
    init_queue_lines = []
    # Also go through the objects contained in the main BrianObject (e.g. Thresholder, Resetter and Stateupdater for NeuronGroup)
    obj_list = [contained_obj for contained_obj in obj.contained_objects]
    # Obviously take the main object into consideration
    obj_list.append(obj)

    # We assume that init queue lines for different objects are independent of each other so the order doesn't matter
    for _obj in obj_list:
        for func, args in self.proc_init_queue[_obj.name]:
            if func == 'code_object':
                codeobj = args
                if not codeobj.template_name in self.init_template_functions:
                    raise ValueError(f"Wrong object in init queue: {codeobj.template_name}")
                init_queue_lines.append(f"self.{codeobj.name}_run()")
            elif func == 'set_by_single_value':
                array_name, item, value = args
                init_queue_lines.append(f"self.init{array_name}[{item}] = {value}")
            elif func == 'set_by_constant':
                array_name, value = args
                init_queue_lines.append(f"self.init{array_name}[:] = {value}")
            elif func == 'set_by_array':
                array_name, input_array = args
                init_queue_lines.append(f"self.init{array_name}[:] = {input_array}")
            elif func == 'resize_array':
                array_name,new_size = args
                init_queue_lines.append(f"self.init{array_name}.resize({new_size})")
            elif func == 'set_array_by_array':
                # TODO: Make sure this is correct!
                array_name, indices, value = args
                init_queue_lines.append(f"self.init{array_name}[{indices}] = {value}")

    return init_queue_lines

def generate_additional_code(self,obj):
    """
    Additional lines of code that might be required for the correct functioning of process models.
    Potentially, even the user could define some code to add here, but this is not supported yet.

    """
    add_code_lines = []
    
    # As for the init queue, consider any possible contained object (this is most likely not necessary but keep for consistency)
    obj_list = [contained_obj for contained_obj in obj.contained_objects]
    obj_list.append(obj)

    for _obj in obj_list:
        for func,args in self.proc_model_add_code[_obj.name]:
            # Read spikes at each timestep from the pre and post pathways
            if func == 'spike_port':
                prepost = args
                # This line is added whether or not a spike queue is present
                add_code_lines.append(f"_spiking_neurons = np.nonzero(self.s_in_{prepost}.recv())[0]")
                spike_queue_owners = [queue['owner'] for queue in self.spike_queues.values()]
                for pathway in obj._pathways:
                    # Process all the pathways with the same 'prepost' in one go.
                    if pathway.prepost == prepost:
                        pathway_name = pathway.objname
                        # Here we read the name of the spike queue from the parent object and the pathway
                        spike_queue = f'{obj.name}_{pathway_name}_spike_queue'
                        # If such a spike queue exists, then we push the spikes to it
                        if spike_queue in self.spike_queues.keys():
                            spike_queue_var = self.spike_queues[spike_queue]['name']
                            add_code_lines.append(f"{spike_queue_var}.push(_spiking_neurons)")
                        # If the pathway doesn't require a spike queue we just read from spike ports
                        else:
                            # TODO: Ideally in future implementations we use get_array_name() for both of these variables..
                            spiking_synapses_var = self.get_array_name(pathway.synapses.variables[f'spiking_{obj.name}_{pathway_name}'])
                            synaptic_pre = self.get_array_name(pathway.synapse_sources)
                            add_code_lines.append(f"{spiking_synapses_var} = [x in _spiking_neurons for x in {synaptic_pre}]")

            # Just to take into account this possibility, even though it is not yet implemented:
            elif func == 'user_code':
                add_code_lines.append([line for line in args])
    
    return add_code_lines

def get_proc_model_init_code(self,obj):
    """
    Potential code to be injected at the beginning of the run_spk function. Used for the initialization of the SpikeQueue.
    We do it here and not in the __init__ method because we want to use variable names and not manually write the delays array to 
    a string. If this is too inefficient it can always be changed later on.
    """

    lines = []
    # At the moment this is only used for synapses (spike queue)
    if not isinstance(obj, Synapses):
        return []
    for name,queue in self.spike_queues.items():
        # If this queue doesn't belong to this object, skip it
        if not obj == queue['owner']:
            continue

        lines.append(f"{queue['name']} = SpikeQueue({queue['start']},{queue['stop']})")
        lines.append(f"{queue['name']}.prepare({queue['delays']},{queue['dt']},{queue['sources']})")
    
    return lines

def get_lrn_guard_code(self,obj):
    """
    Get the definition of the learning phase guard function. This function should return a bool
    indicating whether or not the learning phase should take place during this timestep or not.

    We obtain this by checking if any spike was received by the spiking ports.
    """
    if not isinstance(obj,Synapses):
        return ""
    
    lines = []
    # A trick to optimize writing the required code
    return_stmt = "return False "
    spike_ports = set()
    for pathway in obj._pathways:
        spike_ports.add(pathway.objname)

    for pathwayname in spike_ports:
        spiking_synapses_var = self.get_array_name(obj.variables[f"spiking_{obj.name}_{pathwayname}"])
        lines.append(f"spiking_{pathwayname} = len(np.nonzero({spiking_synapses_var})[0]) > 0")
        return_stmt += f"+ spiking_{pathwayname}"
    lines.append(return_stmt)

    return lines

def schedule_sort(func_list, obj):
    """
    TODO

    Parameters
    ----------
    obj : lava_object
        Lava related network object

    Returns
    -------
    ordered_list
        A list containing the schedule, i.e the order of exectutions for code objects
    """

    from itertools import chain
    from brian2 import CodeRunner
    schedule = {
        'start': [],
        'groups': [],
        'thresholds': [],
        'synapses': [],
        'resets': [],
        'end': []
    }
    for func_call in func_list:
        if not isinstance(obj,CodeRunner):
            code_runner = [item for item in obj.contained_objects if item.name in func_call]
        else:
            # The only supported object which is itself a CodeRunner is the SpikeGeneratorGroup
            assert type(obj) == SpikeGeneratorGroup
            code_runner = [obj]
        
        #If the function doesn't correspond to the contained objects then it must be
        # the activation_processing code object, which doesn't have a corresponding CodeRunner object.
        # NOTE: This might be changed in future updates
        if not len(code_runner):
            # We want to receive the activations and update the neuron at the start of the timestep.
            # NOTE: The various run_ functions from lava might prove useful here in the future.
            assert 'activation_processing' in func_call # or 'synapses_transmit' in func_call
            schedule['synapses'].insert(0, func_call)
            continue

        if not len(code_runner) == 1:
            raise ValueError(f"""More than one CodeRunner corresponding to the same code_object. 
            Try restarting the simulation. If the bug persists please report it to us.
            CodeRunners: {code_runner}""")
        code_runner = code_runner[0]
    
        try:
            schedule[code_runner.when].insert(code_runner.order,func_call)
        # If the keywords 'before' or 'after' are used, we put them at the beginning or end of the 
        # corresponding schedule.
        except KeyError:
            if 'before' in code_runner.when:
                when = code_runner.when.replace("before_","")
                schedule[when].insert(0,func_call)
            elif 'after' in code_runner.when:
                when = code_runner.when.replace("after_", "")
                schedule[when].append(func_call)

    ordered_list = []
    for when in schedule:
        ordered_list = list(chain(ordered_list, schedule[when]))

    return ordered_list
