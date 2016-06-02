#!/usr/bin/env python
import argparse
import json
import sys
sys.path.append('../../marathon_autoscaler')
from marathon_autoscaler.marathon import Marathon

"""
This script constructs an Marathon application definition for the Marathon Autoscaler container.

Be sure to deploy the latest Marathon Autoscaler docker image to the registry before running this.
"""


def load_extension_file(file_path):
    with open(file_path, 'r') as f:
        scaler_extensions_data = json.load(f)
    return scaler_extensions_data


def parse_cli_args():
    parser = argparse.ArgumentParser(description="Deploy Marathon Autoscaler")
    parser.add_argument("--marathon-uri", dest="marathon_uri", type=str,
                        required=True, help="The Marathon Endpoint")
    parser.add_argument("--marathon-user", dest="marathon_user", type=str,
                        required=True, help="Username for Marathon access")
    parser.add_argument("--marathon-pass", dest="marathon_pass", type=str,
                        required=True, help="Password for Marathon access")
    parser.add_argument("--app", dest="marathon_app", type=str,
                        required=True, help="Password for Marathon access")
    parser.add_argument("--ext-file", dest="extensions_file", type=str,
                        required=True, help="Password for Marathon access")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_cli_args()
    scaler_extensions = load_extension_file(args.extensions_file)
    labels_data = {"labels": {}}
    labels_data["labels"]["marathon_autoscaler_extensions"] = \
        json.dumps(scaler_extensions).replace("\n", "").replace(" ", "")
    labels_data["labels"]["use_marathon_autoscaler"] = "True"

    mara = Marathon(args.marathon_uri, (args.marathon_user, args.marathon_pass))
    print(mara.update_app(args.marathon_app, labels_data))



