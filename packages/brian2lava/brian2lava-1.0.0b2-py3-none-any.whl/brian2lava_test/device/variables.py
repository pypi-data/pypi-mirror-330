import numpy as np

from brian2.core.variables import Variables
from brian2.units.fundamentalunits import Quantity


def variableview_set_with_index_array(self, variableview, item, value, check_units):
    """
    Is called when a variable is set with a numerical (or slice) index and numerical target value (e.g. G.v[5:] = -70*mV)
    Most of the code is taken from the CPPStandaloneDevice:
    https://github.com/brian-team/brian2/blob/master/brian2/devices/cpp_standalone/device.py#L462

    Parameters
    ----------
    variableview
        Corresponds to `self` within the orginal variableview
    item : `ndarray`
        The indices for the variable (in the context of this `group`).
    value : value
        A Brian value and unit
    check_units : bool, optional
        Whether to check the units of the expression.
    """

    var = variableview.variable
    if isinstance(item, slice) and item == slice(None):
        item = "True"
    value = Quantity(value)

    # Case of scalar value
    if (
        isinstance(item, int) or (isinstance(item, np.ndarray) and item.shape == ())
    ) and value.size == 1:
        array_name = self.get_array_name(var, access_data=False)
        value_str = np.asarray(value).item(0)
        # Modify the value stored in the array-cache
        if self.arrays.get(var, None) is not None:
            self.arrays[var][item] = value
        
        # CPU specific handling
        if self.mode == 'flexible':
            # For a single assignment, generate a code line instead of storing the array
            self.proc_init_queue[var.owner.name].append(
                ("set_by_single_value", (array_name, item, value_str))
            )

    # Simple case where we don't have to do any indexing
    elif item == "True" and variableview.index_var in ("_idx", "0"):
        self.fill_with_array(var, value)
    else:
        # We have to calculate indices. This will not work for synaptic
        # variables
        try:
            indices = np.asarray(
                variableview.indexing(item, index_var=variableview.index_var)
            )
        except NotImplementedError:
            raise NotImplementedError(
                f"Cannot set variable '{variableview.name}' "
                "this way in standalone, try using "
                "string expressions."
            )
        arrayname = self.get_array_name(var, access_data=False, prefix = None)

        if indices.shape != () and (value.shape == () or (value.size == 1 and indices.size > 1)):
            value = np.repeat(value, indices.size)

        elif value.shape != indices.shape and len(value) != len(indices):
            raise ValueError(
                "Provided values do not match the size "
                "of the indices, "
                f"{len(value)} != len(indices)."
            )
        
        if self.mode == 'flexible':
            # In this case the value can't be computed until running the simulation, so we don't store it
            self.arrays[var] = None
            
            value_str = np.array2string(value, separator = ',')
            indices_str = np.array2string(indices, separator= ',')
            self.proc_init_queue[var.owner.name].append(
                (
                    "set_array_by_array",
                    (arrayname, indices_str, value_str),
                )
                )
        else:
            var.get_value()[indices] = value


def variableview_set_with_expression_conditional(self, variableview, cond, code, run_namespace, check_units=True):
    """
    Is called when a variable is set with a string index and a string expression value (e.g. G.v['i>5'] = (-70+i)*mV)

    Parameters
    ----------
    variableview 
        Corresponds to `self` within the orginal variableview
    cond : str
        The string condition for which the variables should be set.
    code : str
        The code that should be executed to set the variable values.
        Can contain references to indices, such as `i` or `j`
    run_namespace : dict-like, optional
        An additional namespace that is used for variable lookup (if not
        defined, the implicit namespace of local variables is used).
    check_units : bool, optional
        Whether to check the units of the expression.
    """

    variable = variableview.variable
    if variable.scalar and cond != "True":
        raise IndexError(
            f"Cannot conditionally set the scalar variable '{variableview.name}'."
        )
    abstract_code_cond = f"_cond = {cond}"
    abstract_code = f"{variableview.name} = {code}"
    variables = Variables(None)
    variables.add_auxiliary_variable("_cond", dtype=bool)
    from brian2.codegen.codeobject import create_runner_codeobj

    # TODO: Have an additional argument to avoid going through the index
    # array for situations where iterate_all could be used

    codeobj = create_runner_codeobj(
        variableview.group,
        {"condition": abstract_code_cond, "statement": abstract_code},
        "group_variable_set_conditional",
        additional_variables=variables,
        check_units=check_units,
        run_namespace=run_namespace,
        codeobj_class=self.code_object_class(
            fallback_pref="codegen.string_expression_target"
        ),
    )

    # Mode specific handling
    if self.mode == 'flexible':
        # Add the codeobject to the initialization queue for its owner process
        self.proc_init_queue[variable.owner.name].append(('code_object',codeobj))
    else:
        codeobj()


def variableview_set_with_expression(self, variableview, item, code, run_namespace, check_units=True):
    """
    Sets a variable using a string expression. Is called by `VariableView.set_item` for statements such as
    ``S.var[:, :] = 'exp(-abs(i-j)/space_constant)*nS'``.

    Parameters
    ----------
    variableview
        Corresponds to `self` within the orginal variableview
    item : `ndarray`
        The indices for the variable (in the context of this `group`).
    code : str
        The code that should be executed to set the variable values.
        Can contain references to indices, such as `i` or `j`
    run_namespace : dict-like, optional
        An additional namespace that is used for variable lookup (if not
        defined, the implicit namespace of local variables is used).
    check_units : bool, optional
        Whether to check the units of the expression.
    """

    # Some fairly complicated code to raise a warning in ambiguous
    # situations, when indexing with a group. For example, in:
    #   group.v[subgroup] =  'i'
    # the index 'i' is the index of 'group' ("absolute index") and not of
    # subgroup ("relative index")
    if hasattr(item, "variables") or (
        isinstance(item, tuple)
        and any(hasattr(one_item, "variables") for one_item in item)
    ):
        # Determine the variables that are used in the expression
        from brian2.codegen.translation import get_identifiers_recursively

        identifiers = get_identifiers_recursively([code], variableview.group.variables)
        variables = variableview.group.resolve_all(
            identifiers, run_namespace, user_identifiers=set()
        )
        if not isinstance(item, tuple):
            index_groups = [item]
        else:
            index_groups = item

        for varname, var in variables.items():
            for index_group in index_groups:
                if not hasattr(index_group, "variables"):
                    continue
                if (
                    varname in index_group.variables
                    or var.name in index_group.variables
                ):
                    indexed_var = index_group.variables.get(
                        varname, index_group.variables.get(var.name)
                    )
                    if indexed_var is not var:
                        self.logger.warn(
                            "The string expression used for setting "
                            f"'{variableview.name}' refers to '{varname}' which "
                            "might be ambiguous. It will be "
                            "interpreted as referring to "
                            f"'{varname}' in '{variableview.group.name}', not as "
                            "a variable of a group used for "
                            "indexing.",
                            "ambiguous_string_expression",
                        )
                        break  # no need to warn more than once for a variable
    
    indices = np.atleast_1d(variableview.indexing(item))
    abstract_code = f"{variableview.name} = {code}"
    variables = Variables(variableview.group)

    # Get number of set variable indices to be able to set unique names
    counter = len(self.set_variable_index_names)+1
    # Get group idx name for current index iteration
    idx_name = f'_group_idx_{variableview.name}_{counter}'

    # Add group idx variable
    # This function is part of the Variables class, but also calles get_array_name at some point
    variables.add_array(idx_name, size=len(indices), dtype=np.int32, values=indices)

    # Add the new group idx name to an array (needed for the counter)
    self.set_variable_index_names.append(variables._variables[idx_name])

    # Needs to be added to namespace, since group still requires the original name '_group_idx'
    # The specific reason for that is unknown ;)
    run_namespace['_group_idx'] = variables._variables[idx_name]

    # TODO: Have an additional argument to avoid going through the index
    # array for situations where iterate_all could be used
    from brian2.codegen.codeobject import create_runner_codeobj

    codeobj = create_runner_codeobj(
        variableview.group,
        abstract_code,
        "group_variable_set",
        additional_variables=variables,
        check_units=check_units,
        run_namespace=run_namespace,
        codeobj_class=self.code_object_class(
            fallback_pref="codegen.string_expression_target"
        ),
    )

    # Mode specific handling
    if self.mode == 'flexible':
        # Add the codeobject to the initialization queue for its owner process
        self.proc_init_queue[variableview.variable.owner.name].append(('code_object',codeobj))
    else:
        codeobj()
