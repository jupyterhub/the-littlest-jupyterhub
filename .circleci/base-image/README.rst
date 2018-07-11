========================
TLJH CircleCI Base Image
========================

Miniconda should be installed in the base CircleCI image for our unit tests.
Docker CE should be installed in the base CircleCI image for our integration tests.

This image contains both, so we do not have to build it every single time.

Updating the image
==================

1. Make changes to the ``Dockerfile`` & commit it.
2. Run ``./build.bash`` from this directory. It'll build, tag & push the image with
   the hash of the last commit that touched this directory.
3. Use the new image tag in the ``.circleci/config.yml`` file.
