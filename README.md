# Docker extension for Escape

This Escape release can be used to build and push Docker images. 

Please see https://escape.ankyra.io/docs/ for the full documentation on Escape.

## Usage

### Building an Image

```
name: my-image
version: 1.0.0
extends:
- extension-docker-latest

includes:
- Dockerfile

inputs:
- id: docker_image
  default: my-image-name
```

Running `escape run build` will build the Docker image `my-image-name:v1.0.0`
provided the `Dockerfile` exists. The image is not pushed anywhere. The same 
is true for `escape run deploy`; i.e. the build is repeated. We can avoid 
this by setting the `docker_import_image` variable to true.


### Building and Pushing


```
name: my-image
version: 1.0.0
extends:
- extension-docker-latest

includes:
- Dockerfile

inputs:
- id: docker_image
  default: my-image-name
- id: docker_repository
  default: my-repo/
```

Running this release will build the Docker image `my-repo/my-image-name:v1.0.0`
provided the `Dockerfile` exists. The image is then pushed to `my-repo/` as
long as Docker has been configured with the right credentials. To configure
credentials from within this release the `docker_username`, `docker_password`,
`docker_email`and `docker_server` variables can be used.


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
