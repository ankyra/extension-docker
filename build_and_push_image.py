#!/usr/bin/env python

import json
import os
import sys
import subprocess
sys.path = ["deps/_/stdlib"] + sys.path
import escape

outputs_path = sys.argv[1]

env = os.environ
docker_image = env['INPUT_docker_image']
docker_image_version = env['INPUT_docker_image_version']
docker_file = env['INPUT_docker_file']
docker_repo = env['INPUT_docker_repository']
docker_username = env['INPUT_docker_username']
docker_password = env['INPUT_docker_password']
docker_email = env['INPUT_docker_email']
docker_server = env['INPUT_docker_server']
should_push = docker_repo != ''
should_login = docker_username != ''
docker_cmd = json.loads(env['INPUT_docker_cmd'])

if not os.path.exists(docker_file):
    print "Referenced docker file '%s' does not exist" % docker_file
    sys.exit(1)

base_image_name = docker_image
if should_push:
    if not docker_repo.endswith("/"):
        docker_repo = docker_repo + "/"
    base_image_name = docker_repo + base_image_name

versioned_base_image = base_image_name + ":" + docker_image_version


def run_docker(cmd):
    print "Running '%s'" % " ".join(cmd)
    try:
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError, e:
        print "Failed to run", cmd
        print e
        sys.exit(1)
    return output

if should_login:
    cmd = docker_cmd + ["login", "--username", docker_username, "--password", docker_password]
    if docker_email != '':
        cmd += ["--email", docker_email]
    if docker_server != "":
        cmd += [docker_server]
    run_docker(cmd)

print "Building Docker image '%s'" % versioned_base_image

cmd = docker_cmd + ["build", "-f", docker_file, "-t", versioned_base_image, "."]
run_docker(cmd)

print "Tagging '%s:latest'" % base_image_name
cmd = docker_cmd + ["tag", versioned_base_image, base_image_name + ":latest"]
try:
    subprocess.check_output(cmd)
except:
    # Fallback for Docker <1.10
    cmd = docker_cmd + ["tag", "-f", versioned_base_image, base_image_name + ":latest"]
    run_docker(cmd)

if should_push:
    run_docker(docker_cmd + ["push", versioned_base_image])
    run_docker(docker_cmd + ["push", base_image_name + ":latest"])

outputs = json.load(open(outputs_path))
outputs["image"] = versioned_base_image
with open(outputs_path, "w") as f:
    json.dump(outputs, f)
