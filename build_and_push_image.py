#!/usr/bin/env python

import json
import os
import sys
import subprocess
sys.path = ["deps/_/stdlib"] + sys.path
import escape

env = os.environ
docker_image = escape.get_string_input('docker_image')
docker_image_version = escape.get_string_input('docker_image_version')
docker_file = escape.get_string_input('docker_file')
docker_repo = escape.get_string_input('docker_repository')
docker_username = escape.get_string_input('docker_username')
docker_password = escape.get_string_input('docker_password')
docker_email = escape.get_string_input('docker_email')
docker_server = escape.get_string_input('docker_server')
import_image = escape.get_bool_input('docker_import_image')
should_push = docker_repo != ''
should_login = docker_username != ''
docker_cmd = json.loads(env['INPUT_docker_cmd'])

def get_base_image(docker_repo, docker_image, docker_image_version, should_push):
    base_image_name = docker_image
    if should_push:
        if not docker_repo.endswith("/"):
            docker_repo = docker_repo + "/"
        base_image_name = docker_repo + base_image_name
    return base_image_name, base_image_name + ":" + docker_image_version


def run_docker(cmd):
    print "Running '%s'" % " ".join(cmd)
    try:
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError, e:
        print "Failed to run", cmd
        print e
        sys.exit(1)
    return output


def login(docker_cmd, docker_username, docker_password, docker_email, docker_server):
    cmd = docker_cmd + ["login", "--username", docker_username, "--password", docker_password]
    if docker_email != '':
        cmd += ["--email", docker_email]
    if docker_server != "":
        cmd += [docker_server]
    run_docker(cmd)


def build(docker_file, versioned_base_image, docker_cmd, base_image_name):
    if not os.path.exists(docker_file):
        print "Referenced docker file '%s' does not exist" % docker_file
        sys.exit(1)

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

if docker_image == "": 
    print "Missing value for 'docker_image' variable"
    sys.exit(1)

imported = False
if os.path.exists("imported_image"):
    versioned_base_image = open("imported_image").read()
    print "Using imported image", versioned_base_image
    imported = True
    import_image = True
else:
    base_image_name, versioned_base_image = get_base_image(docker_repo, docker_image, docker_image_version, should_push)

if not import_image:
    if should_login:
        login(docker_cmd, docker_username, docker_password, docker_email, docker_server)
    build(docker_file, versioned_base_image, docker_cmd, base_image_name)

    if should_push:
        run_docker(docker_cmd + ["push", versioned_base_image])
        run_docker(docker_cmd + ["push", base_image_name + ":latest"])
else:
    if not imported:
        print "Compile image:", versioned_base_image, "into release"
        with open("imported_image", "w") as f:
            f.write(versioned_base_image)

outputs = escape.get_outputs()
outputs.set_output("image", versioned_base_image)
outputs.save()
