#!/bin/bash

set -euf -o pipefail

if [ ! -f "${INPUT_docker_file}" ] ; then
  echo "Referenced Dockerfile '${INPUT_docker_file}' does not exist."
  exit 1
fi

base_image_name="${INPUT_docker_image}"
if [ "${INPUT_docker_repository}" != "" ] ; then
    base_image_name="${INPUT_docker_repository}/${base_image_name}"
fi

versioned_base_image="${base_image_name}:${INPUT_docker_image_version}"

docker build -f "${INPUT_docker_file}" -t "${versioned_base_image}" .
docker tag "${versioned_base_image}" "${base_image_name}:latest"
if [ "${INPUT_docker_repository}" != "" ] ; then
    docker push "${versioned_base_image}"
    docker push "${base_image_name}:latest"
fi

echo "${versioned_base_image}" > "${INPUT_docker_tmp_file}"
