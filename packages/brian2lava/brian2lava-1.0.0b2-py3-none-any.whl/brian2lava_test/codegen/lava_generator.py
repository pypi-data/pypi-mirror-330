import itertools

import numpy as np

from brian2.parsing.bast import brian_dtype_from_dtype
from brian2.parsing.rendering import NumpyNodeRenderer
from brian2.core.functions import DEFAULT_FUNCTIONS, timestep
from brian2.core.variables import Constant, ArrayVariable
from brian2.utils.stringtools import get_identifiers, word_substitute, indent
from brian2.utils.logger import get_logger
from brian2.core.functions import Function
from brian2.groups.neurongroup import NeuronGroup
from brian2.synapses.synapses import Synapses
from brian2.units.unitsafefunctions import exprel

from brian2.codegen.generators.base import CodeGenerator


# TODO remove, only for development
from pprint import pprint


__all__ = ['LavaCodeGenerator']


logger = get_logger(__name__)

class VectorisationError(Exception):
    """
    Vectorisation error is used in the code generator
    """

    pass


class LavaCodeGenerator(CodeGenerator):
    """
    Generates Lava code.
    
    Notes
    -----
    Essentially Python but vectorised. It is similar to `NumpyCodeGenerator`, but contains modifications.
    """

    # Define some class variables
    class_name = 'lava'
    _use_ufunc_at_vectorisation = True  # allow this to be off for testing only


    def translate_expression(self, expr):
        """
        Translate an abstract code expression to the right of an operator to Python code.
        """

        expr = word_substitute(expr, self.func_name_replacements)
        translated_expr = NumpyNodeRenderer(auto_vectorise=self.auto_vectorise).render_expr(expr, self.variables).strip()
        return translated_expr


    def translate_statement(self, statement):
        """
        Translates abtract code statements to Python code.

        Parameters
        ----------
        statement
            A statement containing the variable, operation, expression and comment.

        Returns
        -------
        `str`
            Compiled code
        """

        # TODO: optimisation, translate arithmetic to a sequence of inplace
        # operations like a=b+c -> add(b, c, a)
        var, op, expr, comment = (statement.var, statement.op, statement.expr, statement.comment)
        if op == ':=':
            op = '='
        # For numpy we replace complex expressions involving a single boolean variable into a
        # where(boolvar, expr_if_true, expr_if_false)
        if (statement.used_boolean_variables is not None and len(statement.used_boolean_variables)==1
                and brian_dtype_from_dtype(statement.dtype)=='float'
                and statement.complexity_std>sum(statement.complexities.values())):
            used_boolvars = statement.used_boolean_variables
            bool_simp = statement.boolean_simplified_expressions
            boolvar = used_boolvars[0]
            for bool_assigns, simp_expr in bool_simp.items():
                _, boolval = bool_assigns[0]
                if boolval:
                    expr_true = simp_expr
                else:
                    expr_false = simp_expr
            code = f'{var} {op} _numpy.where({boolvar}, {expr_true}, {expr_false})'
        else:
            code = f"{var} {op} {self.translate_expression(expr)}"
        if len(comment):
            code += f" # {comment}"
        
        return code


    def ufunc_at_vectorisation(
            self, statement, variables, indices,
            conditional_write_vars, created_vars, used_variables
        ):
        """
        TODO
        """

        if not self._use_ufunc_at_vectorisation:
            raise VectorisationError()
        # Avoids circular import
        from brian2.devices.device import device

        # See https://github.com/brian-team/brian2/pull/531 for explanation
        used = set(get_identifiers(statement.expr))
        used = used.intersection(k for k in list(variables.keys()) if k in indices and indices[k]!='_idx')
        used_variables.update(used)
        if statement.var in used_variables:
            raise VectorisationError()
        expr = NumpyNodeRenderer(auto_vectorise=self.auto_vectorise).render_expr(statement.expr)

        if statement.op == ':=' or indices[statement.var] == '_idx' or not statement.inplace:
            if statement.op == ':=':
                op = '='
            else:
                op = statement.op
            line = f'{statement.var} {op} {expr}'
        elif statement.inplace:
            if statement.op == '+=':
                ufunc_name = '_numpy.add'
            elif statement.op == '*=':
                ufunc_name = '_numpy.multiply'
            elif statement.op == '/=':
                ufunc_name = '_numpy.divide'
            elif statement.op == '-=':
                ufunc_name = '_numpy.subtract'
            else:
                raise VectorisationError()
            array_name = device.get_array_name(variables[statement.var])
            idx = indices[statement.var]
            line = f'{ufunc_name}.at({array_name}, {idx}, {expr})'
            line = self.conditional_write(line, statement, variables,
                conditional_write_vars=conditional_write_vars, created_vars=created_vars)
        else:
            raise VectorisationError()

        if len(statement.comment):
            line += f" # {statement.comment}"

        return line


    def vectorise_code(self, statements, variables, variable_indices, index='_idx'):
        """
        Translates abtract code statements to vectorized Python code.

        Parameters
        ----------
        statements
            Statements containing the corresponding variable, operation, expression and comment.
        variables
            All variables to compile.
        variable_indices
            If a statement only applies to a subset of the variable (e.g. a subset of a list).
            The subset of the variable is chosen by indices, given by `variable_indices`.
        index
            Name of the index variable. Default: `_idx`

        Returns
        -------
        `str`
            Lines of compiled code
        """

        created_vars = {stmt.var for stmt in statements if stmt.op == ':='}
        try:
            lines = []
            used_variables = set()
            for statement in statements:
                lines.append(f'#  Abstract code:  {statement.var} {statement.op} {statement.expr}')
                # We treat every statement individually with its own read and write code
                # to be on the safe side
                read, write, indices, conditional_write_vars = self.arrays_helper([statement])
                # We make sure that we only add code to `lines` after it went
                # through completely
                ufunc_lines = []
                # No need to load a variable if it is only in read because of
                # the in-place operation
                if (statement.inplace and
                            variable_indices[statement.var] != '_idx' and
                            statement.var not in get_identifiers(statement.expr)):
                    read = read - {statement.var}
                ufunc_lines.extend(
                    self.read_arrays(read, write, indices, variables, variable_indices)
                )
                ufunc_lines.append(
                    self.ufunc_at_vectorisation(
                        statement, variables, variable_indices, conditional_write_vars,
                        created_vars, used_variables,
                    )
                )
                # Do not write back such values, the ufuncs have modified the
                # underlying array already
                if statement.inplace and variable_indices[statement.var] != '_idx':
                    write = write - {statement.var}
                ufunc_lines.extend(
                    self.write_arrays([statement], read, write, variables, variable_indices)
                )
                lines.extend(ufunc_lines)
        except VectorisationError:
            if self._use_ufunc_at_vectorisation:
                logger.info("Failed to vectorise code, falling back on Python loop: note that "
                            "this will be very slow! Switch to another code generation target for "
                            "best performance (e.g. cython). First line is: "+str(statements[0]),
                            once=True)
            lines = []
            lines.extend(['_full_idx = _idx',
                          'for _idx in _full_idx:',
                          '    _vectorisation_idx = _idx'
                          ])
            read, write, indices, conditional_write_vars = self.arrays_helper(statements)
            lines.extend(indent(code) for code in
                         self.read_arrays(read, write, indices,
                                          variables, variable_indices))
            for statement in statements:
                line = self.translate_statement(statement)
                if statement.var in conditional_write_vars:
                    lines.append(indent(f'if {conditional_write_vars[statement.var]}:'))
                    lines.append(indent(line, 2))
                else:
                    lines.append(indent(line))
            lines.extend(indent(code) for code in
                         self.write_arrays(statements, read, write,
                                           variables, variable_indices))
            
        return lines


    @staticmethod
    def get_array_name(var, access_data=True, template_name=None):
        """
        Returns a variable name used in the template
        Specifically differentiates between the usage of init and lava variables
        It uses the devices `get_array_name` method

        Notes
        -----
        It is important that this function has the name 'get_array_name', since it is also called by
        internal Brian functions and overwrites the default 'get_array_name' in CodeGenerator
        """

        # We have to do the import here to avoid circular import dependencies
        from brian2.devices.device import get_device
        # Get device
        device = get_device()

        # Template name is not specified
        if template_name is None:
            # '_group_idx' is a special case, see e.g. 'group_variable_set.py_'
            # We assume that '_group_idx' is only used in *process* related templates
            if '_group_idx' in var.name:
                return device.get_array_name(var, access_data, prefix='self.init')
            else:
                return device.get_array_name(var, access_data)
        # If variable is related to a template that is used in *process*
        elif template_name in device.init_template_functions:
            return device.get_array_name(var, access_data, prefix='self.init')
        # if variable is related to a template that is used in *process model*
        else:
            return device.get_array_name(var, access_data)


    def read_arrays(self, read, write, indices, variables, variable_indices):
        """
        Create statements that read from array.

        Parameters
        ----------
        read
            Arrays names to read from.
        write
            Arrays names to write to.
        indices
            Indices of arrays to read from.
        variables
            Actual variables that can be selected by variable names (e.g. contained in `read`).
        variable_indices
            Indices to choose ranges from the variables.

        Returns
        -------
        `str`
            Lines of compiled code
        """

        # index and read arrays (index arrays first)
        lines = []
        for varname in itertools.chain(indices, read):
            var = variables[varname]
            index = variable_indices[varname]
            if self.template_name == 'activation_processing' and 'synapses' in var.owner.name:
                line = f"{varname} = {varname}_received"
            else:
                line = f"{varname} = {self.get_array_name(var, template_name = self.template_name)}"
            
            if index not in self.iterate_all:
                line += f"[{index}]"
            elif varname in write:
                # avoid potential issues with aliased variables, see github #259
                line += '.copy()'
            lines.append(line)

        return lines


    def write_arrays(self, statements, read, write, variables, variable_indices):
        """
        Create statements that write to array.

        Parameters
        ----------
        statements
            Statements containing the corresponding variable, operation, expression and comment.
        read
            Arrays names to read from.
        write
            Arrays names to write to.
        variables
            Actual variables that can be selected by variable names (e.g. contained in `write`).
        variable_indices
            Indices to choose ranges from the variables.

        Returns
        -------
        `str`
            Lines of compiled code
        """

        lines = []
        for varname in write:
            var = variables[varname]
            index_var = variable_indices[varname]
            # check if all operations were inplace and we're operating on the
            # whole vector, if so we don't need to write the array back
            if index_var not in self.iterate_all or varname in read:
                all_inplace = False
            else:
                all_inplace = True
                for stmt in statements:
                    if stmt.var == varname and not stmt.inplace:
                        all_inplace = False
                        break
            if not all_inplace:
                line = self.get_array_name(var, template_name = self.template_name)

                if index_var in self.iterate_all:
                    line = f"{line}[:]"
                else:
                    line = f"{line}[{index_var}]"
                line = f"{line} = {varname}"
                lines.append(line)

        return lines


    def conditional_write(self, line, stmt, variables, conditional_write_vars, created_vars):
        """
        TODO
        """

        if stmt.var in conditional_write_vars:
            subs = {}
            index = conditional_write_vars[stmt.var]
            # we replace all var with var[index], but actually we use this repl_string first because
            # we don't want to end up with lines like x[not_refractory[not_refractory]] when
            # multiple substitution passes are invoked
            # FIXME let's have another look at this at some point
            repl_string = '#$(@#&$@$*U#@)$@(#'  # this string shouldn't occur anywhere I hope! :)
            for varname, var in list(variables.items()):
                if isinstance(var, ArrayVariable) and not var.scalar:
                    subs[varname] = f"{varname}[{repl_string}]"
            # all newly created vars are arrays and will need indexing
            for varname in created_vars:
                subs[varname] = f"{varname}[{repl_string}]"
            # Also index _vectorisation_idx so that e.g. rand() works correctly
            subs['_vectorisation_idx'] = f"_vectorisation_idx[{repl_string}]"

            line = word_substitute(line, subs)
            line = line.replace(repl_string, index)

        return line
    
    def check_for_brian2lava_support(self,scalar_statements,vector_statements):
        """
        Check some features of the codeobject to be generated to make sure that brian2lava supports these operations
        """
        from brian2 import get_device

        # Conditions like: S.connect('v_pre!=v_post') are not supported
        # Go through all the variables used in the statements and make sure they don't belong to NeuronGroups
        if 'synapses_create' in self.template_name:
            created_vars = set()
            # In the scalar statements we only collect possible created scalar variables (useful for differential equations)
            for name,statements in scalar_statements.items():
                created_vars = created_vars.union({stmt.var for stmt in statements if stmt.op == ':='})
            # We only care about vector statements in this case
            for name,statements in vector_statements.items():
                created_vars = created_vars.union({stmt.var for stmt in statements if stmt.op == ':='})
                for stmt in statements:
                    vars_str = [stmt.var]
                    vars_str.extend([id for id in get_identifiers(stmt.expr)])
                    for var_str in vars_str:
                        # Created vars are not a problem, they're handled by the generator
                        if var_str in created_vars:
                            continue

                        var = self.variables[var_str]
                        # Vars without an owner are not a problem, they will be added as constants
                        if not hasattr(var,"owner"):
                            continue

                        if isinstance(var.owner,NeuronGroup) and not isinstance(var,Constant):
                            msg = """Initializing Synapses with variables from other objects is currently not supported.
                            For example:
                            Synapses.connect('v_pre!=v_post')
                            Will raise this error if v_pre and v_post belong to a NeuronGroup.
                            """
                            raise NotImplementedError(msg)


    def translate_statement_sequence(self, scalar_statements, vector_statements):
        """
        Takes lines of code and defines Jinja variables, stored in Python dictionaries.

        Parameters
        ----------
        scalar_statements
            Lines of code containing *scalar* statements.
        vector_statements
            Lines of code containing *vector* statements.

        Returns
        -------
        scalar_code : `dict`
            Jinja variables containing compiled *scalar* code.
        vector_code : `dict`
            Jinja variables containing compiled *vector* code.
        kwds : `dict`
            Jinja variables containing additional custom variables (so called 'keywords').
        """

        # First make sure we can handle this codeobject
        self.check_for_brian2lava_support(scalar_statements, vector_statements)

        # If we're dealing with synapses, we buffer the translation and manage their two functions separately
        if self.template_name == 'synapses':
            # Get the statements which are only related to synapses (the neuronal part of transmission is handled by another template)
            scalar_statements,vector_statements = self.manage_neuron_activations(scalar_statements,vector_statements)

            # Use these statements to manage synaptic transmission
            self.manage_synaptic_behavior(scalar_statements,vector_statements)
            
        scalar_code = {}
        vector_code = {}
        for name, block in scalar_statements.items():
            scalar_code[name] = self.translate_one_statement_sequence(
                block, scalar=True
            )
        for name, block in vector_statements.items():
            vector_code[name] = self.translate_one_statement_sequence(
                block, scalar=False
            )

        kwds = self.determine_keywords()

        return scalar_code, vector_code, kwds


    def translate_one_statement_sequence(self, statements, scalar=False):
        """
        Translate an abstract code statement sequence to Python code.

        Parameters
        ----------
        statements
            Statements containing the corresponding variable, operation, expression and comment.
        scalar: `bool`
            Indicates if the statements shall be scalar or vectorized.

        Returns
        -------
        lines : `str[]`
            List of compiled code lines.
        """
        # For synapses learning, we want to add a # EMPTY_CODE_BLOCK indicator when
        # the vector learning statements are empty. This means that the codeobject will not be compiled.
        if self.template_name == 'synapses' and len(statements) == 0 and not scalar:
            return ['# EMPTY_CODE_BLOCK']

        variables = self.variables
        variable_indices = self.variable_indices

        read, write, indices, conditional_write_vars = self.arrays_helper(statements)
        lines = []
        all_unique = not self.has_repeated_indices(statements)
        if scalar or all_unique:
            # Simple translation
            lines.extend(self.read_arrays(read, write, indices, variables, variable_indices))
            created_vars = {stmt.var for stmt in statements if stmt.op == ':='}
            for stmt in statements:
                line = self.translate_statement(stmt)
                line = self.conditional_write(line, stmt, variables, conditional_write_vars, created_vars)
                lines.append(line)
            lines.extend(self.write_arrays(statements, read, write, variables, variable_indices))
        else:
            # More complex translation to deal with repeated indices
            lines.extend(self.vectorise_code(statements, variables, variable_indices))
        
        # TODO: There might be a better way to add this..
        # We treat the case of int() calls in a special way since importing
        # the numpy.int32 function as int() would overwrite the Python int type
        tmp = []
        for line in lines:
            if 'int(' in line:
                line = line.replace('int(', '_numpy.int32(')
            tmp.append(line)
        lines = tmp

        return lines


    def manage_neuron_activations(self, scalar_statements, vector_statements):
        """
        Manages the transmission of synaptic variables to neurons and creates a code object to handle
        the effect of synaptic transmission on neurons.
        NOTE: This method strongly relies on the device, but also on the variables stored in the generator
        so we have to choose whether this method should be used by the LavaGenerator or by the device itself..

        Parameters
        ----------
        statements: list(Statement) 
            A list of the statements search through for statemtents related to synaptic transmission

        Returns:
        --------
        synapse_statements: list(Statement)
            A list of the statements which are purely internal to synapses, i.e. statements related to 
            learning rules. These statements are then processed by the usual pipeline.
        """

        from brian2 import get_device
        device = get_device()
        # The pathway will have been stored by the device at this point (see device.codeobject())
        pathway = device._pathway

        # Collect scalar and vector statements related to synapses
        synapse_scalar_statements = {name:[] for name in scalar_statements}
        synapse_vector_statements = {name:[] for name in vector_statements}

        # Collect scalar and vector statements related to neurons
        neuron_scalar_statements = {name:[] for name in scalar_statements}
        neuron_vector_statements = {name:[] for name in vector_statements}

        # Also copy the needed variables (having some extra ones is not a problem)
        neuron_statement_variables = self.variables
        neuron_created_vars = []
        # For the next part we don't need to distinguish between statement types
        all_statements = list(itertools.chain.from_iterable(scalar_statements.values())) + list(itertools.chain.from_iterable(vector_statements.values()))
        # Check stmt.var is a created var. If it is, check if there is another stmt in which the var belongs to a neuron
        # and the stmt.expr identifiers (you get them from get_identifiers(stmt.expr)) contain the created stmt.var. If so append the original var to neuron_created_vars
        created_vars = {stmt.var for stmt in all_statements if stmt.op == ':='}
        for stmt in all_statements:
            if stmt.var in created_vars:
                for other_stmt in all_statements:
                    if other_stmt.var not in created_vars and isinstance(self.variables[other_stmt.var].owner,NeuronGroup):
                        identifiers = get_identifiers(other_stmt.expr)
                        if stmt.var in identifiers:
                            neuron_created_vars.append(stmt.var)
                            break

        # We have to deal with both scalar and vector statements (even though in most cases scalar statements are empty)
        for name, block in scalar_statements.items():
            # This potentially is useless, but keep it for now.
            created_vars = {stmt.var for stmt in block if stmt.op == ':='}
            for stmt in block:
                if stmt.var in created_vars:
                    if stmt.var in neuron_created_vars:
                        # Make the operator a simple '=' since the := operator is not recognized by the 
                        # brian parser.
                        stmt.op = '='
                        neuron_scalar_statements[name].append(stmt)
                    # If it wasn't created for the neuron it goes in the synaptic statements
                    synapse_scalar_statements[name].append(stmt)
                    continue
                var = self.variables[stmt.var]
                if isinstance(var.owner,NeuronGroup):
                    neuron_scalar_statements[name].append(stmt)
                    continue
                synapse_scalar_statements[name].append(stmt)

        for name, block in vector_statements.items():
            # Collecting all of the created vars.
            created_vars = {stmt.var for stmt in block if stmt.op == ':='}
            for stmt in block:
                # We don't copy subexpressions, because they are handled internally in brian
                if stmt.subexpression:
                    continue
                # Again the created vars are added to the statements if they are used by the neuron statements
                if stmt.var in created_vars:
                    if stmt.var in neuron_created_vars:
                        stmt.op = '='
                        neuron_vector_statements[name].append(stmt)
                    # If it wasn't created for the neuron it goes in the synaptic statements
                    synapse_vector_statements[name].append(stmt)
                    continue
                var = self.variables[stmt.var]
                if isinstance(var.owner,NeuronGroup):
                    neuron_vector_statements[name].append(stmt)
                    continue
                synapse_vector_statements[name].append(stmt)
        

        # Store the requirements for the synaptic connections in Lava
        device.determine_lava_ports(pathway,neuron_statement_variables)
        
        # Create the 'activation_processing' codeobject handling synaptic effects on neurons
        all_neuron_statements = [statement for block in neuron_scalar_statements.values() for statement in block]
        all_neuron_statements += [statement for block in neuron_vector_statements.values() for statement in block]
        
        code_str = '\n'.join([stmt.var+stmt.op+str(stmt.expr) for stmt in all_neuron_statements])
        abstract_code = {None: code_str}

        codeobj_name = pathway.target.name +'_'+ self.owner.name + '_' + pathway.objname + '_' + 'activation_processing'
        # TODO: Check whether this kwd is actually required or not, for now I'll stay on the safe side
        kwds = {'pathway': pathway}
        # TODO: Figure out if it's better to use this function or 'create_runner_object()'
        device.code_object(
            owner= pathway.target,
            name = codeobj_name,
            abstract_code = abstract_code,
            variables = neuron_statement_variables,
            template_name = 'activation_processing',
            variable_indices = self.variable_indices,
            template_kwds=kwds,
            override_conditional_write=self.override_conditional_write
        )

        return synapse_scalar_statements,synapse_vector_statements


    def manage_synaptic_behavior(self, scalar_statements, vector_statements):
        """
        This method manages the two main code objects related to synaptic behavior: synapses_transmit and synapses.

        Parameters
        ----------
        synapses_transmit:
            handles the signal transmission of the selected variables along the pathway (pre->post or post->pre).
            This code object is created by the device.
        synapses:
            handles the learning rules and the synaptic plasticity.
            The code object is created by the LavaGenerator by following the usual pipeline.
            Here we only check if the learning rules defined by the user are valid.
        """

        vars_from_expr = []
        # TODO: This here is not good, we'll have to figure out a proper way to do this
        from brian2 import Clock, get_device
        device = get_device()
        accepted_owners = [type(None),Clock, type(self.owner)]
        # Group all the statements in one variable
        all_statements = scalar_statements.copy()
        all_statements.update(vector_statements.copy())

        # Go through all the statements and check if the variables are local to the synapses object
        for statements in all_statements.values():
            created_vars = {stmt.var for stmt in statements if stmt.op == ':='}
            for stmt in statements:
                # Again skip created_vars since they're an exception
                if stmt.var in created_vars:
                    continue
                if hasattr(self.variables[stmt.var],'owner') and not self.variables[stmt.var].owner == self.owner:
                    raise ValueError(f"The variable in this learning statement does not belong to synapses: {stmt}") 
                vars_to_append = [self.variables[id] for id in get_identifiers(stmt.expr) if not id in created_vars and hasattr(self.variables[id],'owner')]
                vars_from_expr = itertools.chain(vars_from_expr,vars_to_append)

        for var in vars_from_expr:
            cond = any([isinstance(var.owner, obj) for obj in accepted_owners])
            if  not cond:
                msg = f"""Learning rules requiring variables which are not strictly local to synapses is currently not supported.
                Define all variables required for learning inside the Synapses object or as constants. The var {var.name} belongs to {var.owner}
                and not to {self.owner}
                """
                raise ValueError(msg)

        # Generate the codeobject needed for synaptic transmission. It doesn't need any code as the functionality is included in the template.
        objname = device._pathway.objname
        codeobj_name = f'{self.owner.name}_{objname}_synapses_transmit'
        device.code_object(
            owner= self.owner,
            name = codeobj_name,
            abstract_code = {None: ''},
            variables = self.variables,
            template_name = 'synapses_transmit',
            variable_indices = self.variable_indices,
            template_kwds={'pathway': device._pathway},
            override_conditional_write=self.override_conditional_write
        )


    def determine_keywords(self):
        """
        Adds custom variables to the Jinja templates
        """

        from brian2 import get_device
        device = get_device()
        # Keywords dictionary, by default it only contains the name of the method.
        kwds = {'name': self.name}

        # Add constants to template keywords
        # TODO Francesco: I'm wondering if this is the correct way to add the 'USES_VARIABLES' from templates
        # check: https://github.com/brian-team/brian2/blob/3cf65d4c5c8fa1512cf0a6deb515a8cdc81ae9e5/brian2/codegen/templates.py (186-217)
        # It seems that the templates themselves should take care of this. Further investigation is needed.
        constants = []
        for varname,var in self.variables.items():
            if isinstance(var, Constant):
                constants.append(f'{varname} = {var.get_value()}')
                                                                    # Owner should be same as generator, except for SynapticPathays
            elif isinstance(var, ArrayVariable) and var.constant and (var.owner == self.owner or hasattr(self.owner,'synapses')):
                # TODO This has to be handled differently. For the moment we just avoid adding these to the template constants.
                if 'synapses' in self.template_name and (varname == '_synaptic_pre' or varname == '_synaptic_post'):
                    continue 
                constants.append(f'{varname} = {self.get_array_name(var,template_name=self.template_name)}')
            kwds['constants'] = constants

        # This is only needed for the templates related to pathways
        if self.template_name == 'synapses' or self.template_name == 'synapses_transmit':
            # TODO: there might be a better way to access this value
            pathway = device._pathway
            kwds['prepost'] = pathway.prepost
            synapses_name = self.owner.name
            kwds['spiking_synapses'] = self.get_array_name(self.owner.variables[f"spiking_{synapses_name}_{pathway.objname}"])
        
        # This could be incorporated above, but I want to make it clear that it's only used in this template
        if self.template_name == 'synapses_transmit':
            pathway = device._pathway
            # TODO: This is a bit ugly, but since spike queues don't function properly if no delays are defined,
            #  we have to define two different pipelines for each case.
            # Add the spike queue variable name, used in synapses_transmit template if delays are defined
            try:
                spike_queue = device.spike_queues[f'{synapses_name}_{pathway.objname}_spike_queue']['name']
                # We use this form because we want to keep the spiking_synapses variable to a fixed length otherwise lava will complain
                kwds['read_spikes'] = f"np.isin(np.arange(len({self.get_array_name(pathway.synapse_sources)})),{spike_queue}.peek())"
                kwds['advance_queue'] = spike_queue + '.advance()'
            # Otherwise, we simply read from the spike ports.
            except KeyError:
                spiking_synapses = self.get_array_name(self.owner.variables[f'spiking_{self.owner.name}_{pathway.objname}'])
                kwds['read_spikes'] = spiking_synapses
                kwds['advance_queue'] = ''


        # Read the required synaptic variables which are to be sent to neurons
        # and send them out through the correct port.
        if self.template_name == 'synapses_transmit':  
            read_syn_vars = []
            syn_output_vars = []
            syn_output_ports = []          
            ports = device.lava_ports
            for port in ports.values():
                if not port['pathway'].synapses == self.owner or not port['varname'] in list(self.variables.keys()) or port['pathway'].objname not in self.name:
                    continue
                varname = port['varname']
                lava_name = device.get_array_name(self.variables[varname])
                # Not sure about this
                _idx = self.variable_indices[varname]
                read_syn_vars.append(f'{varname} = {lava_name}[{_idx}]')
                syn_output_vars.append(varname)
                syn_output_ports.append(port['portname'])
            kwds['read_syn_vars'] = read_syn_vars
            kwds['syn_output_vars'] = syn_output_vars
            kwds['syn_output_ports'] = syn_output_ports
            kwds['zip'] = zip

        # Receive the input from the synapses
        if self.template_name == 'activation_processing':
            read_port_input = []
            neur_input_vars = []
            ports = device.lava_ports
            for port in ports.values():
                if not port['pathway'] == device._pathway or not port['varname'] in list(self.variables.keys()):
                    continue
                varname = port['varname'] + '_received'
                portname = port['portname']
                # Not sure about this
                read_port_input.append(f'{varname} = self.{portname}_in.recv()')
                neur_input_vars.append(varname)
            kwds['neur_input_vars'] = neur_input_vars
            kwds['read_port_input'] = read_port_input

        # Determine if scipy is available
        try:
            import scipy
            scipy_available = True
        except ImportError:
            scipy_available = False
        kwds['_scipy_available'] = scipy_available

        # Collect template keywords and return
        return kwds


# Functions that exist under the same name in numpy
for func_name, func in [
    ('sin', np.sin), ('cos', np.cos), ('tan', np.tan), ('sinh', np.sinh),
    ('cosh', np.cosh), ('tanh', np.tanh), ('exp', np.exp), ('log', np.log),
    ('log10', np.log10), ('sqrt', np.sqrt), ('arcsin', np.arcsin),
    ('arccos', np.arccos), ('arctan', np.arctan), ('abs', np.abs), ('sign', np.sign)
]:
    DEFAULT_FUNCTIONS[func_name].implementations.add_implementation(LavaCodeGenerator, code=func)


# Functions that are implemented in a somewhat special way
def randn_func(vectorisation_idx):
    try:
        N = len(vectorisation_idx)
        return np.random.randn(N)
    except TypeError:
        # scalar value
        return np.random.randn()


def rand_func(vectorisation_idx):
    try:
        N = len(vectorisation_idx)
        return np.random.rand(N)
    except TypeError:
        # scalar value
        return np.random.rand()


def poisson_func(lam, vectorisation_idx):
    try:
        N = len(vectorisation_idx)
        return np.random.poisson(lam, size=N)
    except TypeError:
        # scalar value
        return np.random.poisson(lam)

# NOTE: At the moment we are not really using these in any way and are instead importing the related functions
# in the process and processmodel scripts. Maybe there is a way to automatically generate imports from these..
DEFAULT_FUNCTIONS['randn'].implementations.add_implementation(LavaCodeGenerator, code=randn_func)
DEFAULT_FUNCTIONS['rand'].implementations.add_implementation(LavaCodeGenerator, code=rand_func)
DEFAULT_FUNCTIONS['poisson'].implementations.add_implementation(LavaCodeGenerator, code=poisson_func)
clip_func = lambda array, a_min, a_max: np.clip(array, a_min, a_max)
DEFAULT_FUNCTIONS['clip'].implementations.add_implementation(LavaCodeGenerator, code=clip_func)
int_func = lambda value: np.int32(value)
DEFAULT_FUNCTIONS['int'].implementations.add_implementation(LavaCodeGenerator, code=int_func)
ceil_func = lambda value: np.int32(np.ceil(value))
DEFAULT_FUNCTIONS['ceil'].implementations.add_implementation(LavaCodeGenerator, code=ceil_func)
floor_func = lambda value: np.int32(np.floor(value))
DEFAULT_FUNCTIONS['floor'].implementations.add_implementation(LavaCodeGenerator, code=floor_func)
DEFAULT_FUNCTIONS['exprel'].implementations.add_implementation(LavaCodeGenerator,code = exprel)

# We need to explicitly add an implementation for the timestep function,
# otherwise Brian would *add* units during simulation, thinking that the
# timestep function would not work correctly otherwise. This would slow the
# function down significantly.
DEFAULT_FUNCTIONS['timestep'].implementations.add_implementation(LavaCodeGenerator, code=timestep)
