from brian2.core.preferences import prefs

from brian2lava.utils.const import runtime_configs, HARDWARE
from brian2lava.preset_mode.model_loader import ModelLoader
from brian2lava.preset_mode.handler import PresetProcessHandler


class SettingsParser:

    def __init__(self, device):
        self.device = device
        self.settings = {}
    
    def parse_hardware(self, selected_hardware):
        hardware = None
        for available_hw_name in HARDWARE.get_names():
            if selected_hardware == available_hw_name.lower():
                hardware = getattr(HARDWARE, available_hw_name)
                break
        if not hardware:
            # Default: CPU
            hardware = HARDWARE.CPU
        self.settings["hardware"] = hardware

    def parse_mode(self, mode, hardware):
        if not mode:
            # Default for CPU backend: flexible mode
            if hardware == HARDWARE.CPU:
                mode = 'flexible'
            # Default for Loihi2 backend: preset mode (Loihi2 only supports this)
            elif hardware == HARDWARE.Loihi2:
                mode = 'preset'
        self.settings['mode'] = mode

    def parse_num_repr(self, num_repr, mode):
        # Default for flexible mode: floating-point representation
        if mode == 'flexible':
            num_repr = 'float'
        # Default for preset mode: fixed point representation (Loihi2 only supports this)
        elif mode == 'preset':
            num_repr = 'fixed' if not num_repr else num_repr
        self.settings['num_repr'] = num_repr

    def parse_f2f(self, use_f2f, binary_accuracy, decimal_accuracy):

        if not use_f2f:
            self.settings['f2f'] = None
            return
        
        # Default choice
        if use_f2f == 'model_wise' or use_f2f == True:
            from brian2lava.utils.f2f import ModelWiseF2F as F2F
        elif use_f2f == 'generic':
            from brian2lava.utils.f2f import F2F

        # Places to account for when converting to fixed point (first use binary accuracy if provided, 
        # then use decimal accuracy if provided)
        if binary_accuracy:
            F2F.set_binary_accuracy(int(binary_accuracy))
        elif decimal_accuracy:
            F2F.set_decimal_accuracy(int(decimal_accuracy))
        else:
            F2F.set_binary_accuracy(0)

        f2f = F2F()
        self.settings['f2f'] = f2f

    def select_runtime_config(self, mode, hardware, num_repr):
        # Set the runtime configuration for this hardware
        # Raises an exception if the user has selected an unsupported mode or unsupported hardware
        try:
            runtime_config, runtime_tag = runtime_configs[(mode, hardware, num_repr)]
        except KeyError:
            raise NotImplementedError(f"The selected combination of model mode/hardware/number representation " +
                                    f"'({mode}, {hardware}, {num_repr})' is not implemented (yet). " +
                                    f"The available combinations are: {list(runtime_configs.keys())}. Choices are "+
                                    f"case-insensitive but correct spelling is required.")
        
        self.settings['runtime_config'] = runtime_config
        self.settings['runtime_tag'] = runtime_tag

    def select_codegen_targets(self, mode):
        # Set codegen targets.
        # For flexible mode, Brian2Lava performs code generation on its own.
        if mode == 'flexible':
            prefs.codegen.target = 'lava'
            #prefs.codegen.target = 'numpy'
            prefs.codegen.string_expression_target = 'lava'

        # For preset mode, we use the Brian's numpy (runtime) configuration. This is necessary
        # for Brian to execute code and define variables before runtime. These variables can
        # then be fed to the Lava process as kwargs. See the documentation on preset mode for
        # more information.
        elif mode == 'preset':
            prefs.codegen.target = 'numpy'
            prefs.codegen.string_expression_target = 'numpy'
        
        self.device.logger.debug(f"Code generation target set to '{prefs.codegen.target}'.")

    def load_models_from_library(self, models_dir, print_models):
        self.settings['models_dir'] = models_dir
        # Read models from package and from user-defined path; tell if a list of the models should be printed
        ModelLoader.read_models(self.device, models_dir, print_models)
        
    def parse_lava_proc_dir(self, lava_proc_dir):
        if self.settings["hardware"] == HARDWARE.Loihi2:
            self.settings['lava_proc_dir'] = lava_proc_dir
        else:
            self.settings['lava_proc_dir'] = None
        
    def parse_project_dir_path(self, project_path):
        if project_path is None:
            project_path = ''
        self.device.set_project_directory(project_path)

    def parse_variable_updating(self, variable_updating_disabled):
        self.settings['variable_updating_disabled'] = variable_updating_disabled

    def parse_exp_array(self, use_exp_array):
        self.settings['use_exp_array'] = use_exp_array

    def check_deprecated_args(self, kwargs):
        if kwargs.get('models_path'):
                raise ValueError("The argument 'models_path' has been deprecated, please use 'models_dir' instead")
    
    def parse_settings(self, kwargs):

        self.check_deprecated_args(kwargs)

        self.parse_hardware(kwargs.get('hardware','').lower())

        self.parse_mode(kwargs.get('mode', '').lower(), self.settings['hardware'])

        self.parse_num_repr(kwargs.get('num_repr', '').lower(), self.settings['mode'])

        self.parse_f2f(kwargs.get('use_f2f', False),
                       kwargs.get('binary_accuracy', None),
                       kwargs.get('decimal_accuracy', None))
        
        self.select_runtime_config(self.settings['mode'], self.settings['hardware'], self.settings['num_repr'])

        self.select_codegen_targets(self.settings['mode'])

        # Set directory of Lava models to be used
        self.load_models_from_library(kwargs.get('models_dir', None),
                                      kwargs.get('print_models', False))

        # Set directory of other pre-defined Lava processes to be used (only for Loihi 2)
        self.parse_lava_proc_dir(kwargs.get('lava_proc_dir', None))

        # Create the workspace directory (first look at project_path setting, otherwise the current working directory will be used)
        self.parse_project_dir_path(kwargs.get('project_path', ''))

        self.parse_variable_updating(kwargs.get('variable_updating_disabled', False))

        self.parse_exp_array(kwargs.get('use_exp_array', False))

    def apply_settings(self):
        """
        Apply the chosen settings to the device by setting its attributes according to 
        the preferences selected by the user.
        """
        for attr_name, value in self.settings.items():
            setattr(self.device, attr_name, value)
            self.device.logger.diagnostic(f"Set {attr_name} to {value}.")
    