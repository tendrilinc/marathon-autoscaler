#!/usr/bin/env python
"""
This script constructs an Marathon application definition for the Marathon Autoscaler container.

Be sure to deploy the latest Marathon Autoscaler docker image to the registry before running this.
"""
import argparse
import json
import os
import sys

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.dirname(BASE_PATH)
sys.path.append(os.path.join(PROJECT_PATH, 'lib/'))

from marathon_autoscaler.marathon import Marathon


def load_app_definition():
    with open(os.path.join(os.getcwd(), "data", "marathon_autoscaler_app.json"), 'r') as f:
        test_app_definition = json.load(f)
    return test_app_definition


def parse_cli_args():
    p = argparse.ArgumentParser(description="Deploy Marathon Autoscaler")
    p.add_argument("--marathon-uri", dest="marathon_uri", type=str,
                   required=True, help="The Marathon Endpoint")
    p.add_argument("--marathon-user", dest="marathon_user", type=str,
                   required=False, help="Username for Marathon access")
    p.add_argument("--marathon-pass", dest="marathon_pass", type=str,
                   required=False, help="Password for Marathon access")
    p.add_argument("--interval", dest="sleep_interval", type=str,
                   required=True, help="The time duration in seconds between polling events")
    p.add_argument("--mesos-uri", dest="mesos_uri", type=str,
                   required=True, help="The Mesos Endpoint")
    p.add_argument("--log-verbosity", dest="log_verbosity", type=str,
                   required=True, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                   help="Logging verbosity")
    p.add_argument("--cpu-fan-out", dest="cpu_fan_out", type=str,
                   required=True,
                   help="The number of sub processes to fan out to when making parallel web calls")
    p.add_argument("--dd-api-key", dest="datadog_api_key", type=str,
                   required=True, help="Datadog API key")
    p.add_argument("--dd-app-key", dest="datadog_app_key", type=str,
                   required=True, help="Datadog APP key")
    p.add_argument("--dd-env", dest="datadog_env", type=str,
                   required=True, help="Datadog ENV variable")
    p.add_argument("--enforce-version-match", dest="enforce_version_match",
                   type=bool, default=False, required=False,
                   help="If set, version matching will be required of applications to participate")
    p.add_argument("--rules-prefix", dest="rules_prefix",
                   type=str, default="mas_rule", required=False,
                   help="The prefix for rule label names")

    return p.parse_args()


if __name__ == "__main__":
    args = parse_cli_args()

    app_def = load_app_definition()
    app_def["env"]["INTERVAL"] = args.sleep_interval
    app_def["env"]["MESOS_URI"] = args.mesos_uri
    app_def["env"]["MARATHON_URI"] = args.marathon_uri
    app_def["env"]["MARATHON_USER"] = args.marathon_user
    app_def["env"]["MARATHON_PASS"] = args.marathon_pass
    app_def["env"]["LOG_VERBOSITY"] = args.log_verbosity
    app_def["env"]["CPU_FAN_OUT"] = args.cpu_fan_out
    app_def["env"]["DATADOG_API_KEY"] = args.datadog_api_key
    app_def["env"]["DATADOG_APP_KEY"] = args.datadog_app_key
    app_def["env"]["DATADOG_ENV"] = args.datadog_env
    app_def["env"]["ENFORCE_VERSION_MATCH"] = args.enforce_version_match
    app_def["env"]["RULES_PREFIX"] = args.rules_prefix

    mara = Marathon(args.marathon_uri, (args.marathon_user, args.marathon_pass))
    response = mara.create_app(app_def)
    print(response)
