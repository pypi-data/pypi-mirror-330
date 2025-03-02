import importlib
from brian2lava_test.utils.const import runtime_config_maps
from brian2 import BrianObject
from brian2.utils.logger import get_logger
from lava.magma.core.process.process import AbstractProcess 


def make_runtime_config_map(obj: BrianObject, process : AbstractProcess, hardware, mode : str, num_repr : str):
    """
    Generates the correct map to feed to RuntimeCfg as the 'exception_proc_model_map'
    argument to avoid incurring in the problem of having inconsistent tags across different
    ProcessModels for the same hardware. At the moment primarily needed for Loihi 2 hardware.
    """
    # In flexible mode there are no exceptions.
    if mode == 'flexible':
        return {}
    logger = get_logger('brian2.devices.lava')

    # Look for process models.
    module_name, proc_model_name = runtime_config_maps[type(obj)].get((hardware, num_repr), (None, None))
    if module_name:
        try:
            module = importlib.import_module(module_name)
            logger.debug(f"Import of '{module_name}' successful.")
            proc_model = getattr(module, proc_model_name)
            logger.debug(f"Found process model '{proc_model_name}'.")
            pm_map = {type(process): proc_model}
            return pm_map
        except Exception as e:
            print(f"Couldn't find '{module_name}', '{proc_model_name}',")
            print(e)
            return {}
        
    return {}


# Decorators ==================================================================
def mode_dependent(func):
    """
    A decorator to select the correct function to use for mode specific methods.
    This is generally avoided unless a function requires a substantially different implementation 
    for different mode.
    """
    def select_mode(*args,**kwargs):
        from brian2 import get_device
        curdev = get_device()
        mode = f'_{curdev.mode}'
        if hasattr(curdev,func.__name__+mode):
            # Remove the 'self' argument
            if args and isinstance(args[0],type(curdev)):
                args = args[1:] if len(args)>1 else ()
           
            return getattr(curdev,func.__name__+mode)(*args,**kwargs)
        else:
            return func(*args,**kwargs)
    
    return select_mode

