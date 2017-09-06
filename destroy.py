#!/usr/bin/env python

import sys
import json
import os
import subprocess

outputs_path = sys.argv[1]
outputs = json.load(open(outputs_path))

if os.path.exists("imported_image"):
    imported_image = open("imported_image").read()
    if imported_image != "":
        print "Skipping destroy on imported image", imported_image
        sys.exit(0)


if 'image' not in outputs:
    print "Missing 'image' output variable."
    sys.exit(1)

def run_docker(cmd):
    print "Running '%s'" % " ".join(cmd)
    sys.stdout.flush()
    try:
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError, e:
        print "Failed to run", cmd
        print e
        sys.exit(1)
    return output

image = outputs['image']
print "Removing Docker image '%s'" % image

env = os.environ
docker_cmd = json.loads(env['INPUT_docker_cmd'])

output = run_docker(docker_cmd + ["images", "-q", image]).strip()

if output == "":
    print "Image '%s' already removed" % image

parts = image.split(":")
latest = ":".join(parts[:-1]) + ":latest"
latest_out = run_docker(docker_cmd + ["images", "-q", latest]).strip()
is_latest = latest_out == output
run_docker(docker_cmd + ["rmi", image])
if is_latest:
    run_docker(docker_cmd + ["rmi", latest])
