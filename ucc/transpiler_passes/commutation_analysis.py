# This file has been modified from the original version in Qiskit.

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2023.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Analysis pass to find commutation relations between DAG nodes."""

from collections import defaultdict

# from qiskit.circuit.commutation_library import SessionCommutationChecker as scc
from qiskit.dagcircuit import DAGOpNode
from qiskit.transpiler.basepasses import AnalysisPass

from .commutation_checker import CommutationChecker

from qiskit.circuit._standard_gates_commutations import (
    standard_gates_commutations,
)


class CommutationAnalysis(AnalysisPass):
    """Analysis pass to find commutation relations between DAG nodes.

    ``property_set['commutation_set']`` is a dictionary that describes
    the commutation relations on a given wire, all the gates on a wire
    are grouped into a set of gates that commute.

    """

    def __init__(self, standard_gates=None, special_commutations=None):
        """
        standard_gates (list[str]): If provided, only the commutation relations between the gates in this list will be considered.
        special_commutations (dict): If provided, the commutation relations in this dictionary will be added to the commutation checker.
        """

        super().__init__()
        if standard_gates is None:
            new_standard_gates_commutations = standard_gates_commutations
        else:
            # Iterate over the standard_gates_commutations dictionary, if both standard_gates are in standard_gates, add to new dictionary
            new_standard_gates_commutations = {}
            for key, value in standard_gates_commutations.items():
                if key[0] in standard_gates and key[1] in standard_gates:
                    new_standard_gates_commutations[key] = value

        if special_commutations is not None:
            # Append the special commutations dictionary elements to the commutation checker dictionary
            for key, value in special_commutations.items():
                new_standard_gates_commutations[key] = value

        self.comm_checker = CommutationChecker(
            new_standard_gates_commutations, check_matrix=False
        )

    def run(self, dag):
        """Run the CommutationAnalysis pass on `dag`.

        Run the pass on the DAG, and write the discovered commutation relations
        into the ``property_set``.
        """
        # Initiate the commutation set
        self.property_set["commutation_set"] = defaultdict(list)

        # Build a dictionary to keep track of the gates on each qubit
        # The key with format (wire) will store the lists of commutation sets
        # The key with format (node, wire) will store the index of the commutation set
        # on the specified wire, thus, for example:
        # self.property_set['commutation_set'][wire][(node, wire)] will give the
        # commutation set that contains node.

        for wire in dag.qubits:
            self.property_set["commutation_set"][wire] = []

        # Add edges to the dictionary for each qubit
        for node in dag.topological_op_nodes():
            for _, _, edge_wire in dag.edges(node):
                self.property_set["commutation_set"][(node, edge_wire)] = -1

        # Construct the commutation set
        for wire in dag.qubits:
            for current_gate in dag.nodes_on_wire(wire):
                current_comm_set = self.property_set["commutation_set"][wire]
                if not current_comm_set:
                    current_comm_set.append([current_gate])

                if current_gate not in current_comm_set[-1]:
                    does_commute = True

                    # Check if the current gate commutes with all the gates in the current block
                    for prev_gate in current_comm_set[-1]:
                        does_commute = (
                            isinstance(current_gate, DAGOpNode)
                            and isinstance(prev_gate, DAGOpNode)
                            and self.comm_checker.commute_nodes(
                                current_gate, prev_gate
                            )
                        )
                        if not does_commute:
                            break

                    if does_commute:
                        current_comm_set[-1].append(current_gate)
                    else:
                        current_comm_set.append([current_gate])

                temp_len = len(current_comm_set)
                self.property_set["commutation_set"][(current_gate, wire)] = (
                    temp_len - 1
                )
