from brian2.synapses.synapses import SynapticPathway
from brian2.core.functions import Function
from brian2.core.variables import ArrayVariable
import numpy as np
from brian2lava_test.utils.utils import mode_dependent

@mode_dependent
def code_object(
        self,
        owner,
        name,
        abstract_code,
        variables,
        template_name,
        variable_indices,
        codeobj_class=None,
        template_kwds=None,
        override_conditional_write=None,
        compiler_kwds=None
    ):
    """
    Defines a code object.
    This is just a dummy function, the real implementations are 
    code_object_{mode}.

    Parameters
    ----------
    TODO

    Returns
    -------
    codeobj
    """
    raise NotImplementedError()


def code_object_flexible(
        self,
        owner,
        name,
        abstract_code,
        variables,
        template_name,
        variable_indices,
        codeobj_class=None,
        template_kwds=None,
        override_conditional_write=None,
        compiler_kwds=None
    ):
    """
    In the CPU version of this method we need to set up a few things before actually getting to generating the
    code objects. Since the implementation of this method is somewhat intricated, we separate the method depending
    on the hardware in order to help with code maintainability.
    """
    
    # Log when a code object is added
    self.logger.diagnostic(f'Add code_object {name}')
    self.logger.diagnostic(f'Variables gotten from previous steps, {[varname for varname,var in list(variables.items())]}')
    
    # Init template keywords if none were given
    if template_kwds is None:
        template_kwds = dict()
    
    # We define nan as a generic int which hopefully will never appear in a real simulation
    # This is used in synaptic transmission to determine if a synapse is active or not.
    template_kwds["nan"] = -92233720329451

    # In case a variable is set with initial values, we extract the related variable name
    # The variable name is extracted from the abstract code line (before the equal sign)
    # The name is used to get a unique name for the method that initializes the variable
    if template_name in self.init_template_functions:
        # With this we bypass the instructions in the brian base device:
        # (brian2.devices.device -> 328-336)
        # This is because for initialization variables we want to use a different
        # naming convention.
        # Note that this requires renaming the {{variables}} in the template to add the '_init' suffix
        for varname, var in variables.items():
            # NOTE: This might be redundant for simple ArrayVariables, but still relevant for DynamicArrays (or maybe not even for those).
            if isinstance(var, ArrayVariable):
                pointer_name = self.get_array_name(var, prefix = 'self.init')
                if var.scalar:
                    pointer_name += "[0]"
                template_kwds[varname + '_init'] = pointer_name
                if hasattr(var, "resize"):
                    dyn_array_name = self.get_array_name(var, prefix = 'self.init', access_data=False)
                    template_kwds[f"_dynamic_{varname}_init"] = dyn_array_name

    # Taken from CPPStandaloneDevice.code_object()
    do_not_invalidate = set()
    if template_name == "synapses_create_array":
        cache = self.arrays
        if (
            cache[variables["N"]] is None
        ):  # synapses have been previously created with code
            # Nothing we can do
            self.logger.debug(
                f"Synapses for '{owner.name}' have previously been created with "
                "code, we therefore cannot cache the synapses created with arrays "
                f"via '{name}'",
                name_suffix="code_created_synapses_exist",
            )
        else:  # first time we create synapses, or all previous connect calls were with arrays
            cache[variables["N"]][0] += variables["sources"].size
            do_not_invalidate.add(variables["N"])
            for var, value in [
                (
                    variables["_synaptic_pre"],
                    variables["sources"].get_value()
                    + variables["_source_offset"].get_value(),
                ),
                (
                    variables["_synaptic_post"],
                    variables["targets"].get_value()
                    + variables["_target_offset"].get_value(),
                ),
            ]:
                cache[var] = np.append(
                    cache.get(var, np.empty(0, dtype=int)), value
                )
                do_not_invalidate.add(var)

    # In order to properly use synapses we need to be able to access the pathways
    # before they are added to the synapses._pathway variable. Since this variable
    # is only used for this special case, we don't need to store all of the pathways
    # but only the current one, which will then be read by the lava_generator.
    # Note that the template_kwds are NOT available to the CodeGenerator, that's why we do it this way.
    if template_name == 'synapses':
        self._pathway = template_kwds['pathway']
        if not self._pathway.event == 'spike':
            msg = f"""Currently synaptic pathways 'on_pre' and 'on_post' only support spikes as events.
            If handling a different event is a required feature for your model, feel free to make a request on the brian2lava
            repository: https://gitlab.com/brian2lava/brian2lava/-/issues
            Requested event: {self._pathway.event}
            """
            raise NotImplementedError(msg)
    
    # Call code_object method from Brian2 parent device
    codeobj = self.super.code_object(
        owner,
        name,
        abstract_code,
        variables,
        template_name,
        variable_indices,
        codeobj_class=codeobj_class,
        template_kwds=template_kwds,
        override_conditional_write=override_conditional_write,
        compiler_kwds=compiler_kwds
    )
    self.code_objects[codeobj.name] = codeobj

    # This is only used in the pure CPU version where we initialize variables at a later stage
    # Code taken from CPPStandaloneDevice.code_object()
    # Sets the array-cache to None for those variables that are modified
    # by the codeobject in a way which can't be emulated in the array-cache
    template = getattr(codeobj.templater, template_name)
    written_readonly_vars = {
        codeobj.variables[varname] for varname in template.writes_read_only
    } | getattr(owner, "written_readonly_vars", set())
    for var in codeobj.variables.values():
        if (
            isinstance(var, ArrayVariable)
            and var not in do_not_invalidate
            and (not var.read_only or var in written_readonly_vars)
        ):
            self.arrays[var] = None
    
    return codeobj

def code_object_preset(
        self,
        owner,
        name,
        abstract_code,
        variables,
        template_name,
        variable_indices,
        codeobj_class=None,
        template_kwds=None,
        override_conditional_write=None,
        compiler_kwds=None
    ):
    """
    In the Loihi implementation we don't need to do anything, and just let
    the Device class handle the creation of code_objects.
    This is because we don't actually need to use any of the code generated by the device
    for running the simulation itself, since the functionality is already given by Lava.
    """
    # Call code_object method from Brian2 parent device
    codeobj = self.super.code_object(
        owner,
        name,
        abstract_code,
        variables,
        template_name,
        variable_indices,
        codeobj_class=codeobj_class,
        template_kwds=template_kwds,
        override_conditional_write=override_conditional_write,
        compiler_kwds=compiler_kwds
    )
    self.code_objects[codeobj.name] = codeobj

    return codeobj

    
    




