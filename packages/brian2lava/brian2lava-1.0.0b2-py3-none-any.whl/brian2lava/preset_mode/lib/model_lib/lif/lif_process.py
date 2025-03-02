import numpy as np
import typing as ty

from lava.magma.core.learning.learning_rule import Loihi2FLearningRule
from lava.magma.core.process.process import LogConfig, AbstractProcess
from lava.magma.core.process.variable import Var
from lava.magma.core.process.ports.ports import InPort, OutPort
from lava.magma.core.process.neuron import LearningNeuronProcess
from brian2.utils.logger import get_logger

class AbstractLIF(AbstractProcess):
    """Abstract class for variables common to all neurons with leaky
    integrator dynamics."""

    def __init__(
        self,
        *,
        shape: ty.Tuple[int, ...],
        j: ty.Union[float, list, np.ndarray],
        v: ty.Union[float, list, np.ndarray],
        delta_j: float,
        delta_v: float,
        bias_mant: ty.Union[float, list, np.ndarray],
        bias_exp: ty.Union[float, list, np.ndarray],
        name: str,
        log_config: LogConfig,
        **kwargs,
    ) -> None:
        super().__init__(
            shape=shape,
            j=j,
            v=v,
            delta_j=delta_j,
            delta_v=delta_v,
            bias_mant=bias_mant,
            bias_exp=bias_exp,
            name=name,
            log_config=log_config,
            **kwargs,
        )
        self.logger = get_logger('brian2.devices.lava')

        self.a_in = InPort(shape=shape)
        self.s_out = OutPort(shape=shape)
        self.j = Var(shape=shape, init=j)
        self.v = Var(shape=shape, init=v)
        #self.bias = Var(shape=shape, init=np.int16(bias_mant * 2**bias_exp))
        self.delta_j = Var(shape=(1,), init=delta_j)
        self.delta_v = Var(shape=(1,), init=delta_v)
        self.bias_exp = Var(shape=shape, init=bias_exp)
        self.bias_mant = Var(shape=shape, init=bias_mant)


class LIF(AbstractLIF):
    """Leaky-Integrate-and-Fire (LIF) neural Process.

    LIF dynamics abstracts to:
    j[t] = j[t-1] * (1-delta_j) + a_in         # neuron current
    v[t] = v[t-1] * (1-delta_v) + j[t] + bias  # neuron voltage
    s_out = v[t] > v_th                         # spike if threshold is exceeded
    v[t] = 0                                   # reset at spike

    Parameters
    ----------
    shape : tuple(int)
        Number and topology of LIF neurons.
    j : float, list, numpy.ndarray, optional
        Initial value of the neurons' current.
    v : float, list, numpy.ndarray, optional
        Initial value of the neurons' voltage (membrane potential).
    delta_j : float, optional
        Inverse of decay time constant `tau_j` for current decay. Currently, 
        only a single decay can be set for the entire population of neurons.
    delta_v : float, optional
        Inverse of decay time constant `tau_v` for voltage decay. Currently, 
        only a single decay can be set for the entire population of neurons.
    bias_mant : float, list, numpy.ndarray, optional
        Mantissa part of neuron bias.
    bias_exp : float, list, numpy.ndarray, optional
        Exponent part of neuron bias, if needed. Mostly for fixed point
        implementations. Ignored for floating point implementations.
    v_th : float, optional
        Neuron threshold voltage, exceeding which, the neuron will spike.
        Currently, only a single threshold can be set for the entire
        population of neurons.
    v_rs : float, optional
        Neuron reset voltage after spike.
    dt : float, optional
        Duration of one timestep. Is only used for floating-point computation
        (assuming integer value `>= 1` for fixed-point computation).

    Example
    -------
    >>> lif = LIF(shape=(200, 15), delta_j=10, delta_v=5)
    This will create 200x15 LIF neurons that all have the same current decay
    of 10 and voltage decay of 5.
    """

    def __init__(
        self,
        *,
        shape: ty.Tuple[int, ...],
        j: ty.Optional[ty.Union[float, list, np.ndarray]] = 0,
        v: ty.Optional[ty.Union[float, list, np.ndarray]] = 0,
        delta_j: ty.Optional[float] = 0,
        delta_v: ty.Optional[float] = 0,
        bias_mant: ty.Optional[ty.Union[float, list, np.ndarray]] = 0,
        bias_exp: ty.Optional[ty.Union[float, list, np.ndarray]] = 0,
        v_th: ty.Optional[float] = 100,
        v_rs: ty.Optional[float] = 0,
        dt: ty.Optional[float] = 0,
        name: ty.Optional[str] = None,
        log_config: ty.Optional[LogConfig] = None,
        **kwargs) -> None:
        super().__init__(
            shape=shape,
            j=j,
            v=v,
            delta_j=delta_j,
            delta_v=delta_v,
            bias_mant=bias_mant,
            bias_exp=bias_exp,
            name=name,
            log_config=log_config,
            **kwargs)
        # Set threshold and reset voltage
        self.v_th = Var(shape=(1,), init=v_th)
        self.v_rs = Var(shape=(1,), init=v_rs)
        self.dt = Var(shape=(1,), init=dt)
        msg_var_par = f"Initialized attributes in process '{self.name}'"
            
        # Print the values
        msg_var_par = f"""{msg_var_par}:
             shape = {shape}
             j = {j}
             v = {v}
             delta_j = {self.delta_j.init} (computed from tau_j)
             delta_v = {self.delta_v.init} (computed from tau_v)
             bias_mant = {self.bias_mant.init}, bias_exp = {self.bias_exp.init}
             v_th = {self.v_th.init}
             v_rs = {self.v_rs.init}
             dt = {self.dt.init}"""
        self.logger.debug(msg_var_par)
        
