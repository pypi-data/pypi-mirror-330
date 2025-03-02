import os
import tempfile

# Import Brian2 modules
from brian2.utils.filetools import ensure_directory

# Import Brian2Lava modules
from brian2lava.utils.writer import PyWriter


def prepare_directory(self):
    """
    Make sure the set project directory exists and prepare it.
    """
        
    # Create project directories (if not exists)
    ensure_directory(self.project_dir)
    #for d in ['code_objects', 'results', 'static_arrays']:
    #    ensure_directory(os.path.join(directory, d))

    # Log directory path
    self.logger.debug(
        "Writing Lava project to directory " + os.path.normpath(self.project_dir)
    )


def write_templates(self, process_rendered: str, process_model_rendered: str, name: str):
    """
    Write the rendered templates to files.
    
    Parameters
    ----------
    process_rendered : `str`
        The rendered Lava process template as string.
    process_model_rendered : `str`
        The rendered Lava process model template as string.
    name : `str`
        Name of the network object (e.g. 'neurongroup_0').
    """
    full_file_contents = process_rendered + '\n' + process_model_rendered
    # Write 'process' to working directory
    self.writer.write(f'{name}.py', full_file_contents)
    
