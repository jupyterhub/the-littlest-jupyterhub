.. _contributing/docs:

=====================
Writing documentation
=====================

.. note::

   Heavily inspired by the
   `django project's guidelines <https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/>`_

We place a high importance on consistency, readability and completeness of documentation.
If a feature is not documented, it does not exist. If a behavior is not documented,
it is a bug! We try to treat our
documentation like we treat our code: we aim to improve it as often as
possible.

Documentation changes generally come in two forms:

* General improvements: typo corrections, error fixes and better
  explanations through clearer writing and more examples.

* New features: documentation of features that have been added to the
  framework since the last release.

This section explains how writers can craft their documentation changes
in the most useful and least error-prone ways.

Getting the raw documentation
=============================

Though TLJH's documentation is intended to be read as HTML at
https://the-littlest-jupyterhub.readthedocs.io/, we edit it as a collection of text files for
maximum flexibility. These files live in the top-level ``docs/`` directory of
TLJH's repository.

If you'd like to start contributing to our docs, get the development version of
TLJH from the source code repository. The development version has the
latest-and-greatest documentation, just as it has latest-and-greatest code.

Getting started with Sphinx
===========================

TLJH's documentation uses the Sphinx__ documentation system, which in turn
is based on docutils__. The basic idea is that lightly-formatted plain-text
documentation is transformed into HTML, PDF, and any other output format.

__ http://sphinx-doc.org/
__ http://docutils.sourceforge.net/

To build the documentation locally, install the Sphinx dependencies:

.. code-block:: console

     $ cd docs/
     $ pip install -r requirements.txt

Then from the ``docs`` directory, build the HTML:

.. code-block:: console

     $ make html

If you encounter this error, it's likely that you are running inside a virtual environment.

.. code-block:: console

   Error in "currentmodule" directive:

To get started contributing, you'll want to read the :ref:`reStructuredText
reference <sphinx:rst-index>`

Your locally-built documentation will be themed differently than the
documentation at `the-littlest-jupyterhub.readthedocs.io <https://the-littlest-jupyterhub.readthedocs.io>`_.
This is OK! If your changes look good on your local machine, they'll look good
on the website.

How the documentation is organized
==================================

The documentation is organized into several categories:

* **Tutorials** take the reader by the hand through a series
  of steps to create something.

  The important thing in a tutorial is to help the reader achieve something
  useful, preferably as early as possible, in order to give them confidence.

  Explain the nature of the problem we're solving, so that the reader
  understands what we're trying to achieve. Don't feel that you need to begin
  with explanations of how things work - what matters is what the reader does,
  not what you explain. It can be helpful to refer back to what you've done and
  explain afterwards.

  **Installation Tutorials** are a special subcategory of tutorials that
  teach the user how to install TLJH in various cloud providers / bare metal
  systems. These should cross-link a lot to other parts of the documentation,
  avoid forcing the user to learn to SSH if possible & have lots of screenshots.

* **Topic guides** aim to explain a concept or subject at a
  fairly high level.

  Link to reference material rather than repeat it. Use examples and don't be
  reluctant to explain things that seem very basic to you - it might be the
  explanation someone else needs.

  Providing background context helps a newcomer connect the topic to things
  that they already know.

* **Reference guides** contain technical reference for APIs.
  They describe the functioning of TLJH's internal machinery and instruct in
  its use.

  Keep reference material tightly focused on the subject. Assume that the
  reader already understands the basic concepts involved but needs to know or
  be reminded of how TLJH does it.

  Reference guides aren't the place for general explanation. If you find
  yourself explaining basic concepts, you may want to move that material to a
  topic guide.

* **How-to guides** are recipes that take the reader through
  steps in key subjects.

  What matters most in a how-to guide is what a user wants to achieve.
  A how-to should always be result-oriented rather than focused on internal
  details of how TLJH implements whatever is being discussed.

  These guides are more advanced than tutorials and assume some knowledge about
  how TLJH works. Assume that the reader has followed the tutorials and don't
  hesitate to refer the reader back to the appropriate tutorial rather than
  repeat the same material.

* **Troubleshooting guides** help reader answer the question "Why is my JupyterHub
  not working?".

  These guides help readers try find causes for their symptoms, and hopefully fix
  the issues. Some of these need to be specific to cloud providers, and that is
  acceptable.

Writing style
=============

Typically, documentation is written in second person, referring to the reader as “you”. 
When using pronouns in reference to a hypothetical person, such as "a user with
a running notebook", gender neutral pronouns (they/their/them) should be used.
Instead of:

* he or she... use they.
* him or her... use them.
* his or her... use their.
* his or hers... use theirs.
* himself or herself... use themselves.

Commonly used terms
===================

Here are some style guidelines on commonly used terms throughout the
documentation:

* **TLJH** -- common abbreviation of The Littlest JupyterHub. Fully
  capitalized except when used in code / the commandline.

* **Python** -- when referring to the language, capitalize Python.

* **Notebook Interface** -- generic term for referring to JupyterLab,
  nteract, classic notebook & other user interfaces for accessing


Guidelines for reStructuredText files
=====================================

These guidelines regulate the format of our reST (reStructuredText)
documentation:

* In section titles, capitalize only initial words and proper nouns.

* Wrap the documentation at 120 characters wide, unless a code example
  is significantly less readable when split over two lines, or for another
  good reason.


* Use these heading styles::

    ===
    One
    ===

    Two
    ===

    Three
    -----

    Four
    ~~~~

    Five
    ^^^^

Documenting new features
========================

Our policy for new features is:

    All new features must have appropriate documentation before they
    can be merged.

Choosing image size
===================

When adding images to the documentation, try to keep them as small as possible.
Larger images make the site load more slowly on browsers, and may make the site
inaccessible for people with a slow internet connection.

If you're adding screenshots, make the size of your shot as small as possible.
If you're uploading large images, consider using an image optimizer in order
to reduce its size.

For example, for PNG files, use OptiPNG and AdvanceCOMP's ``advpng``:

.. code-block:: console

   $ cd docs
   $ optipng -o7 -zm1-9 -i0 -strip all `find . -type f -not -path "./_build/*" -name "*.png"`
   $ advpng -z4 `find . -type f -not -path "./_build/*" -name "*.png"`

This is based on OptiPNG version 0.7.5. Older versions may complain about the
``--strip all`` option being lossy.

Spelling check
==============

Before you commit your docs, it's a good idea to run the spelling checker.
You'll need to install a couple packages first:

* `pyenchant <https://pypi.org/project/pyenchant/>`_ (which requires
  `enchant <https://www.abisource.com/projects/enchant/>`_)

* `sphinxcontrib-spelling
  <https://pypi.org/project/sphinxcontrib-spelling/>`_

Then from the ``docs`` directory, run ``make spelling``. Wrong words (if any)
along with the file and line number where they occur will be saved to
``_build/spelling/output.txt``.

If you encounter false-positives (error output that actually is correct), do
one of the following:

* Surround inline code or brand/technology names with grave accents (`).
* Find synonyms that the spell checker recognizes.
* If, and only if, you are sure the word you are using is correct - add it
  to ``docs/spelling_wordlist`` (please keep the list in alphabetical order).
