import itertools
import math
import random

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes.utils import CheckMap

from ucc import compile
from ucc.tests.mock_backends import Mybackend
from ucc.transpilers.phase_polynomial import (
    PhasePolynomialSynthesis,
    phase_polynomial_of,
    synthesize_phase_polynomial,
)
from ucc.transpilers.ucc_defaults import UCCDefault1


def run_pass(circuit):
    return PassManager([PhasePolynomialSynthesis()]).run(circuit)


def assert_exact(result, circuit):
    """Equal as matrices, global phase included."""
    assert np.allclose(
        Operator(result).data, Operator(circuit).data, atol=1e-8
    )


def diagonal_step(num_qubits=3):
    step = QuantumCircuit(num_qubits, name="step")
    for qubit in range(num_qubits):
        step.rz(0.3 * (qubit + 1), qubit)
    step.cx(0, 1)
    step.rz(0.7, 1)
    step.cx(0, 1)
    step.cx(1, 2)
    step.p(1.1, 2)
    step.cx(1, 2)
    return step


def test_extracts_terms_and_global_phase():
    circuit = QuantumCircuit(2)
    circuit.rzz(0.4, 0, 1)
    circuit.p(0.3, 0)

    terms, global_phase, linear_map = phase_polynomial_of(circuit)

    assert terms == pytest.approx({0b11: 0.4, 0b01: 0.3})
    assert global_phase == pytest.approx(-0.2)
    assert linear_map is None


def test_rejects_non_phase_gates():
    circuit = QuantumCircuit(1)
    circuit.h(0)

    with pytest.raises(ValueError):
        phase_polynomial_of(circuit)


def test_synthesis_handles_angles_above_pi():
    # Qiskit's synth_cnot_phase_aam reduces angles modulo pi, which is wrong
    # for p(theta); angles in [pi, 2pi) must still come out exact.
    circuit = QuantumCircuit(3)
    for (first, second), angle in zip(
        itertools.combinations(range(3), 2), (4.0, -1.3, 2 * math.pi - 0.1)
    ):
        circuit.rzz(angle, first, second)
    terms, global_phase, linear_map = phase_polynomial_of(circuit)

    result = synthesize_phase_polynomial(3, terms, global_phase, linear_map)

    assert_exact(result, circuit)


@pytest.mark.parametrize("num_qubits", [3, 5, 6])
def test_commuting_rzz_layer_uses_fewer_cx(num_qubits):
    rng = random.Random(num_qubits)
    circuit = QuantumCircuit(num_qubits)
    for first, second in itertools.combinations(range(num_qubits), 2):
        circuit.rzz(rng.uniform(-4, 4), first, second)
    circuit.h(0)

    result = run_pass(circuit)

    assert_exact(result, circuit)
    if num_qubits >= 5:
        direct_cx = 2 * num_qubits * (num_qubits - 1) // 2
        assert result.count_ops().get("cx", 0) < direct_cx


@pytest.mark.parametrize(
    "power, num_ctrl_qubits, ctrl_state",
    [(32, 1, 1), (8, 1, 0), (4, 2, 3), (4, 2, 2)],
)
def test_controlled_power_of_phase_polynomial(
    power, num_ctrl_qubits, ctrl_state
):
    gate = (
        diagonal_step()
        .power(power)
        .to_gate()
        .control(num_ctrl_qubits, ctrl_state=ctrl_state)
    )
    circuit = QuantumCircuit(gate.num_qubits)
    circuit.append(gate, circuit.qubits)

    result = run_pass(circuit)

    assert_exact(result, circuit)
    assert result.count_ops().get("cx", 0) <= 40


def test_controlled_gate_inside_custom_composite_is_reached():
    controlled = diagonal_step().power(16).to_gate().control(1)
    wrapper = QuantumCircuit(4, name="wrapper")
    wrapper.h(0)
    wrapper.append(controlled, range(4))
    circuit = QuantumCircuit(4)
    circuit.append(wrapper.to_gate(), range(4))

    result = run_pass(circuit)

    assert_exact(result, circuit)
    assert "wrapper" not in result.count_ops()


@pytest.mark.parametrize("seed", range(15))
def test_random_cnot_phase_blocks_are_exact(seed):
    # Includes blocks whose CNOTs do not cancel (non-identity linear part).
    rng = random.Random(seed)
    num_qubits = 4
    circuit = QuantumCircuit(num_qubits)
    for _ in range(16):
        gate = rng.choice(["cx", "rz", "cp", "cz", "t", "rzz", "swap", "s"])
        first, second = rng.sample(range(num_qubits), 2)
        if gate == "cx":
            circuit.cx(first, second)
        elif gate == "swap":
            circuit.swap(first, second)
        elif gate == "rz":
            circuit.rz(rng.uniform(-4, 4), first)
        elif gate == "cp":
            circuit.cp(rng.uniform(-4, 4), first, second)
        elif gate == "rzz":
            circuit.rzz(rng.uniform(-4, 4), first, second)
        elif gate == "cz":
            circuit.cz(first, second)
        else:
            getattr(circuit, gate)(first)
    circuit.h(rng.randrange(num_qubits))

    result = run_pass(circuit)

    assert_exact(result, circuit)


def test_single_qubit_phase_runs_are_left_alone():
    circuit = QuantumCircuit(1)
    circuit.rz(0.1, 0)
    circuit.p(0.2, 0)

    result = run_pass(circuit)

    assert result == circuit


def test_block_is_kept_when_resynthesis_is_not_cheaper():
    circuit = QuantumCircuit(2)
    circuit.cx(0, 1)
    circuit.rz(0.3, 1)
    circuit.cx(0, 1)

    result = run_pass(circuit)

    assert result == circuit


def test_block_is_kept_when_two_qubit_consolidation_does_as_well():
    """Regression: a block was replaced whenever the parity network beat its
    raw CNOT count, even when later two-qubit consolidation does as well.
    Parity networks spread CNOTs over more qubits, which made a 100-qubit
    QFT go from 2,740 to 3,695 CNOTs after consolidation."""
    circuit = QuantumCircuit(2)
    for angle in (0.3, 0.5, 0.7):
        circuit.cp(angle, 0, 1)
        circuit.rz(0.1, 1)

    result = run_pass(circuit)

    assert result == circuit


def controlled_power_circuit(num_qubits=3, power=32):
    gate = diagonal_step(num_qubits).power(power).to_gate().control(1)
    circuit = QuantumCircuit(gate.num_qubits)
    circuit.h(0)
    circuit.append(gate, circuit.qubits)
    return circuit


def test_compile_option_is_off_by_default():
    circuit = controlled_power_circuit()

    assert compile(circuit) == compile(
        circuit, phase_polynomial_synthesis=False
    )


def test_compile_option_lowers_cx_count_exactly():
    circuit = controlled_power_circuit()

    default = compile(circuit)
    result = compile(circuit, phase_polynomial_synthesis=True)

    assert Operator(result).equiv(Operator(circuit))
    assert set(result.count_ops()) <= UCCDefault1.DEFAULT_GATESET
    assert result.count_ops()["cx"] < default.count_ops()["cx"]


def test_compile_option_respects_target_backend():
    circuit = controlled_power_circuit()
    backend = Mybackend()

    result = compile(
        circuit, target_backend=backend, phase_polynomial_synthesis=True
    )

    assert set(result.count_ops()) <= set(backend.operation_names)
    check_map = CheckMap(
        backend.target.build_coupling_map(), property_set_field="check_map"
    )
    pass_manager = PassManager([check_map])
    pass_manager.run(result)
    assert pass_manager.property_set["check_map"]
