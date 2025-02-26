from cirq.devices import TiltedSquareLattice
from qiskit.transpiler import CouplingMap


def coords_to_labels(graph):
    """Convert lattice coordinates to node numbers (labels)."""
    labeled_edges = []
    labels = {str(node): n for n, node in enumerate(graph.nodes())}
    for edge in graph.edges:
        labeled_edges.append((labels[str(edge[0])], labels[str(edge[1])]))
    return labeled_edges


def generate_tilted_square_coupling_list(width, height):
    """Returns coupling list for a tilted square lattice (sycamore layout)
    given the width and height of the device lattice."""
    tilted_square_layout = TiltedSquareLattice(width, height).graph
    return coords_to_labels(tilted_square_layout)


def generate_heavy_hex_coupling_list(distance):
    """Returns coupling list for a heavy-hex lattice given the distance of the
    device lattice."""
    return list(CouplingMap().from_heavy_hex(distance).get_edges())
