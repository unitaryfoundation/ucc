.. _benchmarks:

Benchmarking
############

UCC includes a benchmarking suite to evaluate the performance of its quantum circuit compiler.
These benchmarks help validate improvements, compare performance across compilers, and guide future optimizations.
The benchmarking code, configuration and results are maintained in the companion repository `ucc-bench <https://github.com/unitaryfoundation/ucc-bench>`_.
This guide explains the **purpose**, **design**, and **execution** of UCC benchmarks and how you can contribute.

Purpose
-------
UCC seeks to provide an end-to-end compiler that works well for the majority of the users out of the box across a
wide range of use cases. To ensure our optimizations are effective, we run regular benchmarks that:

- Compare UCC's compiler performance against leading quantum compilers.
- Evaluate metrics such as gate count reduction, runtime performance and noise performance.
- Test across a diverse set of quantum circuits, ensuring optimizations generalize beyond specific cases.
- Provide reproducible results to guide future improvements in UCC’s compiler pipeline.

Benchmark design & methodology
------------------------------

Our benchmarks follow a structured methodology to ensure consistency and reliability.

1. **Circuits**: A selection of circuits for standard quantum algorithms such as QFT, QAOA, Quantum Volume, and QCNN. Circuits are selected to cover a range of qubit counts gate structures, and depth complexities.
     - Many of the included circuits are from the `benchpress <https://github.com/Qiskit/benchpress>`_ benchmarking suite.

2. **Compilers**: UCC is benchmarked comparing its default passes (defined in :class:`ucc.transpilers.ucc_defaults.UCCDefault1`) against other similar defaults for leading compilers, including `Qiskit <https://github.com/Qiskit/qiskit>`_, `Cirq <https://github.com/quantumlib/Cirq>`_, and `PyTKET <https://github.com/CQCL/tket>`_.

3. **Metrics**: We track several metrics to evaluate compiler performance:
    - *Compiled Gate count Ratio*: Measures the ratio of 2-qubit gates in the compiled versus raw circuit.
    - *Compilation Time*: Tracks the time taken to compile a circuit.
    - *Observable under noise*: Measures the fidelity of the compiled circuit under noise, using an observable relevant for that circuit.

4. **Reproducibility**: In order to ensure the reliability of our benchmarks, we follow these practices:
    - Benchmark scripts and results are available in the `ucc-bench <https://github.com/unitaryfoundation/ucc-bench>`_ repository.
    - Results are stored in version-controlled reports to track improvements over time.
    - Official results are run using a dedicated machine for consistent comparison.

Running the benchmarks
----------------------

To run the benchmarks locally, follow the steps in the
`ucc-bench README <https://github.com/unitaryfoundation/ucc-bench/blob/main/README.md#usage-running-a-benchmark-suite>`_. These instructions
will tell you how to setup your environment, install the required dependencies, and run the benchmarks.


Circuits
--------
ucc-bench currently benchmark circuits (see `here <https://github.com/unitaryfoundation/ucc-bench/tree/main/benchmarks/circuits>`__) for the problems below

- **QAOA on Barabási-Albert Graph** – A variational algorithm to determine max-cut of a scale-free network.
  *Reference*: Farhi et al., *A Quantum Approximate Optimization Algorithm*, `arXiv:1411.4028 <https://arxiv.org/abs/1411.4028>`_
  *Circuit from benchpress*

- **Quantum Volume Circuit** – Randomized circuit used to assess quantum device performance via heavy output probability.
  *Reference*: Cross et al., *Validating quantum computers using randomized model circuits*, `arXiv:1811.12926 <https://arxiv.org/abs/1811.12926>`_
  *Circuit from benchpress*

- **Quantum Fourier Transform (QFT)** – Core subroutine for quantum algorithms including factoring.
  *Reference*: Nielsen and Chuang, *Quantum Computation and Quantum Information*
  *Circuit from benchpress*

- **Square Heisenberg Model** – Simulates spin interactions on a lattice using a Heisenberg Hamiltonian.
  *Reference*: Whitfield et al., *Simulation of electronic structure Hamiltonians using quantum computers*, `arXiv:1001.3855 <https://arxiv.org/abs/1001.3855>`_
  *Circuit from benchpress*

- **GHZ State Preparation** – Constructs a maximally entangled GHZ state for testing multi-qubit correlations.
  *Reference*: Greenberger et al., *Going Beyond Bell’s Theorem*, `arXiv:0712.0921 <https://arxiv.org/abs/0712.0921>`_

- **Quantum Convolutional Neural Network (QCNN)** – Quantum machine learning architecture for classification tasks.
  *Reference*: Cong et al., *Quantum Convolutional Neural Networks*, `arXiv:1810.03787 <https://arxiv.org/abs/1810.03787>`_

Compiler Configurations
-----------------------
For benchmarking, UCC follows the documentation of the respective compilers to set up the default configurations.
This is consistent with UCC's design philosophy is to make compiling easy and painless for people running quantum algorithms,
and not require the user to have in-depth knowledge of compilation to get solid performance.

All compilers target a basis gateset of RX, RY, RZ, H and CNOT gates to ensure we have an apples-to-apples comparison of circuit properties
post compilation, including the number of multi-qubit gates.

To see the compiler specific configuration, consult the corresponding python class implemented in the ``ucc-bench.compilers`` module
viewable `here <https://github.com/unitaryfoundation/ucc-bench/tree/main/src/ucc_bench/compilers>`__. Of note

- **Qiskit** is configured with ``optimization_level`` 3.
- **Cirq** relies on a custom written ``BenchmarkTargetGateset`` to target the above mentioned basis gates.
- **PyTKET** uses the  "`Full Peephole <https://docs.quantinuum.com/tket/api-docs/passes.html#pytket.passes.FullPeepholeOptimise>`_" optimization strategy.
- **PyQPanda3** uses optimization level 2. Note that PyQPanda3 is not open source.


Contributing to benchmarks
--------------------------

We welcome contributions to improve UCC’s benchmarking suite! This could include

- **Adding New Benchmark Circuits** to cover an additional real-world use case.
- **Improving Benchmark Metrics** to add additional metrics of interest to compare compiler performance.
- **Optimizing Compiler Configurations** to improve the default configuration of compilers in the benchmark.

To contribute, please open an issue in the `ucc-bench <https://github.com/bachase/ucc-bench>`__ repository.
