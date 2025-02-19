## `ucc`: Unitary Compiler Collection

[![Repository](https://img.shields.io/badge/GitHub-5C5C5C.svg?logo=github)](https://github.com/unitaryfund/ucc)
[![Unitary Foundation](https://img.shields.io/badge/Supported%20By-Unitary%20Foundation-FFFF00.svg)](https://unitary.foundation)
[![Documentation Status](https://readthedocs.org/projects/ucc/badge/?version=latest)](https://ucc.readthedocs.io/en/latest/?badge=latest)
[![Discord Chat](https://img.shields.io/badge/dynamic/json?color=blue&label=Discord&query=approximate_presence_count&suffix=%20online.&url=https%3A%2F%2Fdiscord.com%2Fapi%2Finvites%2FJqVGmpkP96%3Fwith_counts%3Dtrue)](http://discord.unitary.foundation)


The **Unitary Compiler Collection (UCC)** is a Python library for frontend-agnostic, high performance compilation of quantum circuits. UCC's goal is to gather together the best of open source compilation to make quantum programming simpler, faster, and more scalable.

By leveraging [qBraid](https://github.com/qBraid/qBraid), UCC interfaces automatically with multiple quantum computing frameworks, including [Qiskit](https://github.com/Qiskit/qiskit), [Cirq](https://github.com/quantumlib/Cirq), and [PyTKET](https://github.com/CQCL/tket) and supports programs in OpenQASM 2 and [OpenQASM 3](https://openqasm.com/). For a full list of the latest supported interfaces, just call `ucc.supported_circuit_formats`.


**Want to know more?**
- Check out our [documentation](https://ucc.readthedocs.io/en/latest/), which you can build locally after installation by running `make html` in `ucc/docs/source`.
- Read the [launch announcement](https://unitary.foundation/posts/2025_ucc_launch_blog) to learn more on the current state of UCC, its capabilities and future direction.
- For code, repo, or theory questions, especially those requiring more detailed responses, submit a [Discussion](https://github.com/unitaryfund/ucc/discussions).
- For casual or time sensitive questions, chat with us on [Discord](http://discord.unitary.foundation).

## Quickstart

### Installation

**Note**: UCC requires Python version ≥ 3.12.

```bash
pip install ucc
```

If developing or running benchmark, please install [Poetry](https://python-poetry.org/), then setup a dev version:

```bash
git clone https://github.com/unitaryfund/ucc.git
cd ucc
poetry install
```

### Example with Qiskit, Cirq, and PyTKET

Define a circuit with your preferred quantum SDK and compile it!

```python
from ucc import compile

from pytket import Circuit as TketCircuit
from cirq import Circuit as CirqCircuit
from qiskit import QuantumCircuit as QiskitCircuit
from cirq import H, CNOT, LineQubit

def test_tket_compile():
    circuit = TketCircuit(2)
    circuit.H(0)
    circuit.CX(0, 1)
    compile(circuit)

def test_qiskit_compile():
    circuit = QiskitCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    compile(circuit)

def test_cirq_compile():
    qubits = LineQubit.range(2)
    circuit = CirqCircuit(
        H(qubits[0]),
        CNOT(qubits[0], qubits[1]))
    compile(circuit)
```
<!-- start-how-does-ucc-stack-up -->
<!-- comment used to strip this section from being added to the docs build-->
## How does UCC stack up?

UCC seeks to provide an end-to-end compiler that works well for the majority of the users out of the box. Today, this is achieved by building on and customizing [Qiskit](https://github.com/Qiskit/qiskit) transpiler passes. To ensure these customizations improve performance and meet user needs, we regularly run benchmarks comparing UCC against the latest versions of leading quantum compiler frameworks across a range of circuits. Here’s the latest:
![alt text](benchmarks/latest_compiler_benchmarks_by_circuit.png)

In addition to raw compilation stats, we simulate the compiled circuits with a noisy density matrix simulation to see how each compiler impacts performance.
Here we plot the absolute errors $|\langle O\rangle_{C_i,\text{ideal}} - \langle O\rangle_{C_i,\text{noisy}}|$ for a collection of circuits $C_i$.

![Violin plot showing absolute error of each compiler across a variety of circuits](benchmarks/latest_expval_benchmark_by_compiler.png)

And here you can see progress over time, with new package versions labeled for each compiler:
![alt text](benchmarks/avg_compiler_benchmarks_over_time.png)
Note that the compile times before 2024-12-10 may have been run on different classical compute instances, so their runtime is not reported here, but you can find this data in benchmarks/results.
After 2024-12-10, all data present in this plot is on the same compute instance using our [ucc-benchmarks](https://github.com/unitaryfund/ucc/blob/main/.github/workflows/ucc-benchmarks.yml) GitHub Actions workflow.

To learn more about running these benchmarks, the overall benchmark philosophy, or how to contribute to improving the benchmarking methodology, check out the [benchmarking section](https://ucc.readthedocs.io/en/latest/benchmarking.html) in the docs.
<!-- end-how-does-ucc-stack-up -->

## Contributing

We’re building UCC as a community-driven project.
Your contributions help improve the tool for everyone!
There are many ways you can contribute, such as

- **Create a Custom Compiler Pass**: Learn how in the [User Guide](https://ucc.readthedocs.io/en/latest/user_guide.html)
- **Submit a bug report or feature request**: Submit a bug report or feature request [on GitHub](https://github.com/unitaryfund/ucc/issues/new/choose).
- **Contribute Code**: Follow the [Contribution Guide](https://ucc.readthedocs.io/en/latest/contributing.html) to submit new passes and improvements.

If you have questions about contributing please ask on the [Unitary Foundation Discord](http://discord.unitary.foundation).

## License

UCC is distributed under [GNU Affero General Public License version 3.0](https://www.gnu.org/licenses/agpl-3.0.en.html)(AGPLv3).
Parts of ucc contain code or modified code that is part of Qiskit, which is distributed under Apache 2.0 license.
