#!/bin/bash

set -euf -o pipefail

base_image_name="${INPUT_docker_image}"
if [ "${INPUT_docker_repository}" != "" ] ; then
    base_image_name="${INPUT_docker_repository}/${base_image_name}"
fi
versioned_base_image="${base_image_name}:${INPUT_docker_image_version}"

echo "Using ${versioned_base_image}"
echo "${versioned_base_image}" > "${INPUT_docker_tmp_file}"
