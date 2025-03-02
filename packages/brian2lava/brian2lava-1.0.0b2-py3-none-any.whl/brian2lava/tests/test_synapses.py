import pytest
from brian2 import NeuronGroup,Synapses, run, ms
from brian2.utils.logger import catch_logs
from numpy.testing import assert_array_equal, assert_equal, assert_allclose
import numpy as np
from brian2lava.tests.utils import *


def _compare(synapses, expected):
    conn_matrix = np.zeros((len(synapses.source), len(synapses.target)), dtype=np.int32)
    for _i, _j in zip(synapses.i[:], synapses.j[:]):
        conn_matrix[_i, _j] += 1

    assert_equal(conn_matrix, expected)
    # also compare the correct numbers of incoming and outgoing synapses
    incoming = conn_matrix.sum(axis=0)
    outgoing = conn_matrix.sum(axis=1)
    assert all(
        synapses.N_outgoing[:] == outgoing[synapses.i[:]]
    ), "N_outgoing returned an incorrect value"
    assert_array_equal(
        synapses.N_outgoing_pre, outgoing
    ), "N_outgoing_pre returned an incorrect value"
    assert all(
        synapses.N_incoming[:] == incoming[synapses.j[:]]
    ), "N_incoming returned an incorrect value"
    assert_array_equal(
        synapses.N_incoming_post, incoming
    ), "N_incoming_post returned an incorrect value"

    # Compare the "synapse number" if it exists
    if synapses.multisynaptic_index is not None:
        # Build an array of synapse numbers by counting the number of times
        # a source/target combination exists
        synapse_numbers = np.zeros_like(synapses.i[:])
        numbers = {}
        for _i, (source, target) in enumerate(zip(synapses.i[:], synapses.j[:])):
            number = numbers.get((source, target), 0)
            synapse_numbers[_i] = number
            numbers[(source, target)] = number + 1
        assert all(
            synapses.state(synapses.multisynaptic_index)[:] == synapse_numbers
        ), "synapse_number returned an incorrect value"

@use_lava_device
def test_incoming_outgoing(config):
    """
    Test the count of outgoing/incoming synapses per neuron.
    (It will be also automatically tested for all connection patterns that
    use the above _compare function for testing)
    """
    G1 = NeuronGroup(5, "")
    G2 = NeuronGroup(5, "")
    S = Synapses(G1, G2, "")
    S.connect(i=[0, 0, 0, 1, 1, 2], j=[0, 1, 2, 1, 2, 3])
    run(0 * ms)  # to make this work for standalone
    # First source neuron has 3 outgoing synapses, the second 2, the third 1
    assert all(S.N_outgoing[0, :] == 3)
    assert all(S.N_outgoing[1, :] == 2)
    assert all(S.N_outgoing[2, :] == 1)
    assert all(S.N_outgoing[3:, :] == 0)
    assert_array_equal(S.N_outgoing_pre, [3, 2, 1, 0, 0])
    # First target neuron receives 1 input, the second+third each 2, the fourth receives 1
    assert all(S.N_incoming[:, 0] == 1)
    assert all(S.N_incoming[:, 1] == 2)
    assert all(S.N_incoming[:, 2] == 2)
    assert all(S.N_incoming[:, 3] == 1)
    assert all(S.N_incoming[:, 4:] == 0)
    assert_array_equal(S.N_incoming_post, [1, 2, 2, 1, 0])

@use_lava_device
def test_connection_arrays(config):
    """
    Test connecting synapses with explictly given arrays
    """
    G = NeuronGroup(42, "")
    G2 = NeuronGroup(17, "")

    # one-to-one
    expected1 = np.eye(len(G2))
    S1 = Synapses(G2)
    S1.connect(i=np.arange(len(G2)), j=np.arange(len(G2)))

    # full
    expected2 = np.ones((len(G), len(G2)))
    S2 = Synapses(G, G2)
    X, Y = np.meshgrid(np.arange(len(G)), np.arange(len(G2)))
    S2.connect(i=X.flatten(), j=Y.flatten())

    # Multiple synapses
    expected3 = np.zeros((len(G), len(G2)))
    expected3[3, 3] = 2
    S3 = Synapses(G, G2)
    S3.connect(i=[3, 3], j=[3, 3])

    run(0 * ms)  # for standalone
    _compare(S1, expected1)
    _compare(S2, expected2)
    _compare(S3, expected3)

    # Incorrect usage
    S = Synapses(G, G2)
    with pytest.raises(TypeError):
        S.connect(i=[1.1, 2.2], j=[1.1, 2.2])
    with pytest.raises(TypeError):
        S.connect(i=[1, 2], j="string")
    with pytest.raises(TypeError):
        S.connect(i=[1, 2], j=[1, 2], n="i")
    with pytest.raises(TypeError):
        S.connect([1, 2])
    with pytest.raises(ValueError):
        S.connect(i=[1, 2, 3], j=[1, 2])
    with pytest.raises(ValueError):
        S.connect(i=np.ones((3, 3), dtype=np.int32), j=np.ones((3, 1), dtype=np.int32))
    with pytest.raises(IndexError):
        S.connect(i=[41, 42], j=[0, 1])  # source index > max
    with pytest.raises(IndexError):
        S.connect(i=[0, 1], j=[16, 17])  # target index > max
    with pytest.raises(IndexError):
        S.connect(i=[0, -1], j=[0, 1])  # source index < 0
    with pytest.raises(IndexError):
        S.connect(i=[0, 1], j=[0, -1])  # target index < 0
    with pytest.raises(ValueError):
        S.connect("i==j", j=np.arange(10))
    with pytest.raises(TypeError):
        S.connect("i==j", n=object())
    with pytest.raises(TypeError):
        S.connect("i==j", p=object())
    with pytest.raises(TypeError):
        S.connect(object())

@use_lava_device
def test_connection_string_deterministic_full(config):
    G = NeuronGroup(17, "")
    G2 = NeuronGroup(4, "")

    # Full connection
    expected_full = np.ones((len(G), len(G2)))

    S1 = Synapses(G, G2, "")
    S1.connect(True)

    S2 = Synapses(G, G2, "")
    S2.connect("True")

    run(0 * ms)  # for standalone

    _compare(S1, expected_full)
    _compare(S2, expected_full)

@use_lava_device
def test_connection_string_deterministic_full_no_self(config):

    G = NeuronGroup(17, "v : 1")
    G.v = "i"
    G2 = NeuronGroup(4, "v : 1")
    G2.v = "17 + i"

    # Full connection without self-connections
    expected_no_self = np.ones((len(G), len(G))) - np.eye(len(G))

    S1 = Synapses(G, G)
    S1.connect("i != j")
    with pytest.raises(NotImplementedError):
        S2 = Synapses(G, G)
        S2.connect("v_pre != v_post")

    S3 = Synapses(G, G)
    S3.connect(condition="i != j")

    run(0 * ms)  # for standalone

    _compare(S1, expected_no_self)
    #_compare(S2, expected_no_self)
    _compare(S3, expected_no_self)

@use_lava_device
def test_connection_string_deterministic_full_custom(config):
    G = NeuronGroup(17, "")
    G2 = NeuronGroup(4, "")
    # Everything except for the upper [2, 2] quadrant
    number = 2
    expected_custom = np.ones((len(G), len(G)))
    expected_custom[:number, :number] = 0
    S1 = Synapses(G, G)
    S1.connect("(i >= number) or (j >= number)")

    S2 = Synapses(G, G)
    S2.connect(
        "(i >= explicit_number) or (j >= explicit_number)",
        namespace={"explicit_number": number},
    )

    # check that this mistaken syntax raises an error
    with pytest.raises(ValueError):
        S2.connect("k for k in range(1)")

    # check that trying to connect to a neuron outside the range raises an error

    run(0 * ms)  # for standalone

    _compare(S1, expected_custom)
    _compare(S2, expected_custom)

@use_lava_device
def test_connection_random_with_condition(config):
    G = NeuronGroup(4, "")

    S1 = Synapses(G, G)
    S1.connect("i!=j", p=0.0)

    S2 = Synapses(G, G)
    S2.connect("i!=j", p=1.0)
    expected2 = np.ones((len(G), len(G))) - np.eye(len(G))

    S3 = Synapses(G, G)
    S3.connect("i>=2", p=0.0)

    S4 = Synapses(G, G)
    S4.connect("i>=2", p=1.0)
    expected4 = np.zeros((len(G), len(G)))
    expected4[2, :] = 1
    expected4[3, :] = 1

    S5 = Synapses(G, G)
    S5.connect("j<2", p=0.0)
    S6 = Synapses(G, G)
    S6.connect("j<2", p=1.0)
    expected6 = np.zeros((len(G), len(G)))
    expected6[:, 0] = 1
    expected6[:, 1] = 1

    with catch_logs() as _:  # Ignore warnings about empty synapses
        run(0 * ms)  # for standalone

    assert len(S1) == 0
    _compare(S2, expected2)
    assert len(S3) == 0
    _compare(S4, expected4)
    assert len(S5) == 0
    _compare(S6, expected6)

@use_lava_device
def test_connection_random_with_condition_2(config):
    G = NeuronGroup(4, "")

    # Just checking that everything works in principle (we can't check the
    # actual connections)
    S7 = Synapses(G, G)
    S7.connect("i!=j", p=0.01)

    S8 = Synapses(G, G)
    S8.connect("i!=j", p=0.03)

    S9 = Synapses(G, G)
    S9.connect("i!=j", p=0.3)

    S10 = Synapses(G, G)
    S10.connect("i>=2", p=0.01)

    S11 = Synapses(G, G)
    S11.connect("i>=2", p=0.03)

    S12 = Synapses(G, G)
    S12.connect("i>=2", p=0.3)

    S13 = Synapses(G, G)
    S13.connect("j>=2", p=0.01)

    S14 = Synapses(G, G)
    S14.connect("j>=2", p=0.03)

    S15 = Synapses(G, G)
    S15.connect("j>=2", p=0.3)

    S16 = Synapses(G, G)
    S16.connect("i!=j", p="i*0.1")

    S17 = Synapses(G, G)
    S17.connect("i!=j", p="j*0.1")

    # Forces the use of the "jump algorithm"
    big_group = NeuronGroup(10000, "")
    S18 = Synapses(big_group, big_group)
    S18.connect("i != j", p=0.001)

    # See github issue #835 -- this failed when using numpy
    S19 = Synapses(big_group, big_group)
    S19.connect("i < int(N_post*0.5)", p=0.001)

    with catch_logs() as _:  # Ignore warnings about empty synapses
        run(0 * ms)  # for standalone

    assert not any(S7.i == S7.j)
    assert not any(S8.i == S8.j)
    assert not any(S9.i == S9.j)
    assert all(S10.i >= 2)
    assert all(S11.i >= 2)
    assert all(S12.i >= 2)
    assert all(S13.j >= 2)
    assert all(S14.j >= 2)
    assert all(S15.j >= 2)
    assert not any(S16.i == 0)
    assert not any(S17.j == 0)

@use_lava_device
def test_connection_random_with_indices(config):
    """
    Test random connections.
    """
    G = NeuronGroup(4, "")
    G2 = NeuronGroup(7, "")

    S1 = Synapses(G, G2)
    S1.connect(i=0, j=0, p=0.0)
    expected1 = np.zeros((len(G), len(G2)))

    S2 = Synapses(G, G2)
    S2.connect(i=0, j=0, p=1.0)
    expected2 = np.zeros((len(G), len(G2)))
    expected2[0, 0] = 1

    S3 = Synapses(G, G2)
    S3.connect(i=[0, 1], j=[0, 2], p=1.0)
    expected3 = np.zeros((len(G), len(G2)))
    expected3[0, 0] = 1
    expected3[1, 2] = 1

    # Just checking that it works in principle
    S4 = Synapses(G, G)
    S4.connect(i=0, j=0, p=0.01)
    S5 = Synapses(G, G)
    S5.connect(i=[0, 1], j=[0, 2], p=0.01)

    S6 = Synapses(G, G)
    S6.connect(i=0, j=0, p=0.03)

    S7 = Synapses(G, G)
    S7.connect(i=[0, 1], j=[0, 2], p=0.03)

    S8 = Synapses(G, G)
    S8.connect(i=0, j=0, p=0.3)

    S9 = Synapses(G, G)
    S9.connect(i=[0, 1], j=[0, 2], p=0.3)

    with catch_logs() as _:  # Ignore warnings about empty synapses
        run(0 * ms)  # for standalone

    _compare(S1, expected1)
    _compare(S2, expected2)
    _compare(S3, expected3)
    assert 0 <= len(S4) <= 1
    assert 0 <= len(S5) <= 2
    assert 0 <= len(S6) <= 1
    assert 0 <= len(S7) <= 2
    assert 0 <= len(S8) <= 1
    assert 0 <= len(S9) <= 2

@use_lava_device
def test_connection_random_without_condition(config):
    G = NeuronGroup(
        4,
        """
        v: 1
        x : integer
        """,
    )
    G.x = "i"
    G2 = NeuronGroup(
        7,
        """
        v: 1
        y : 1
        """,
    )
    G2.y = "1.0*i/N"

    S1 = Synapses(G, G2)
    S1.connect(True, p=0.0)

    S2 = Synapses(G, G2)
    S2.connect(True, p=1.0)

    # Just make sure using values between 0 and 1 work in principle
    S3 = Synapses(G, G2)
    S3.connect(True, p=0.3)

    # TODO: These are currently not supported! Reinstate them when we fix this issue.
    # Use pre-/post-synaptic variables for "stochastic" connections that are
    # actually deterministic
    # S4 = Synapses(G, G2)
    # S4.connect(True, p="int(x_pre==2)*1.0")

    # # Use pre-/post-synaptic variables for "stochastic" connections that are
    # # actually deterministic
    # S5 = Synapses(G, G2)
    # S5.connect(True, p="int(x_pre==2 and y_post > 0.5)*1.0")

    with catch_logs() as _:  # Ignore warnings about empty synapses
        run(0 * ms)  # for standalone

    _compare(S1, np.zeros((len(G), len(G2))))
    _compare(S2, np.ones((len(G), len(G2))))
    assert 0 <= len(S3) <= len(G) * len(G2)
    # assert len(S4) == 7
    # assert_equal(S4.i, np.ones(7) * 2)
    # assert_equal(S4.j, np.arange(7))
    # assert len(S5) == 3
    # assert_equal(S5.i, np.ones(3) * 2)
    # assert_equal(S5.j, np.arange(3) + 4)

@use_lava_device
def test_connection_multiple_synapses(config):
    """
    Test multiple synapses per connection.
    """
    G = NeuronGroup(42, "v: 1")
    G.v = "i"
    G2 = NeuronGroup(17, "v: 1")
    G2.v = "i"

    S1 = Synapses(G, G2)
    S1.connect(True, n=0)

    S2 = Synapses(G, G2)
    S2.connect(True, n=2)

    S3 = Synapses(G, G2)
    S3.connect(True, n="j")

    S4 = Synapses(G, G2)
    S4.connect(True, n="i")

    S5 = Synapses(G, G2)
    S5.connect(True, n="int(i>j)*2")

    # TODO: This is not supported yet
    # S6 = Synapses(G, G2)
    # S6.connect(True, n="int(v_pre>v_post)*2")

    with catch_logs() as _:  # Ignore warnings about empty synapses
        run(0 * ms)  # for standalone

    assert len(S1) == 0
    _compare(S2, 2 * np.ones((len(G), len(G2))))
    _compare(S3, np.arange(len(G2)).reshape(1, len(G2)).repeat(len(G), axis=0))

    _compare(S4, np.arange(len(G)).reshape(len(G), 1).repeat(len(G2), axis=1))
    expected = np.zeros((len(G), len(G2)), dtype=np.int32)
    for source in range(len(G)):
        expected[source, :source] = 2
    _compare(S5, expected)
    #_compare(S6, expected)

@use_lava_device
def test_constant_variable_subexpression_in_synapses(config):
    G = NeuronGroup(10, "")
    S = Synapses(
        G,
        G,
        """
        dv1/dt = -v1**2 / (10*ms) : 1 (clock-driven)
        dv2/dt = -v_const**2 / (10*ms) : 1 (clock-driven)
        dv3/dt = -v_var**2 / (10*ms) : 1 (clock-driven)
        dv4/dt = -v_noflag**2 / (10*ms) : 1 (clock-driven)
        v_const = v2 : 1 (constant over dt)
        v_var = v3 : 1
        v_noflag = v4 : 1
        """,
        method="rk2",
    )
    S.connect(j="i")
    S.v1 = "1.0*i/N"
    S.v2 = "1.0*i/N"
    S.v3 = "1.0*i/N"
    S.v4 = "1.0*i/N"

    run(10 * ms)
    # "variable over dt" subexpressions are directly inserted into the equation
    assert_allclose(S.v3[:], S.v1[:])
    assert_allclose(S.v4[:], S.v1[:])
    # "constant over dt" subexpressions will keep a fixed value over the time
    # step and therefore give a slightly different result for multi-step
    # methods
    assert np.sum((S.v2 - S.v1) ** 2) > 1e-10

# @use_lava_device
# def test_nested_subexpression_references(config):
#     """
#     Assure that subexpressions in targeted groups are handled correctly.
#     """
#     G = NeuronGroup(
#         10,
#         """
#         v : 1
#         v2 = 2*v : 1
#         v3 = 1.5*v2 : 1
#         """,
#         threshold="v>=5",
#     )
#     G2 = NeuronGroup(10, "v : 1")
#     G.v = np.arange(10)
#     S = Synapses(G, G2, on_pre="v_post += v3_pre")
#     S.connect(j="i")
#     run(defaultclock.dt)
#     assert_allclose(G2.v[:5], 0.0)
#     assert_allclose(G2.v[5:], (5 + np.arange(5)) * 3)

# if __name__ == '__main__':
#     from brian2.utils.logger import BrianLogger
#     from brian2.core.preferences import prefs
#     prefs.logging.file_log = True
#     prefs.logging.file_log_level = "DIAGNOSTIC"
#     prefs.codegen.target = 'numpy'
#     test_nested_subexpression_references()

if __name__ == '__main__':
    test_constant_variable_subexpression_in_synapses({})


    