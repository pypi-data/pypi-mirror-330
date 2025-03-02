import os
import glob
from brian2 import NeuronGroup
from brian2lava.utils.const import available_processes_lava, available_processes_b2l, \
                                   available_processes_lava_loihi_custom, HARDWARE

def scrap_folder(path, name : str = '', startswith : str = '', endswith : str = '', max_files: int = None, return_full_path: bool = False, empty_ok: bool = False):
    """
    Find files in a directory based on certain criteria.

    Parameters
    ----------
        path : str
            The directory path where to search for files.
        name : str, optional
            The exact filename to match (default `''`).
        startswith : str, optional
            The prefix of the filename (default `''`).
        endswith : str, optional
            The suffix of the filename (default `''`).
        max_files : int, optional
            The maximum number of files allowed (default `None`).
        return_full_path : bool, optional
            Specifies if full path shall be returned (default `False`).
        empty_ok : bool, optional
            Prevents an error to be raised if no file was found (default `False`).

    Returns
    -------
        list: A list of matching file paths.
    """

    # Validate input parameters
    if not os.path.exists(path):
        raise ValueError(f"Invalid directory path: {path}")

    # Use glob to perform file matching
    files_found = glob.glob(os.path.join(path, name)) if name else glob.glob(os.path.join(path, f"{startswith}*{endswith}"))

    # Only keep the basename if the user doesn't want the full path
    if not return_full_path:
        tmp = []
        for file in files_found:
            tmp.append(os.path.basename(file))
        files_found = tmp

    if max_files is not None and len(files_found) > max_files:
        obj_of_search = name if len(name) else startswith + '*' + endswith
        raise Exception(f"A maximum of {max_files} files were expected from this search, {len(files_found)} were found.\n \
                        Object of the search: {obj_of_search}")
    if not files_found and not empty_ok:
        raise FileNotFoundError(f"A file matching the criteria {startswith}*{endswith} was not found.")
    
    return files_found

def get_module_name(brian_object, device, base_name = '', force_scrap = False):
    """
    Utility function to get the name of the module containing the class implementation for the
    Lava Process corresponding to a certain Brian object. If the module relates to a (pre-)defined or dynamically
    generated neuron group process, the function searches through the project directory, while if it's one of the
    modules already made available by Lava, it's collected from the dictionaries of available Lava modules stored
    in `brian2lava.utils.const`.

    Parameters
    ----------
        brian_object : any
            The Brian object to consider.
        device : any
            The device object (holding the project directory to be searched as well as other important information).
        base_name : str, optional
            The suffix of the file name of files to be found (default `''`).
        force_scrap : bool, optional
            Can be set to `True` to enforce searching the project directory (default `False`).

    Returns
    -------
        str
            The name of the Lava module, e.g., 'lava.proc.dense.process'.
    """
    if isinstance(brian_object, NeuronGroup) or force_scrap:
        # Look for the correct file in the project directory
        file_name = scrap_folder(device.project_dir, endswith=base_name+'.py', max_files=1, return_full_path=False)[0]

        #print(f"file_name = '{file_name}' (project_dir = '{device.project_dir}', sys.path = '{sys.path}')")
        # Get the process from the module where it's defined
        return os.path.basename(device.project_dir) + '.' + os.path.splitext(file_name)[0]
		
    else:
        brian_object_type = type(brian_object)
        # Check if we want to use arrays of (individual) exponent values in mantissa-and-exponent representation, in which
        # case we need customized synapse processes.
        if device.use_exp_array:
            # For Loihi 2, use user-provided customized processes (which are automatically copied to the project directory)
            if device.hardware == HARDWARE.Loihi2 and brian_object_type in available_processes_lava_loihi_custom.keys():
                return available_processes_lava_loihi_custom[brian_object_type]
            
            # Otherwise, use customized processes included the Brian2Lava package
            elif brian_object_type in available_processes_b2l.keys():
                return available_processes_b2l[brian_object_type]
            
        # Otherwise, we just use the processes provided by Lava
        elif brian_object_type in available_processes_lava.keys():
            return available_processes_lava[brian_object_type]
        
        raise ValueError(f"No Lava module available for Brian object type '{brian_object_type}'.")
