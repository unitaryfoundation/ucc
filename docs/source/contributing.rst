Contributing Guide
==================

Thank you for your interest in contributing to UCC!
All contributions to this project are welcome, and they are greatly appreciated; every little bit helps.
The most common ways to contribute here are

1. opening an `issue <https://github.com/unitaryfund/ucc/issues/new/choose>`_ to report a bug or propose a new feature, or ask a question, and
2. opening a `pull request <https://github.com/unitaryfund/ucc/pulls>`_ to fix a bug, or implement a desired feature.

The rest of this document describes the technical details of getting set up to develop, and make your first contribution to ucc.

Setting up your development environment
---------------------------------------

We leverage `poetry <https://python-poetry.org/>`_ for packaging and dependency management.
After installing poetry, run the following commands to clone the repository, create a poetry managed virtual environment for development, and install dependencies.

.. code:: bash

    git clone https://github.com/unitaryfund/ucc.git
    cd ucc
    poetry install

For all of the following commands, either first run ``poetry shell`` to enable the poetry managed virtual environment,
or prefix each command with ``poetry run``.

.. code:: bash

    pytest ucc

and build the documentation by changing to the ``docs/source`` directory where you can run

.. code:: bash

    make html

The built documentation will then live in ``ucc/docs/source/_build/html``.

We also use `pre-commit <https://pre-commit.com/>`_ to run code formatting and linting checks before each commit.
To enable the pre-commit hooks, run

.. code:: bash

    pre-commit install

.. tip::

    Remember to run the tests and build the documentation before opening a pull request to ensure a smoother pull request review.

Proposing a new transpiler pass
-------------------------------

1. Proposing a New Transpiler Pass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When proposing a new transpiler pass, please include a detailed report containing:

#. Detailed description of the technique
    #. Provide a written abstract without excessive jargon, citing the source of the technique.
    #. (Optional, recommended): Include a diagram showing an example circuit and how it would be affected by this pass.

#. Performance expectations
    #. Estimate how much the technique is expected to reduce gate counts or compile time. This rough estimate helps us prioritize techniques.
    #. Specify which types of circuits are expected to improve or not improve with this technique.
    #. Define test circuits of the above types which you will use to validate the technique.

2. Implementing and Validating a Prototype of the Pass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Create a prototype
    * A Jupyter notebook or a small script is sufficient for the prototype.

#. Validate the prototype
    * Use the test circuits defined in section `1. Proposing a New Transpiler Pass`_ to validate the technique.

.. _1. Proposing a New Transpiler Pass: #proposing-a-new-transpiler-pass

3. Implementing the New Pass in the Codebase
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the prototype is validated, implement the new pass in the codebase.
Documentation to guide you through this process is available in the :doc:`user guide <user_guide>`.
For more detailed information and examples, refer to the `Qiskit documentation <https://docs.quantum.ibm.com/guides/custom-transpiler-pass>`_.

4. Clear Acceptance Criteria for Incorporation into default transpiler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the new pass to be incorporated into `the default compiler <https://github.com/unitaryfund/ucc/blob/main/ucc/transpilers/ucc_defaults.py>`_, it must meet the following criteria:

#. Reduction in compiled 2-qubit gate count
    * Demonstrate a reduction in the number of 2-qubit gates.

#. Reduction in runtime
    * Show a reduction in runtime, especially if the new technique replaces a slower one.

#. Compatibility with other passes
    * Ensure the new pass performs as expected when used with other existing passes.

We appreciate your contributions and look forward to your new pass proposals!

Code of Conduct
---------------

UCC development abides by the :doc:`CODE_OF_CONDUCT`.
