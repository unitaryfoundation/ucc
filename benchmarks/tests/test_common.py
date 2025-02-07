import cirq
from benchmarks.scripts.common import BenchmarkTargetGateset
from benchmarks.scripts import random_clifford_circuit
from qbraid.transpiler import transpile


def test_benchmark_target_gateset_simple_circuit():
    """
    Tests that a simple circuit compiles to the desired target
    gateset and has equivalent functionality
    """
    q = cirq.LineQubit.range(2)
    c_orig = cirq.Circuit(
        cirq.T(q[0]),
        cirq.SWAP(*q),
        cirq.T(q[0]),
        cirq.SWAP(*q),
        cirq.SWAP(*q),
        cirq.T.on_each(*q),
    )

    c_new = cirq.optimize_for_target_gateset(
        c_orig, gateset=BenchmarkTargetGateset()
    )

    cirq.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        c_orig, c_new, atol=1e-6
    )

    expected_gates = cirq.Gateset(cirq.CNOT, cirq.Rx, cirq.Ry, cirq.Rz, cirq.H)
    assert expected_gates.validate(c_new), (
        "Cirq compilation had unsupported gatges"
    )


def test_benchmark_target_gateset_random_clifford():
    """
    Tests that a random clifford circuit compiles to the desired target
    gateset and has equivalent functionality
    """
    c_orig = transpile(random_clifford_circuit(6, 727), target="cirq")

    c_new = cirq.optimize_for_target_gateset(
        c_orig, gateset=BenchmarkTargetGateset()
    )

    # Check that circuits are equivalent
    cirq.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        c_orig, c_new, atol=1e-6
    )
    # Check if the compiled circuit uses only the expected gates
    expected_gates = cirq.Gateset(cirq.CNOT, cirq.Rx, cirq.Ry, cirq.Rz, cirq.H)
    assert expected_gates.validate(c_new), (
        "Cirq compilation had unsupported gatges"
    )
