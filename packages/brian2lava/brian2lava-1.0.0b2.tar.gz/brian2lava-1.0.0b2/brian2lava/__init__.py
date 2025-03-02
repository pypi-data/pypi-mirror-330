# Import device
from .device import LavaDevice
from .preset_mode.model_loader import ModelLoader
#from .preset_mode.lava_parameters import LavaParameters
#from .preset_mode.handler import PresetProcessHandler
#from .utils.f2f import F2F

# Needed to add the lava code object to the codegen targets
from brian2lava.codegen.codeobject import LavaCodeObject

# The Brian2Lava version
__version__ = '1.0.0b2'