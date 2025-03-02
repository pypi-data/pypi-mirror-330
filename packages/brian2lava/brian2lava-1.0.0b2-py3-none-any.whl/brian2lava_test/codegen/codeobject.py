import numpy as np

# from brian2.core.base import BrianObjectException
# from brian2.core.preferences import prefs, BrianPreference
from brian2.core.variables import DynamicArrayVariable, ArrayVariable, AuxiliaryVariable, Subexpression
from brian2.core.functions import Function

from brian2.codegen.codeobject import CodeObject, constant_or_scalar, check_compiler_kwds
from brian2.codegen.targets import codegen_targets

from brian2lava_test.codegen.lava_generator import LavaCodeGenerator
from brian2lava_test.codegen.templater import Templater


class LavaCodeObject(CodeObject):
    """
    Class of code objects that generate Lava compatible code
    """


    templater = Templater('brian2lava_test.codegen','.py_', env_globals={'constant_or_scalar': constant_or_scalar})
    generator_class = LavaCodeGenerator
    class_name = 'lava'


    def __init__(
            self, owner, code, variables, variable_indices,
            template_name, template_source, compiler_kwds,
            name='lava_code_object*'
        ):
        check_compiler_kwds(compiler_kwds, [], 'lava')

        from brian2.devices.device import get_device
        self.device = get_device()
        self.namespace = {
            '_owner': owner,
            'logical_not': np.logical_not  # TODO: This should maybe go somewhere else
        }
        CodeObject.__init__(
            self, owner, code, variables, variable_indices,
            template_name, template_source,
            compiler_kwds=compiler_kwds, name=name
        )


    @classmethod
    def is_available(cls):
        """
        Checks if the given backend is available

        Parameters
        ----------
        cls
            A CodeObject derived class

        Returns
        -------
        `bool`
            Indicates if the given backend is avialable or not
        """

        # TODO
        # For all hardwares perhaps check if Lava is installed?
        # For Loihi, we need to check if Loihi is actually available
        # For now, just return true
        return True


    def compile_block(self, block):
        """
        Compiles a block of code.

        Parameters
        ----------
        block
            A block of code

        Returns
        -------
        `str`
            Compiled code
        """

        code = getattr(self.code, block, '').strip()
        if not code or 'EMPTY_CODE_BLOCK' in code:
            return None
        return code


    def run(self):
        # Running is handled by Lava
        pass


    def run_block(self, block):
        # Running is handled by Lava
        pass


codegen_targets.add(LavaCodeObject)
