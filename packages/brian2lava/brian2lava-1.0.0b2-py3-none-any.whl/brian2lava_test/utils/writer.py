import os

# Import Brian2 modules
from brian2.utils.logger import get_logger
from brian2 import get_device


class PyWriter(object):
    '''
    Writes given contents to Python files.
    Inspired from CPPWriter from the cpp_standalone device.
    '''

    def __init__(self, project_directory):
        '''
        Initializes the project directory
        '''

        # Store project directory
        self.project_directory = project_directory

        # Make logger available to all methods in this class
        self.logger = get_logger('brian2.devices.lava')

    def write(self, filename: str, contents: str):
        '''
        Writes a given content to a file with given filename
        '''

        # Log contents and filename
        self.logger.diagnostic(f'Writing file {filename}:\n{contents}')

        # Assemble path
        path = os.path.join(self.project_directory, filename)

        # If path already exist and content of the file matches the given content, return
        if os.path.exists(path):
            with open(path, 'r') as f:
                if f.read() == contents:
                    return

        # Write contents to file
        with open(path, 'w') as f:
            f.write(contents)
