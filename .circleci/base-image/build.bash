#!/bin/bash
set -euo pipefail

# Very simple script to build and push images
# Should be replaced by chartpress or similar at some point
# Uses google container image builder for simplicity
IMAGE="jupyterhub/tljh-circleci-base-image"
TAG=$(git log -n1 --pretty="%h" .)
IMAGE_SPEC="${IMAGE}:${TAG}"


echo "Building and pushing ${IMAGE_SPEC}"
docker build -t ${IMAGE_SPEC} .
docker push ${IMAGE_SPEC}
echo "Built and pushed ${IMAGE_SPEC}"
