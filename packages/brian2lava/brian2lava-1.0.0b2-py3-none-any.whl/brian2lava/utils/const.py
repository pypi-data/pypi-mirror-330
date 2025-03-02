from lava.magma.core.run_configs import Loihi2SimCfg, Loihi2HwCfg
from brian2 import SpikeGeneratorGroup, NeuronGroup
from brian2.synapses.synapses import SynapticPathway, Synapses
from enum import Enum

# Define very small number that is numerically considered zero 
EPSILON = 1e-10	

# Define the eligible hardware via an abstract class (strings should be used case insensitive)
class HARDWARE(Enum):
    CPU = 1
    Loihi2 = 2

    def get_names():
        return set(x.name for x in HARDWARE) 
    
    def get_values():
        return set(x.value for x in HARDWARE) 

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"'{self.name}'"
    

# Define the runtime config and tag for all possible combinations of model mode, hardware, and number
# representation (note: flexible mode only supports floating-point, Loihi2 only supports fixed-point representation)
runtime_configs = {
   #(Mode,         Hardware,          Number repr.)    :    (Configuration,   Tag)
    ('flexible',   HARDWARE.CPU,      'float')         :    (Loihi2SimCfg,    None),
    ('preset',     HARDWARE.CPU,      'float')         :    (Loihi2SimCfg,    None),
    ('preset',     HARDWARE.CPU,      'fixed')         :    (Loihi2SimCfg,    'fixed_pt'),
    ('preset',     HARDWARE.Loihi2,   'fixed')         :    (Loihi2HwCfg,     'ucoded')
}


# Spcify the objects that shall be subject to F2F conversion
objects_using_f2f = (
    NeuronGroup,
    Synapses,
    SynapticPathway
)


# Map Brian objects to Lava processes that are readily available in the Lava library
available_processes_lava = {
    #BrianObject           :    lava_process_module
    SynapticPathway       :    'lava.proc.dense.process',
    Synapses              :    'lava.proc.dense.process',
    SpikeGeneratorGroup   :    'lava.proc.io.source'
}


# Map Brian objects to customized Lava processes that are readily available within the Brian2Lava package
available_processes_b2l = {
    #BrianObject           :    lava_process_module
    SynapticPathway       :    'brian2lava.preset_mode.lib.lava_proc.dense.process',
    Synapses              :    'brian2lava.preset_mode.lib.lava_proc.dense.process',
    SpikeGeneratorGroup   :    'lava.proc.io.source'
}


# Map Brian objects to customized Lava processes from a user-defined directory. This is/has to be used for the 
# special case of Lava-Loihi
available_processes_lava_loihi_custom = {
    #BrianObject           :    lava_process_module
    SynapticPathway       :    'lava_workspace.dense.adapted_ncmodels',
    Synapses              :    'lava_workspace.dense.adapted_ncmodels'
}


# We only define the exceptions to the tags in case there are any
runtime_config_maps = {
    #BrianObject           :    { (hardware, num_repr, custom_proc_dir) : (lava_process_module, implementation_name) , ... }
    Synapses                :   {
        (HARDWARE.Loihi2, 'fixed', False)    : ('lava.proc.dense.ncmodels', 'NcModelDense'),
        (HARDWARE.Loihi2, 'fixed', True)     : ('lava_workspace.dense.adapted_ncmodels', 'NcModelDense'),
    },

    SpikeGeneratorGroup     :   {
        (HARDWARE.Loihi2, 'fixed', False)    : ('lava.proc.io.source', 'PySendModelFixed'),
        (HARDWARE.Loihi2, 'fixed', True)     : ('lava.proc.io.source', 'PySendModelFixed')
    },
    
    NeuronGroup             :   {}

}

class LOIHI2_SPECS:
    Max_Variables = 2**23 - 1
    Max_Weights = 2**15
    Max_Constants = 2**16
    Max_Random = 2**24
    Max_Deltas = 2**12 
    Max_Mantissa_Weights = 2**8 -1
    Max_Mantissa_Others = 2**12 -1 # 13-bit signed
    Max_Exponent_Weights = 7
    Nax_Exponent_Others = 7
    MSB_Alignment_Act = 6
    MSB_Alignment_Decay = 12
    MSB_Alignment_Prob = 24
