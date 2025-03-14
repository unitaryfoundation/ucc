Changelog
=========

[0.4.4] - 2025-03-13
--------------------

In version 0.4.4, we updated and expanded our documentation and streamlined benchmark data visualization. We also implemented more custom observables for our expectation value benchmarks, improved the user experience for adding custom transpiler passes, and switched to using the `FullPeepHoleOptimize` function to benchmark PyTKET based on feedback from the community!

Added
^^^^^^^^^^^^^^^^^^^^^

- Enable repeat use of `UCCDefault1` and update documentation. #268 [@bachase]
- Support custom passes in `ucc.compile`. #301 [@bachase]
- Add note defining `pytket-peep` in README. #284 [@jordandsullivan]
- Add `dependabot` for automated dependency updates. #297 [@bachase]

Fixed
^^^^^^^^^^^^^^^^^^^^^

- Improve reproducibility and consistency of benchmarking workflow. #253 [@bachase]
- Ensure `target_device` is used when specified, not just connectivity, when compiling. #290 [@bachase]

Changed
^^^^^^^^^^^^^^^^^^^^^

- Change QAOA observable to use the problem Hamiltonian. #260 [@Misty-W]
- Switch PyTKET to use `FullPeepHoleOptimize`. #266 [@jordandsullivan]
- Adjust plotting scripts to change resolution to per release in time series plots. #254 [@Misty-W]
- Update Poetry lock file, Qiskit, and PyTKET versions. #294 [@jordandsullivan]
- Relabel Qiskit data in plots. #300 [@jordandsullivan]

Removed
^^^^^^^^^^^^^^^^^^^^^

- Remove violin plots from benchmark visualizations. #282 [@jordandsullivan]
- Remove outdated README reference to custom transpiler passes. #274 [@jordandsullivan]
- Remove specific dated data from plots. #283 [@jordandsullivan]

[0.4.3] - 2025-02-26
--------------------

In version 0.4.3, we enhanced UCC infrastructure, benchmarking, and documentation.
Release highlights include the introduction of
[Poetry](https://github.com/python-poetry/install.python-poetry.org) for dependency management,
the automated display of results from benchmarks run on the `main` branch,
and plotting of expectation value benchmark results.
In the case of quantum volume circuits, we changed the expectation value metric from the default
ZZZZZZZZZZZ observable to the heavy output probability.


Added
^^^^^^^^^^^^^^^^^^^^^

- Mention benchpress explicitly in License section. #241 [@jordandsullivan]
- Add target gate set for cirq benchmarking #224 [@bachase]
- Add ruff for linting and formating #216 [@bachase]
- Added warnings to top level compile function for trying to import non-supported python versions #185 [@jordandsullivan]
- Add explicit Sphinx config in .readthedocs.yaml file #180 [@Misty-W]


Fixed
^^^^^^^^^^^^^^^^^^^^^

- Ensure benchmarking runs don't add gitignored files #247 [@bachase]
- Pull latest compatible version of libraries when generating benchmark docker #244 [@bachase]
- Fix broken links in docs #240 [@bachase]
- Fix spelling mistake #237 [@natestemen]
- Fix relative path bug in expval benchmarking script #231 [@natestemen]
- Fix typo in readme for supported formats #230 [@bachase]
- Fix benchmark script to work with poetry #214 [@bachase]
- Combine recent data files w/ incomplete benchmarks #207 [@Misty-W]


Changed
^^^^^^^^^^^^^^^^^^^^^

- Run pytest before ruff linter checks #267 [@jordandsullivan]
- Clarify poetry usage #265 [@bachase]
- Update Install Poetry link to instructions for installation #257 [@jordandsullivan]
- Upgrade dependencies #250 [@bachase]
- Change QV error rates back to global variables #248 [@Misty-W]
- Update documentation to expand on design goals: #245 [@bachase]
- Change expectation value metric to HOP for QV circuits #223 [@Misty-W]
- Switch to poetry for dependency management #208 [@bachase]
- Test run benchmarks with simple wording change #205 [@Misty-W]
- Wording #198 [@jordandsullivan]
- Test deploy key push access #197 [@jordandsullivan]
- Plot adjustments #183 by jordandsullivan
- Minor docs updates #181 by Misty-W
- Update README.md #178 by willzeng


Removed
^^^^^^^^^^^^^^^^^^^^^

- Remove custom transpilation passes #256 [@bachase]


[0.4.2] - 2025-01-17
--------------------

Version 0.4.2 marks the first formal release to [PyPI](https://pypi.org/project/ucc/) of the Unitary Compiler Collection (UCC), a Python library for frontend-agnostic, high performance compilation of quantum circuits.

This release contains the default UCC compilation workflow, including circuit translation and optimization passes, pass management, and the user interface.
It also encompasses benchmarking scripts and utilities, tests, documentation, and basic infrastructure.

Added
^^^^^^^^^^^^^^^^^^^^^

- PyPI release #165 [@Misty-W]
- Add RTD for online documentation #164 [@natestemen]
- Create contribution guide #157 [@natestemen]
- Plot compiler versions over time on graph #145 [@jordandsullivan]
- Add platform info to header #144 [@jordandsullivan]
- Speed up Github benchmarks #140 [@]
- Test GitHub actions for benchmarking pipeline #129 [@jordandsullivan]
- Save compiler versions with data #123 [@]
- Generate plot via GitHub actions pipeline #114 [@jordandsullivan]
- Clean up unnecessary files #101 [@jordandsullivan]
- Reorganize results files #97 [@jordandsullivan]
- Set up AWS workflow for benchmarking #93 [@jordandsullivan]
- Expand logical equivalence test #91 [@Misty-W]
- Add synthesis sequence that preserves natural gateset #89 [@Misty-W]
- Improve routing algorithm #85 [@Misty-W]
- Add benchmark for qubit mapping #83 [@Misty-W]
- Test to check that output circuits from ucc benchmarking are in the natural gate set #82 [@Misty-W]
- Reorganize code structure #70 [@Misty-W]
- Add expectation value benchmark #66 [@natestemen]
- benchmark script #64 [@jordandsullivan]
- Add Qiskit Optimization pass(es) that improve UCC gate reduction #60 [@Misty-W]
- Run first hardware benchmarks #58 [@jordandsullivan]
- Create contribution guide for new transpiler passes #56 [@jordandsullivan]
- Create user guide #54 [@Misty-W]
- Display most recent benchmarks #53 [@jordandsullivan]
- Add CI/CD for tests #52 [@natestemen]
- Expand README with examples #51 [@jordandsullivan]
- Generate API guide with Sphinx #50 [@natestemen]
- Version release and changelog #47 [@natestemen]
- Separate qasm benchmark files from code to generate them #45 [@jordandsullivan]
- Profile code and triage speedups #44 [@jordandsullivan]
- Add tests to check logical equivalence of small circuits #35 [@natestemen]
- confirm licensing requirements #20 [@nathanshammah, @jordandsullivan]
- Non-quantum things to improve the robustness of our package, e.g. CI/CD #20 [@nathanshammah]
- Handle parameterized 1Q gates #19 [@sonikaj]
- Add qubit mapping pass #18 [@sonikaj]
- Docstrings for modified transpiler passes [@sonikaj]
- replace QuantumTranslator with qBraid.transpile #15 In unitaryfund/ucc [@jordandsullivan]
- Add a README #7 [@nathanshammah, @jordandsullivan]
- Add custom UCC transpiler code to ucc/ucc module #6 [@sonikaj]
- Add benchmarks #2 [@jordandsullivan]
- Choose a license #1 [@jordandsullivan]


Fixed
^^^^^^^^^^^^^^^^^^^^^

- Install error due to openqasm versioning #154 [@Misty-W]
- fix small_test.sh CLI command to deal with spaces in paths #152 [@willzeng]
- Mismatched headers in datafiles #148 [@jordandsullivan]
- run-benchmarks action is failing on PRs #138 [@jordandsullivan]
- Fix cirq transformers import #126 [@jordandsullivan]
- RebaseTket function not compatible #118 [@jordandsullivan]
- qiskit blocks_to_matrix no longer imports #111 [@Misty-W]
- Shell script crashes computer #99 [@jordandsullivan]
- Compiled output circuit doesn't dump to OpenQASM 2.0 or 3.0 #80 [@Misty-W]
- Other qcs/quil install errors #75 [@willzeng]
- Hidden rust dependency on install #74 [@Misty-W]


Removed
^^^^^^^^^^^^^^^^^^^^^

- Remove innaccurate data for multi-q gates #86 [@jordandsullivan]
- Remove QuantumTranslator references #23 [@jordandsullivan]
