Quickstart
==========

This project defines two pytest markers that allow linking of
tests to requirement and usecase IDs.


Installation and Setup
----------------------

To use this plugin, add it to your test dependencies, e.g. like this:

.. code-block:: toml
   :caption: ``pyproject.toml``
   :emphasize-lines: 4

   [project.optional-dependencies]
   test = [
     "pytest",
     "pytest-requirements",
     "pytest-cov",
   ]

And enable the plugin via the ``addopts`` configuration option:

.. code-block:: toml
   :caption: ``pyproject.toml``
   :emphasize-lines: 4

   [tool.pytest.ini_options]
   minversion = "7"
   testpaths = ["src"]
   addopts = ["-p", "pytest_requirements"]


Linking tests to requirements and usecases
------------------------------------------

Then you can use two markers to connect your tests to usecases and requirements:

.. code-block:: python

   import pytest

   @pytest.mark.verifies_requirement("B-DPPS-0123")
   def test_super_important_requirement():
       pass


   @pytest.mark.verifies_usecase("UC-130-2.1")
   def test_super_important_usecase():
       pass


Generating XML reports
----------------------

The requirement and usecase IDs are also included in the ``junit``-style xml reports:

.. code-block:: shell

   $ pytest --junit-xml=report.xml

``report.xml`` will contain properties for each marker in the corresponding ``<testcase>``-node of the form:

.. code-block:: xml

   <property name="requirement_id" value="B-DPPS-0123" />
   <property name="usecase_id" value="UC-123-2.1" />
