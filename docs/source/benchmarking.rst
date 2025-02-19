.. _benchmarks:

Benchmarking
############

UCC includes a benchmarking suite to evaluate the performance of its quantum circuit compiler.
These benchmarks help validate improvements, compare performance across compilers, and guide future optimizations.
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
      - The current compiler settings are defined `here <https://github.com/unitaryfund/ucc/blob/fde89f6e25f3adc2b47313e3e1c7cc0b5b2e1a18/benchmarks/scripts/common.py#L90-L207>`_ and we welcome contributions to these defaults as suggested below.

3. **Metrics**: We track several metrics to evaluate compiler performance:
    - *Compiled Gatecount Ratio*: Measures the ratio of 2-qubit gates in the compiled versus raw circuit.
    - *Compilation Time*: Tracks the time taken to compile a circuit.
    - *Observable under noise*: Measures the fidelity of the compiled circuit under noise, using an observable relevant for that circuit.

4. **Reproducibility**: In order to ensure the reliability of our benchmarks, we follow these practices:
    - Benchmark scripts and results are available in the `UCC repository <https://github.com/unitaryfund/ucc/tree/main/benchmarks>`_.
    - Results are stored in version-controlled reports to track improvements over time.
    - Official results are run using a dedicated machine for consistent comparison.

Running the benchmarks
----------------------

To run the benchmarks locally, first follow the steps in the
:doc:`contributing guide <contributing>` to setup your dev environment. Then, run
the benchmark script via:

.. code-block:: sh

   poetry run ./benchmarks/scripts/run_benchmarks.sh <num_parallel>

where ``num_parallel`` is the number of parallel processes to run on. The results are stored in
``benchmarks/results/`` as CSV files.

The script assumes you have GNU parallel available on your machine, available
via ``apt-get install parallel`` on Ubuntu or ``brew install parallel`` on MacOS.

Contributing to benchmarks
--------------------------

We welcome contributions to improve UCC’s benchmarking suite! This could include

- **Adding New Benchmark Circuits** to cover an additional real-world use case.
- **Improving Benchmark Metrics** to add additional metrics of interest to compare compiler performance.
- **Optimizing Compiler Configurations** to improve the default configuration of compilers in the benchmark.
     - The current compiler settings are defined `here <https://github.com/unitaryfund/ucc/blob/fde89f6e25f3adc2b47313e3e1c7cc0b5b2e1a18/benchmarks/scripts/common.py#L90-L207>`_.
     - For Qiskit, a change could be to the `optimization level set when transpiling <https://github.com/unitaryfund/ucc/blob/bbf6042951606a6999658036507e219674577f68/benchmarks/scripts/common.py#L108>`_.
     - For Cirq, a change could update the `gate set optimization passes <https://github.com/unitaryfund/ucc/blob/bbf6042951606a6999658036507e219674577f68/benchmarks/scripts/common.py#L113>`_ used when compiling.

Take a look at
:doc:`contributing guide <contributing>` for the more general steps to follow on making contributions to the UCC codebase.
