.. _howto/content/nbgitpuller:

================================================
Distributing materials to users with nbgitpuller
================================================

Goal
====

A very common need when using JupyterHub is to easily
distribute study materials / lab notebooks to students.

Students should be able to:

1. Easily get the latest version of materials, including any updates the instructor
   has made to materials the student already has a copy of.
2. Be confident they won't lose any of their work. If an instructor has modified
   something the student has also modified, the student's modification should
   never be overwritten.
3. Not have to deal with manual merge conflicts or other complex operations.

Instructors should be able to:

1. Use modern collaborative version control tools to author & store their
   materials. This currently means using Git.

**nbgitpuller** is a Jupyter server extension that helps achieve these goals.
This tutorial will walk you through the process of creating a magic
nbgitpuller link that users of your JupyterHub can click to fetch the latest
version of materials from a git repo.

Pre-requisites
==============

1. A JupyterHub set up with The Littlest JupyterHub
2. A git repository containing materials to distribute

Step 1: Generate nbgitpuller link
=================================

The quickest way to generate a link is to use `nbgitpuller.link
<https://nbgitpuller.link>`_, but other options exist as described in the
`nbgitpuller project's documentation
<https://jupyterhub.github.io/nbgitpuller/use.html>`_.

Step 2: Users click on the nbgitpuller link
===========================================

#. Send the link to your users in some way - email, slack, post a
   shortened version (with `bit.ly <https://bit.ly>`_ maybe) on the wall, or
   put it on your syllabus page (like `UC Berkeley's data8 does <http://data8.org/sp18/>`_).
   Whatever works for you :)

#. When users click the link, they will be asked to log in to the hub
   if they have not already.

#. Users will see a progress bar as the git repository is fetched & any
   automatic merging required is performed.

   .. image:: ../../images/nbgitpuller/pull-progress.png
      :alt: Progress bar with git repository being pulled

#. Users will now be redirected to the notebook specified in the URL!

This workflow lets users land directly in the notebook you specified
without having to understand much about git or the JupyterHub interface.
