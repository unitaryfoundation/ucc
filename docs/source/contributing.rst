Contributing Guide
==================

Thank you for your interest in contributing to UCC!
All contributions to this project are welcome, and they are greatly appreciated; every little bit helps.
The most common ways to contribute here are

1. opening an `issue <https://github.com/unitaryfoundation/ucc/issues/new/choose>`_ to report a bug or propose a new feature, or ask a question, and
2. opening a `pull request <https://github.com/unitaryfoundation/ucc/pulls>`_ to fix a bug, or implement a desired feature.

For issues/contributions related to benchmarks, please open in the `ucc-bench <https://github.com/unitaryfoundation/ucc-bench>`_ repo

The rest of this document describes the technical details of getting set up to develop, and make your first contribution to ucc.

Setting up your development environment
---------------------------------------

We leverage `uv <https://docs.astral.sh/uv/>`_ for packaging and dependency management.
After installing uv, run the following commands to clone the repository, create a uv managed virtual environment for development, and install dependencies.

.. code:: bash

    git clone https://github.com/unitaryfoundation/ucc.git
    cd ucc
    uv sync --all-extras --all-groups

This particular invocation of ``uv sync`` ensures optional developer and documentation dependencies are installed.

For all of the following commands, we assume you either prefix each command with ``uv run``, or
you first activate the `uv managed virtual environment <https://docs.astral.sh/uv/pip/environments/#using-a-virtual-environment>`_ by running ``source .venv/bin/activate`` in your shell.

For more details on using uv, refer to its `documentation <https://docs.astral.sh/uv/>`__ or `this tutorial <https://realpython.com/python-uv/>`__.

To run the unit tests, you can use the following command

.. code:: bash

    pytest ucc

and build the documentation by changing to the ``docs/source`` directory where you can run

.. code:: bash

    make html

The built documentation will then live in ``ucc/docs/source/_build/html``.

To test that code examples in the documentation work as expected, you can run

.. code:: bash

    make doctest

This leverages Sphinx `doctest extension <https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html>`_ .

We also use `pre-commit <https://pre-commit.com/>`_ to run code formatting and linting checks before each commit.
To enable the pre-commit hooks, run

.. code:: bash

    pre-commit install

.. tip::

    Remember to run the tests and build the documentation before opening a pull request to ensure a smoother pull request review.

Contributing a New Compiler Pass
--------------------------------

1. Proposing a New Compiler Pass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have an idea for a new compiler pass, please feel free to create an `issue <https://github.com/unitaryfoundation/ucc/issues/new/choose>`_.
If you have a formal proposal for a new compiler pass you intend to develop in UCC, please fill out this `New Compiler Pass Proposal template <https://github.com/unitaryfoundation/ucc/discussions/categories/new-compiler-pass>`_.

2. Implementing and Validating a Prototype of the Pass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Create a prototype
    * A Jupyter notebook or a small script is sufficient for the prototype.

#. Validate the prototype
    * Use the test circuits you defined in your proposal to validate the technique.

3. Implementing the New Pass in the Codebase
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the prototype is validated, implement the new pass in the codebase.
Documentation to guide you through this process is available in the :doc:`user guide <user_guide>`.
For more detailed information and examples, refer to the `Qiskit documentation <https://docs.quantum.ibm.com/guides/custom-transpiler-pass>`_.

4. Clear Acceptance Criteria for Incorporation into default transpiler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the new pass to be incorporated into `the default compiler <https://github.com/unitaryfoundation/ucc/blob/main/ucc/transpilers/ucc_defaults.py>`_, it must meet the following criteria:

#. Reduction in compiled 2-qubit gate count
    * Demonstrate a reduction in the number of 2-qubit gates.

#. Reduction in runtime
    * Show a reduction in runtime, especially if the new technique replaces a slower one.

#. Passes should not cause new bugs or worsen performance
    * Whether the new pass is meant to run alongside existing passes or replace some of them, we check that it doesn't cause any unexpected bugs, break any existing tests, or worsen performance.

#. Integration with the library vs. default transpiler
    * It's important to know that a new pass might be accepted into the library of passes but not necessarily integrated into the default transpiler. You can see examples of this in `this discussion <https://github.com/unitaryfoundation/ucc/discussions/392>`_ and `this pull request <https://github.com/unitaryfoundation/ucc/pull/421>`_.

#. Benchmarking your new pass
    * To run benchmarks on your new pass, please refer to the `tutorial and documentation <https://github.com/unitaryfoundation/ucc/issues/469>`_ on using ucc-bench.

We appreciate your contributions and look forward to your new pass proposals!

Code of Conduct
---------------

UCC development abides by the :doc:`CODE_OF_CONDUCT`.
