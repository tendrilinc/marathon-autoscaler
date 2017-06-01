#!/usr/bin/env python
"""
This script constructs an Marathon application definition for the Marathon Autoscaler container.

Be sure to deploy the latest Marathon Autoscaler docker image to the registry before running this.
"""
import argparse
import json
import os
import sys
import logging
logging.basicConfig(level=logging.CRITICAL)

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.dirname(BASE_PATH)
sys.path.append(os.path.join(PROJECT_PATH, 'lib/'))

from marathon_autoscaler.marathon import Marathon

MARATHON_URL = "http://192.168.99.100:8080"
REGISTRY_HOST = "192.168.99.100"
REGISTRY_PORT = "5000"
try:
    marathon = Marathon(os.environ.get("MINIMESOS_MARATHON", MARATHON_URL), (None, None))

    registry_tasks = marathon.get_app_tasks("registry")

    if registry_tasks and len(registry_tasks.get("tasks")) > 0:
        REGISTRY_HOST = registry_tasks.get("tasks")[0].get("host", REGISTRY_HOST)
        REGISTRY_PORT = registry_tasks.get("tasks")[0].get("ports", REGISTRY_PORT)[0]
except:
    pass

print("DOCKER_REGISTRY={}:{}".format(REGISTRY_HOST, REGISTRY_PORT))
