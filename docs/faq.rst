================================
Frequently Asked Questions (FAQ)
================================

What is the effect of using ``sudo -E``?
========================================

You may notice the use of ``sudo -E`` in several commands in this guide. Using
``-E`` with ``sudo`` allows you to carry over all the environment variables
into the ``sudo`` command. Most importantly, this lets use use the contents
of ``PATH`` with ``sudo``, which gives access to the right path for ``conda``,
``pip``, etc.
