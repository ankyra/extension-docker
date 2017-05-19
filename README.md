# Docker extension for Escape

Please see http://escape.ankyra.io for the full documentation.

Can be used in Escape releases to build and push Docker images

## Usage

```
name: my-release
extends:
- extension-docker
inputs:

- id: docker_image
  default: my_image
  description: > 
      The name of the Docker image to build. Don't specify the repository 
      (see 'Docker Repository') or version here (see 'Docker Image Version')

- id: docker_image_version
  default: $__concat("v", $this.version)
  friendly: Docker Image Version
  description: > 
      The version with which to tag the Docker image.

- id: docker_file
  default: Dockerfile
  friendly: Docker File
  description: > 
      The path of the Dockerfile to use.

- id: docker_repository
  default: ""
  friendly: Docker Repository
  description: > 
      If set the image will be tagged with this repository and
      pushed on every successful build.
```

## License

```
Copyright 2017 Ankyra

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
