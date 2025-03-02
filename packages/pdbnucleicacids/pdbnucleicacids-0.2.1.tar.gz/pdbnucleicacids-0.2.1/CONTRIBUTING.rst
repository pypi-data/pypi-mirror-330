.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://gitlab.com/MorfeoRenai/pdbnucleicacids/-/issues

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the Gitlab issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the Gitlab issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

PDBNucleicAcids could always use more documentation, whether as part of the
official PDBNucleicAcids docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://gitlab.com/MorfeoRenai/pdbnucleicacids/-/issues

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up PDBNucleicAcids for local development.

1. Fork the PDBNucleicAcids repo on Gitlab.
2. Clone your fork locally:

.. code-block:: console

    $ git clone git@gitlab.com:your_name_here/pdbnucleicacids.git

3. Install your local copy into a virtualenv. Assuming you have
   virtualenvwrapper installed, this is how you set up your fork for
   local development:

.. code-block:: console

    $ mkvirtualenv pdbnucleicacids
    $ cd pdbnucleicacids/
    $ make requirements-dev

4. Create a branch for local development:

.. code-block:: console

    $ git checkout -b name-of-your-bugfix-or-feature

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox:

.. code-block:: console

    $ make lint
    $ make test
    $ make test-all

6. Commit your changes and push your branch to Gitlab:

.. code-block:: console

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the Gitlab website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.8, 3.9, 3.10, 3.11, 3.12 and 3.13,
   and for PyPy. Make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests:

.. code-block:: console

    $ make test

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run:

.. code-block:: console

    $ bump-my-version patch # possible: major / minor / patch
    $ git push
    $ git push --tags


Code of Conduct
---------------

Please note that this project is released with a `Contributor Code of Conduct`_.
By participating in this project you agree to abide by its terms.

.. _`Contributor Code of Conduct`: CODE_OF_CONDUCT.rst
