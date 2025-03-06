from qbraid.programs.alias_manager import get_program_type_alias
from qbraid.transpiler import ConversionGraph
from qbraid.transpiler import transpile
from .transpilers.ucc_defaults import UCCDefault1


import sys
import warnings

# Specify the supported Python version range
REQUIRED_MAJOR = 3
MINOR_VERSION_MIN = 12
MINOR_VERSION_MAX = 13

current_major = sys.version_info.major
current_minor = sys.version_info.minor

if current_major != REQUIRED_MAJOR or not (
    MINOR_VERSION_MIN <= current_minor <= MINOR_VERSION_MAX
):
    warnings.warn(
        f"Warning: This package is designed for Python {REQUIRED_MAJOR}.{MINOR_VERSION_MIN}-{REQUIRED_MAJOR}.{MINOR_VERSION_MAX}. "
        f"You are using Python) {current_major}.{current_minor}."
    )
supported_circuit_formats = ConversionGraph().nodes()


def compile(
    circuit,
    return_format="original",
    compiler=None,
):
    """Compiles the provided quantum `circuit` by translating it to a Qiskit
    circuit, transpiling it, and returning the optimized circuit in the
    specified `return_format`.

    Args:
        circuit (object): The quantum circuit to be compiled.
        return_format (str): The format in which your circuit will be returned.
            e.g., "TKET", "OpenQASM2". Check ``ucc.supported_circuit_formats()``.
            Defaults to the format of the input circuit.
        compiler (object): The compiler to be used. If None, the default UCCDefault1 is used

    Returns:
        object: The compiled circuit in the specified format.
    """
    if return_format == "original":
        return_format = get_program_type_alias(circuit)

    compiler = UCCDefault1() if compiler is None else compiler

    # Translate to Qiskit Circuit object
    qiskit_circuit = transpile(circuit, "qiskit")
    compiled_circuit = compiler.run(
        qiskit_circuit,
    )

    # Translate the compiled circuit to the desired format
    final_result = transpile(compiled_circuit, return_format)
    return final_result
