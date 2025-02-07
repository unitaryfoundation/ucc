from benchmarks.scripts.common import (
    cirq_compile,
    qiskit_compile,
    get_native_rep,
    pytket_compile,
)

from cirq import Gateset, CNOT, Rx, Ry, Rz, H


def test_cirq_compiles_to_expected_gateset():
    qasm_str = r"""
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[10];
    ry(pi/2) q[0];
    rx(pi) q[0];
    ry(pi/2) q[1];
    rx(pi) q[1];
    cx q[0],q[1];
    rz(1.5846238651156088) q[1];
    cx q[0],q[1];
    ry(pi/2) q[2];
    rx(pi) q[2];
    cx q[0],q[2];
    rz(1.5846238651156088) q[2];
    cx q[0],q[2];
    rx(1.9993980494552113) q[2];
    """

    # Create a simple Cirq circuit
    cirq_rep = get_native_rep(qasm_str, "cirq")
    # Compile the circuit
    compiled_circuit = cirq_compile(cirq_rep)

    # Check if the compiled circuit uses only the expected gates
    expected_gates = Gateset(CNOT, Rx, Ry, Rz, H)
    assert expected_gates.validate(compiled_circuit), (
        "Cirq compilation had unsupported gatges"
    )


def test_qiskit_compiles_to_expected_gateset():
    qasm_str = r"""
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[10];
    ry(pi/2) q[0];
    rx(pi) q[0];
    ry(pi/2) q[1];
    rx(pi) q[1];
    cx q[0],q[1];
    rz(1.5846238651156088) q[1];
    cx q[0],q[1];
    ry(pi/2) q[2];
    rx(pi) q[2];
    cx q[0],q[2];
    rz(1.5846238651156088) q[2];
    cx q[0],q[2];
    rx(1.9993980494552113) q[2];
    """

    # Create a simple Cirq circuit
    qiskit_rep = get_native_rep(qasm_str, "qiskit")
    # Compile the circuit
    compiled_circuit = qiskit_compile(qiskit_rep)

    # Check if the compiled circuit uses only the expected gates
    expected_gates = {"rz", "rx", "ry", "h", "cx"}
    for op_kind in compiled_circuit.count_ops().keys():
        assert op_kind in expected_gates, (
            f"Qiskit compilation did not produce expected gateset: {op_kind}"
        )


def test_ucc_compiles_to_expected_gateset():
    qasm_str = r"""
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[10];
    ry(pi/2) q[0];
    rx(pi) q[0];
    ry(pi/2) q[1];
    rx(pi) q[1];
    cx q[0],q[1];
    rz(1.5846238651156088) q[1];
    cx q[0],q[1];
    ry(pi/2) q[2];
    rx(pi) q[2];
    cx q[0],q[2];
    rz(1.5846238651156088) q[2];
    cx q[0],q[2];
    rx(1.9993980494552113) q[2];
    """

    # Create a simple Cirq circuit
    native_rep = get_native_rep(qasm_str, "ucc")
    # Compile the circuit
    compiled_circuit = qiskit_compile(native_rep)

    # Check if the compiled circuit uses only the expected gates
    expected_gates = {"rz", "rx", "ry", "h", "cx"}
    for op_kind in compiled_circuit.count_ops().keys():
        assert op_kind in expected_gates, (
            f"Qiskit compilation did not produce expected gateset: {op_kind}"
        )


def test_pytket_compiles_to_expected_gateset():
    qasm_str = r"""
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[10];
    ry(pi/2) q[0];
    rx(pi) q[0];
    ry(pi/2) q[1];
    rx(pi) q[1];
    cx q[0],q[1];
    rz(1.5846238651156088) q[1];
    cx q[0],q[1];
    ry(pi/2) q[2];
    rx(pi) q[2];
    cx q[0],q[2];
    rz(1.5846238651156088) q[2];
    cx q[0],q[2];
    rx(1.9993980494552113) q[2];
    """

    # Create a simple Cirq circuit
    native_rep = get_native_rep(qasm_str, "pytket")
    # Compile the circuit
    compiled_circuit = pytket_compile(native_rep)

    # Check if the compiled circuit uses only the expected gates
    expected_gates = {"Rz", "Rx", "Ry", "H", "CX"}
    for actual_gate in {
        command.op.type.name for command in compiled_circuit.get_commands()
    }:
        assert actual_gate in expected_gates, (
            f"{actual_gate} not in {expected_gates}"
        )
