#!/usr/bin/env python
"""
This script constructs an Marathon application definition for the stress tester container.

Be sure to deploy the latest stress tester docker image to the registry before running this.
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
    with open(os.path.join(os.getcwd(), "data", "stress_tester_app.json"), 'r') as f:
        test_app_definition = json.load(f)
    return test_app_definition


def load_stress_parameters():
    with open(os.path.join(os.getcwd(), "data", "stress-parameters.json"), 'r') as f:
        test_app_definition = json.load(f)
    return test_app_definition


def load_autoscaler_parameters():
    with open(os.path.join(os.getcwd(), "data", "autoscaler-parameters.json"), 'r') as f:
        test_app_definition = json.load(f)
    return test_app_definition


def parse_cli_args():
    parser = argparse.ArgumentParser(description="Stress Tester Deployer")
    parser.add_argument("--marathon-uri", dest="marathon_uri", type=str,
                        required=True, help="The Marathon Endpoint")
    parser.add_argument("--marathon-user", dest="marathon_user", type=str,
                        required=True, help="Username for Marathon access")
    parser.add_argument("--marathon-pass", dest="marathon_pass", type=str,
                        required=True, help="Password for Marathon access")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_cli_args()
    app_def = load_app_definition()

    mara = Marathon(args.marathon_uri, (args.marathon_user, args.marathon_pass))

    stress_params = load_stress_parameters()
    autoscaler_params = load_autoscaler_parameters()
    print("""
    Stress Parameters:
    {0}

    """.format(stress_params))

    print("""
    Scaling Parameters:
    {0}

    """.format(autoscaler_params))
    app_def["labels"]["use_marathon_autoscaler"] = "0.0.3"
    app_def["labels"]["min_instances"] = str(autoscaler_params["min_instances"])
    app_def["labels"]["max_instances"] = str(autoscaler_params["max_instances"])
    # app_def["labels"]["upper_cpu_avg_usage"] = str(autoscaler_params["upper_threshold"]["cpu_avg_usage"])
    # app_def["labels"]["upper_memory_avg_usage"] = str(autoscaler_params["upper_threshold"]["memory_avg_usage"])
    # app_def["labels"]["upper_scale_factor"] = str(autoscaler_params["upper_threshold"]["scale_factor"])
    # app_def["labels"]["upper_tolerance"] = str(autoscaler_params["upper_threshold"]["tolerance"])
    # app_def["labels"]["upper_backoff"] = str(autoscaler_params["upper_threshold"]["backoff"])
    # app_def["labels"]["upper_exclusive"] = str(autoscaler_params["upper_threshold"]["exclusive"])
    # app_def["labels"]["lower_cpu_avg_usage"] = str(autoscaler_params["lower_threshold"]["cpu_avg_usage"])
    # app_def["labels"]["lower_memory_avg_usage"] = str(autoscaler_params["lower_threshold"]["memory_avg_usage"])
    # app_def["labels"]["lower_scale_factor"] = str(autoscaler_params["lower_threshold"]["scale_factor"])
    # app_def["labels"]["lower_tolerance"] = str(autoscaler_params["lower_threshold"]["tolerance"])
    # app_def["labels"]["lower_backoff"] = str(autoscaler_params["lower_threshold"]["backoff"])
    # app_def["labels"]["lower_exclusive"] = str(autoscaler_params["lower_threshold"]["exclusive"])
    app_def["labels"]["mas_rule_scaleup_1"] = "cpu | >90 | PT2M | 1 | PT2M"
    app_def["labels"]["mas_rule_scaleup_2"] = "mem | >90 | PT2M | 1 | PT2M"
    app_def["labels"]["mas_rule_scaledown"] = "cpu | <90 | PT2M | -1 | PT2M"

    app_def["env"]["INSTRUCTIONS"] = json.dumps(stress_params).replace("\n", "").replace(" ", "")

    response = mara.create_app(app_def)
    print(response)
