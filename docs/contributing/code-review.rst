.. _contributing/code-review:

======================
Code Review guidelines
======================

This document outlines general guidelines to follow when you are making
or reviewing a Pull Request.

Have empathy
============

We recommend reading `On Empathy & Pull Requests <https://slack.engineering/on-empathy-pull-requests-979e4257d158>`_
and `How about code reviews <https://slack.engineering/how-about-code-reviews-2695fb10d034>`_
to learn more about being empathetic in code reviews.

Write documentation
===================

If your pull request touches any code, you must write or update documentation
for it. For this project, documentation is a lot more important than the code.
If a feature is not documented, it does not exist. If a behavior is not documented, 
it is a bug. 

Do not worry about having perfect documentation! Documentation improves over
time. The requirement is to have documentation before merging a pull request,
not to have *perfect* documentation before merging a pull request. If you
are new and not sure how to add documentation, other contributors will
be happy to guide you.

See :ref:`contributing/docs` for guidelines on writing documentation.

Write tests
===========

If your pull request touches any code, you must write unit or integration tests
to exercise it. This helps validate & communicate that your pull request works
the way you think it does. It also makes sure you do not accidentally break
other code, and makes it harder for future pull requests to break the code
added in your pull request.

Since TLJH is a distribution that integrates many JupyterHub components,
integration tests provide more value for effort than unit tests do. Unit
tests are easier to write & faster to run, so if the code being changed
feels exhaustively unit-testable, write unit tests too. When in doubt,
add more tests.

If you are unsure what kind of tests to add for your pull request, other
contributors to the repo will be happy to help guide you!

See :ref:`contributing/tests` for guidelines on writing tests.
