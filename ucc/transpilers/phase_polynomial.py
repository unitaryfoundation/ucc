"""Phase-polynomial resynthesis of CNOT + phase structure.

A circuit built only from CNOTs and diagonal phase gates is a phase
polynomial followed by a reversible linear map:
``|x> -> exp(i f(x)) |L x>`` with ``f(x) = phi + sum_y theta_y * (y . x)``
over a set of parities ``y`` (all arithmetic mod 2 inside the parities).
Basis translation hides this structure: Qiskit expands a controlled power
``C-U^(2^k)`` of such a circuit into ``2^k`` controlled copies, and emits
each two-qubit ``ZZ`` rotation as its own ``CX RZ CX`` sandwich.

Working on the polynomial instead is exact and much cheaper:

* repeating a phase polynomial ``2^k`` times only scales its angles;
* controlling it maps each term ``theta * y`` to
  ``theta * c * y = theta/2 * (c + y - c^y)``;
* a whole layer of commuting phase gates is one polynomial, which a parity
  network (GraySynth, Amy-Azimzadeh-Mosca) realizes with far fewer CNOTs
  than one ``CX RZ CX`` per term; a remaining linear map ``L`` is added
  with Patel-Markov-Hayes CNOT synthesis.

:class:`PhasePolynomialSynthesis` applies these rewrites before basis
translation and keeps a rewrite only when it lowers the CNOT count.
"""

import math
from functools import lru_cache
from itertools import combinations

from qiskit import transpile as qiskit_transpile
from qiskit.circuit import ControlledGate, Gate, QuantumCircuit
from qiskit.converters import circuit_to_dag
from qiskit.dagcircuit import DAGOpNode
from qiskit.exceptions import QiskitError
from qiskit.dagcircuit.collect_blocks import BlockCollector
from qiskit.synthesis import synth_cnot_count_full_pmh, synth_cnot_phase_aam
from qiskit.transpiler import PassManager
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.transpiler.passes import (
    Collect2qBlocks,
    ConsolidateBlocks,
    UnitarySynthesis,
)

_TWO_PI = 2 * math.pi
_ANGLE_TOLERANCE = 1e-10
_PLACEHOLDER_STEP = 1e-6

# Fixed phases, in units of exp(i * angle * x), for parameterless gates.
_FIXED_PHASES = {
    "z": math.pi,
    "s": math.pi / 2,
    "sdg": -math.pi / 2,
    "t": math.pi / 4,
    "tdg": -math.pi / 4,
}
_PHASE_GATES = {
    "rz",
    "p",
    "u1",
    "rzz",
    "cz",
    "cp",
    "cu1",
    "crz",
    *_FIXED_PHASES,
}
_LINEAR_GATES = {"cx", "swap"}
_IGNORED = {"id", "barrier"}

# Translation CNOT cost of each collectable gate, used to decide whether a
# resynthesized block is an improvement.
_DIRECT_CX_COST = {
    "cx": 1,
    "swap": 3,
    "rzz": 2,
    "cz": 1,
    "cp": 2,
    "cu1": 2,
    "crz": 2,
}

# Upper bounds that keep the symbolic simulation and synthesis cheap.
_MAX_POLYNOMIAL_QUBITS = 64
_MAX_SIMULATED_INSTRUCTIONS = 200_000
_MAX_CONTROLLED_TERMS = 4096


class _NotPhasePolynomial(Exception):
    """Raised when a circuit fragment is not a pure CNOT + phase circuit."""


class _PhasePolynomialBuilder:
    """Symbolically simulate CNOT + phase gates on parity bitmasks."""

    def __init__(self, num_qubits):
        self.parities = [1 << qubit for qubit in range(num_qubits)]
        self.terms = {}
        self.global_phase = 0.0
        self.simulated = 0

    def add_term(self, parity, angle):
        if parity == 0:
            return
        self.terms[parity] = self.terms.get(parity, 0.0) + angle

    def apply(self, operation, qubits):
        self.simulated += 1
        if self.simulated > _MAX_SIMULATED_INSTRUCTIONS:
            raise _NotPhasePolynomial("fragment too large")

        name = operation.name
        if name in _IGNORED:
            return
        params = [_numeric(param) for param in operation.params]
        parities = self.parities

        if name == "cx":
            parities[qubits[1]] ^= parities[qubits[0]]
        elif name == "swap":
            first, second = qubits
            parities[first], parities[second] = (
                parities[second],
                parities[first],
            )
        elif name == "rz":
            self.add_term(parities[qubits[0]], params[0])
            self.global_phase -= params[0] / 2
        elif name in ("p", "u1"):
            self.add_term(parities[qubits[0]], params[0])
        elif name in _FIXED_PHASES:
            self.add_term(parities[qubits[0]], _FIXED_PHASES[name])
        elif name == "rzz":
            first, second = qubits
            self.add_term(parities[first] ^ parities[second], params[0])
            self.global_phase -= params[0] / 2
        elif name in ("cz", "cp", "cu1"):
            angle = math.pi if name == "cz" else params[0]
            self._add_product(qubits[0], qubits[1], angle)
        elif name == "crz":
            control, target = qubits
            # Control on: rz(theta) on the target, i.e. -theta/2 * c
            # + theta * c * t.
            self.add_term(parities[control], -params[0] / 2)
            self._add_product(control, target, params[0])
        elif operation.definition is not None and not isinstance(
            operation, ControlledGate
        ):
            definition = operation.definition
            self.global_phase += _numeric(definition.global_phase)
            positions = {
                bit: qubits[index]
                for index, bit in enumerate(definition.qubits)
            }
            for instruction in definition.data:
                if instruction.clbits:
                    raise _NotPhasePolynomial("classical bits")
                self.apply(
                    instruction.operation,
                    [positions[bit] for bit in instruction.qubits],
                )
        else:
            raise _NotPhasePolynomial(name)

    def _add_product(self, first, second, angle):
        """Add ``angle * a * b`` = ``angle/2 * (a + b - a^b)``."""
        first_parity = self.parities[first]
        second_parity = self.parities[second]
        self.add_term(first_parity, angle / 2)
        self.add_term(second_parity, angle / 2)
        self.add_term(first_parity ^ second_parity, -angle / 2)

    def finish(self):
        """Return ``(terms, global_phase, linear_map)``.

        ``linear_map`` lists, per output qubit, the parity of input qubits it
        holds; it is None when the CNOTs cancel overall.
        """
        linear_map = list(self.parities)
        if all(
            parity == 1 << qubit for qubit, parity in enumerate(linear_map)
        ):
            linear_map = None
        terms = {}
        for parity, angle in self.terms.items():
            angle = _reduce_angle(angle)
            if angle is not None:
                terms[parity] = angle
        return terms, self.global_phase, linear_map


def _numeric(value):
    try:
        return float(value)
    except TypeError as error:
        raise _NotPhasePolynomial("symbolic parameter") from error


def _reduce_angle(angle):
    """Reduce to [0, 2pi); None if the phase is trivial."""
    angle %= _TWO_PI
    if angle < _ANGLE_TOLERANCE or _TWO_PI - angle < _ANGLE_TOLERANCE:
        return None
    return angle


def phase_polynomial_of(circuit):
    """Return ``(terms, global_phase, linear_map)`` of a CNOT + phase circuit.

    ``terms`` maps a parity bitmask over ``circuit.qubits`` to an angle and
    ``linear_map[q]`` is the input parity left on qubit ``q`` (None if the
    identity), so the circuit is
    ``|x> -> exp(i (global_phase + sum theta (y.x))) |L x>``.
    Raises ``ValueError`` for anything else.
    """
    builder = _PhasePolynomialBuilder(circuit.num_qubits)
    builder.global_phase += _numeric(circuit.global_phase)
    try:
        for instruction in circuit.data:
            if instruction.clbits:
                raise _NotPhasePolynomial("classical bits")
            builder.apply(
                instruction.operation,
                [circuit.find_bit(bit).index for bit in instruction.qubits],
            )
        return builder.finish()
    except _NotPhasePolynomial as error:
        raise ValueError(str(error)) from error


def synthesize_phase_polynomial(
    num_qubits, terms, global_phase=0.0, linear_map=None
):
    """Synthesize a phase polynomial with a GraySynth parity network.

    ``synth_cnot_phase_aam`` reduces numeric angles modulo pi rather than
    2 pi, so an angle in [pi, 2pi) is given as an exact ``z`` column plus a
    remainder below pi. The CNOT network depends only on the columns, not on
    the angles, so it is cached per column layout and the real angles are
    filled in afterwards (QAOA layers on one graph share one synthesis). A
    non-identity ``linear_map`` is appended with Patel-Markov-Hayes.
    """
    columns = []
    angles = []
    for parity, angle in sorted(terms.items()):
        angle %= _TWO_PI
        if angle >= math.pi:
            columns.append((parity, "z"))
            angle -= math.pi
        if angle >= _ANGLE_TOLERANCE:
            columns.append((parity, "p"))
            angles.append(angle)

    circuit = QuantumCircuit(num_qubits)
    if columns:
        network = _parity_network(num_qubits, tuple(columns))
        for instruction in network.data:
            qubits = [
                network.find_bit(bit).index for bit in instruction.qubits
            ]
            operation = instruction.operation
            if operation.name == "p":
                # Placeholder k marks the k-th "p" column.
                index = round(float(operation.params[0]) / _PLACEHOLDER_STEP)
                circuit.p(angles[index - 1], qubits[0])
            else:
                circuit.append(operation, qubits)
    if linear_map is not None:
        circuit.compose(
            _linear_network(num_qubits, tuple(linear_map)), inplace=True
        )
    circuit.global_phase += global_phase
    return circuit


@lru_cache(maxsize=1024)
def _parity_network(num_qubits, columns):
    """GraySynth network for ``(parity, "z" | "p")`` columns.

    The k-th ``p`` column gets the placeholder angle
    ``k * _PLACEHOLDER_STEP`` (well below pi, so it survives the modulo-pi
    reduction unchanged), which lets callers substitute the real angle.
    """
    cnots = [
        [(parity >> qubit) & 1 for parity, _ in columns]
        for qubit in range(num_qubits)
    ]
    angles = []
    placeholder = 0
    for _, kind in columns:
        if kind == "z":
            angles.append("z")
        else:
            placeholder += 1
            angles.append(placeholder * _PLACEHOLDER_STEP)
    return synth_cnot_phase_aam(cnots, angles)


_CONSOLIDATION_CACHE = {}
_MAX_CONSOLIDATION_CACHE = 4096


def _consolidated_cx_count(circuit, block_key):
    """CNOTs left after two-qubit block consolidation and resynthesis.

    Cached per block polynomial (bounded); only the accept/reject decision
    depends on it, never the emitted circuit.
    """
    cached = _CONSOLIDATION_CACHE.get(block_key)
    if cached is not None:
        return cached
    consolidated = PassManager(
        [
            Collect2qBlocks(),
            ConsolidateBlocks(force_consolidate=True),
            UnitarySynthesis(basis_gates=["cx", "u"]),
        ]
    ).run(circuit)
    count = _cx_count(consolidated)
    if len(_CONSOLIDATION_CACHE) >= _MAX_CONSOLIDATION_CACHE:
        _CONSOLIDATION_CACHE.clear()
    _CONSOLIDATION_CACHE[block_key] = count
    return count


@lru_cache(maxsize=4096)
def _cached_block_synthesis(num_qubits, terms_key, linear_key):
    """Synthesize a block exactly repeated elsewhere (rounded-angle key)."""
    return synthesize_phase_polynomial(
        num_qubits,
        dict(terms_key),
        linear_map=None if linear_key is None else list(linear_key),
    )


@lru_cache(maxsize=1024)
def _linear_network(num_qubits, linear_map):
    """Patel-Markov-Hayes CNOT circuit for ``|x> -> |L x>``."""
    matrix = [
        [bool((parity >> column) & 1) for column in range(num_qubits)]
        for parity in linear_map
    ]
    return synth_cnot_count_full_pmh(matrix)


def _controlled_terms(terms, global_phase, num_ctrl_qubits):
    """Terms of the polynomial controlled on all-ones control qubits.

    Controls occupy bits ``0 .. k-1`` and the base qubits are shifted up by
    ``k``. A product of ``m`` bits expands into parities as
    ``prod v_i = 2^(1-m) * sum_{S != {}} (-1)^(|S|+1) XOR_{i in S} v_i``.
    """
    controls = [1 << index for index in range(num_ctrl_qubits)]
    controlled = {}

    def add_product(variables, angle):
        scale = angle / 2 ** (len(variables) - 1)
        for size in range(1, len(variables) + 1):
            sign = 1 if size % 2 else -1
            for subset in combinations(variables, size):
                parity = 0
                for variable in subset:
                    parity ^= variable
                controlled[parity] = controlled.get(parity, 0.0) + sign * scale

    for parity, angle in terms.items():
        add_product(controls + [parity << num_ctrl_qubits], angle)
    if _reduce_angle(global_phase) is not None:
        add_product(controls, global_phase)

    reduced = {}
    for parity, angle in controlled.items():
        angle = _reduce_angle(angle)
        if angle is not None:
            reduced[parity] = angle
    return reduced


def _cx_count(circuit):
    return circuit.count_ops().get("cx", 0)


def _synthesize_controlled_gate(gate):
    """Return a cheaper circuit for a controlled phase polynomial, or None."""
    if gate.num_qubits > _MAX_POLYNOMIAL_QUBITS or gate.num_ctrl_qubits > 4:
        return None
    base = QuantumCircuit(gate.base_gate.num_qubits)
    base.append(gate.base_gate, base.qubits)
    try:
        terms, global_phase, linear_map = phase_polynomial_of(base)
    except ValueError:
        return None
    if linear_map is not None:
        return None

    num_ctrl_qubits = gate.num_ctrl_qubits
    controlled = _controlled_terms(terms, global_phase, num_ctrl_qubits)
    if len(controlled) > _MAX_CONTROLLED_TERMS:
        return None
    try:
        synthesized = synthesize_phase_polynomial(gate.num_qubits, controlled)
    except (QiskitError, ValueError):
        return None

    # Open controls (ctrl_state bit 0) are handled by X conjugation.
    open_controls = [
        index
        for index in range(num_ctrl_qubits)
        if not (gate.ctrl_state >> index) & 1
    ]
    if open_controls:
        wrapped = QuantumCircuit(gate.num_qubits)
        wrapped.x(open_controls)
        wrapped.compose(synthesized, inplace=True)
        wrapped.x(open_controls)
        synthesized = wrapped

    reference = QuantumCircuit(gate.num_qubits)
    reference.append(gate, reference.qubits)
    reference = qiskit_transpile(
        reference, basis_gates=["cx", "u"], optimization_level=0
    )
    if _cx_count(synthesized) >= _cx_count(reference):
        return None
    return synthesized


_COLLECTABLE = _PHASE_GATES | _LINEAR_GATES


def _is_collectable(node):
    # Reads ``name`` and ``is_parameterized`` rather than ``node.op``, which
    # builds a new Python gate object on every access.
    return (
        isinstance(node, DAGOpNode)
        and not node.cargs
        and node.name in _COLLECTABLE
        and not node.is_parameterized()
    )


def _inline_custom_composites(dag, max_rounds=8):
    """Inline user-defined composite gates (plain ``Gate`` with a definition).

    Library gates and controlled gates are left intact; inlining exposes the
    controlled phase polynomials inside wrappers such as Qiskit's ``QPE``.
    """
    for _ in range(max_rounds):
        inlined = False
        for node in list(dag.op_nodes()):
            if node.is_standard_gate() or node.is_controlled_gate():
                continue
            operation = node.op
            if type(operation) is Gate and operation.definition is not None:
                dag.substitute_node_with_dag(
                    node, circuit_to_dag(operation.definition)
                )
                inlined = True
        if not inlined:
            return


class PhasePolynomialSynthesis(TransformationPass):
    """Resynthesize CNOT + phase structure as phase polynomials.

    Two rewrites, each kept only if it lowers the CNOT count:

    1. A controlled gate whose base gate is a phase polynomial (for example
       ``C-U^(2^k)`` in phase estimation with a diagonal ``U``) becomes the
       controlled polynomial, synthesized once with a parity network.
    2. A maximal block of CNOT and phase gates (for example a QAOA cost
       layer of commuting ``rzz`` gates, or the ``cx``/``rz`` runs left by
       basis translation) is resynthesized with a parity network plus, if
       its CNOTs do not cancel, a linear CNOT circuit.

    Both rewrites are exact, including global phase. Run it before basis
    translation for the controlled-gate rewrite; block resynthesis also
    pays off after translation. Synthesized circuits are inlined.

    Args:
        max_block_qubits: Blocks on more qubits are left alone. Parity
            network synthesis is the expensive step; wide blocks rarely beat
            two-qubit consolidation.
    """

    def __init__(self, max_block_qubits=_MAX_POLYNOMIAL_QUBITS):
        super().__init__()
        self.max_block_qubits = max_block_qubits

    def run(self, dag):
        _inline_custom_composites(dag)
        for node in list(dag.op_nodes()):
            if (
                not node.is_controlled_gate()
                or node.cargs
                or node.name in _COLLECTABLE
            ):
                continue
            operation = node.op
            if not isinstance(operation, ControlledGate):
                continue
            synthesized = _synthesize_controlled_gate(operation)
            if synthesized is not None:
                dag.substitute_node_with_dag(node, circuit_to_dag(synthesized))

        blocks = BlockCollector(dag).collect_all_matching_blocks(
            _is_collectable, split_blocks=True, min_block_size=2
        )
        for block in blocks:
            self._resynthesize_block(dag, block, self.max_block_qubits)
        return dag

    @staticmethod
    def _resynthesize_block(
        dag, block, max_block_qubits=_MAX_POLYNOMIAL_QUBITS
    ):
        block_qubits = sorted(
            {qubit for node in block for qubit in node.qargs},
            key=lambda qubit: dag.find_bit(qubit).index,
        )
        # Single-qubit phase runs are left to the 1q optimizer.
        if not 2 <= len(block_qubits) <= max_block_qubits:
            return
        direct_cost = sum(_DIRECT_CX_COST.get(node.name, 0) for node in block)
        # A non-trivial two-qubit phase already needs two CNOTs.
        if direct_cost <= 2:
            return
        positions = {qubit: index for index, qubit in enumerate(block_qubits)}
        circuit = QuantumCircuit(len(block_qubits))
        for node in block:
            circuit.append(node.op, [positions[q] for q in node.qargs])
        try:
            terms, global_phase, linear_map = phase_polynomial_of(circuit)
        except ValueError:
            return
        block_key = (
            len(block_qubits),
            tuple(
                sorted(
                    (parity, round(angle, 12))
                    for parity, angle in terms.items()
                )
            ),
            None if linear_map is None else tuple(linear_map),
        )
        try:
            synthesized = _cached_block_synthesis(*block_key)
        except (QiskitError, ValueError):
            return
        if _cx_count(synthesized) >= direct_cost:
            return
        # Later local passes consolidate two-qubit runs (a cp is cx-rz-cx,
        # and several on one pair collapse to at most three CNOTs). A parity
        # network spreads CNOTs over more qubits and defeats that, so it has
        # to beat what consolidation would reach, not just the raw count.
        if _cx_count(synthesized) >= _consolidated_cx_count(
            circuit, block_key
        ):
            return
        replacement = circuit_to_dag(synthesized)
        replacement.global_phase += global_phase
        # BlockCollector blocks are convex, so the cycle check (a full DAG
        # traversal per block) is unnecessary, as in Qiskit's BlockCollapser.
        placeholder = dag.replace_block_with_op(
            block, synthesized.to_gate(), positions, cycle_check=False
        )
        dag.substitute_node_with_dag(placeholder, replacement)
