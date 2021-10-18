.. _contributing/tests:

============
Testing TLJH
============

Unit and integration tests are a core part of TLJH, as important as
the code & documentation. They help validate that the code works as
we think it does, and continues to do so when changes occur. They
also help communicate in precise terms what we expect our code
to do.

Integration tests
=================

TLJH is a *distribution* where the primary value is the many
opinionated choices we have made on components to use and how
they fit together. Integration tests are perfect for testing
that the various components fit together and work as they should.
So we write a lot of integration tests, and put in more effort
towards them than unit tests.

All integration tests are run in `GitHub Actions <https://github.com/jupyterhub/the-littlest-jupyterhub/actions>`_
for each PR and merge, making sure we don't have broken tests
for too long.

The integration tests are in the ``integration-tests`` directory
in the git repository. ``py.test`` is used to write the integration
tests. Each file should contain tests that can be run in any order
against the same installation of TLJH.

Running integration tests locally
---------------------------------

You need ``docker`` installed and callable by the user running
the integration tests without needing sudo.

You can then run the tests with:

.. code-block:: bash

   .github/integration-test.py run-test <name-of-run> <test-file-names>

- ``<name-of-run>`` is an identifier for the tests - you can choose anything you want
- ``<test-file-names>>`` is list of test files (under ``integration-tests``) that should be run in one go.

For example, to run all the basic tests, you would write:

.. code-block:: bash

   .github/integration-test.py run-test basic-tests \
      test_hub.py \
      test_proxy.py \
      test_install.py \
      test_extensions.py

This will run the tests in the three files against the same installation
of TLJH and report errors.

If you would like to run the tests with a custom pip spec for the bootstrap script, you can use the ``--bootstrap-pip-spec``
parameter:

.. code-block:: bash

   .github/integration-test.py run-test <name-of-run> <test-file-names> \
      --bootstrap-pip-spec="git+https://github.com/your-username/the-littlest-jupyterhub.git@branch-name"
