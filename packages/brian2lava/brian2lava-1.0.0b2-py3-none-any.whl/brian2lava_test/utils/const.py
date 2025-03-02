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
objects_f2f = (
    NeuronGroup,
    Synapses,
    SynapticPathway
)


available_lava_modules = {
   #BrianObject           :    Lava module
    SynapticPathway       :    'lava.proc.dense.process',
    Synapses              :    'lava.proc.dense.process',
    SpikeGeneratorGroup   :    'lava.proc.io.source',
}


# We only define the exceptions to the tags in case there are any
runtime_config_maps = {
    Synapses                :   {
        (HARDWARE.Loihi2, 'fixed')     : ('lava.proc.dense.ncmodels','NcModelDense'),
    },

    SpikeGeneratorGroup     :   {
        (HARDWARE.Loihi2, 'fixed')     : ('lava.proc.io.source', 'PySendModelFixed')
    },
    
    NeuronGroup             :   {}

}

LOIHI2_MAX_BIT_RANGE = 2**16
class LOIHI2_MANTISSA_MAX_VALUE:
    weights = 2**8 -1
    other = 2**16 -1
