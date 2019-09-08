

=======
Beefore
=======

Beefore is a set of tooling that automatically performs checks on pull requests
(PRs) before they are merged in and reports back any issues. This is done to keep
style consistency across all projects and no matter who is committing the code.
If further information for each of the check that are made is needed, follow the
links referenced in each of the check sections below.


Checks
======

DCO
---

Check for the existence of a Developer Certificate of Origin in the commit.
A DCO is a legally binding statement that asserts that you are the creator of
your contribution, and that you wish to allow BeeWare to use your work.
For more details see
https://pybee.org/contributing/how/dco/


Python Checks
-------------

For checking style on python code `flake8`_
is the tool that is used.

The only exception to the pep8 standards that are applied by flake8 is the allowing
of up to 199 character. Further information about this and what else is expected
can be found at https://pybee.org/contributing/how/process/


Java Checks
-----------

The tool used for checking the standards for java code is `checkstyle`_


Javascript Checks
-----------------

Eslint is the tool that is used to apply the `rules`_


How does it work
================

Each of the projects under Beeware has a beekeeper.yml file that defines checks and tests that are
required. The Beefore tests are part of pull_request and gets kicked off when any pull request is
raised against the project. The request code is checked for the lines that have changed and these
are then run against the style checkers. Should any issues be found the PR will be updated with
the lines that have failed and the reason why. These should be fixed before the PR is resubmitted.

Running locally
---------------

To be developed...


Community
=========

Beefore is part of the `BeeWare suite`_. You can talk to the community through:

 * `@pybeeware on Twitter`_

 * `pybee/general on Gitter`_

.. _flake8: http://flake8.pycqa.org/en/latest/
.. _checkstyle: http://checkstyle.sourceforge.net/
.. _rules: http://eslint.org/docs/rules/
.. _BeeWare suite: http://pybee.org
.. _Read The Docs: https://toga.readthedocs.io
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _pybee/general on Gitter: https://gitter.im/pybee/general
