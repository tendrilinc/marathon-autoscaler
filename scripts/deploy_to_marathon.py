#!/usr/bin/env python
"""

"""
import requests
from requests.auth import HTTPBasicAuth
import argparse
import json
import logging
import os
import sys
import traceback

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
LOG.addHandler(ch)


def main(main_args):
    """
    Read environment variables to envvars_dict
    Open file with file_path
    Read contents as template_contents
    Render template_contents as rendered_file_contents with envvars_dict
    Send rendered_file_contents to file or stdout
    """
    appdef_contents = read_file_contents(main_args.appdef_file)
    send_to_marathon(appdef_contents, main_args)


def parse_cli_args():
    p = argparse.ArgumentParser(description="Deploy To Marathon")
    p.add_argument("appdef_file",
                   type=str,
                   help="Path to application definition file")
    p.add_argument("--marathon-uri", dest="marathon_uri", type=str,
                   required=True, help="The Marathon Endpoint")
    p.add_argument("--marathon-user", dest="marathon_user", type=str,
                   required=False, help="Username for Marathon access")
    p.add_argument("--marathon-pass", dest="marathon_pass", type=str,
                   required=False, help="Password for Marathon access")

    return p.parse_known_args()


def read_file_contents(file_path):
    contents = None
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            contents = f.read()
    return contents


def send_to_marathon(app_def_contents, cli_args):
    app_def_obj = json.loads(app_def_contents)
    request_args = ["{}/v2/apps/{}".format(
        cli_args.marathon_uri,
        app_def_obj.get("id"))]
    request_kwargs = dict(data=json.dumps(app_def_obj))

    if cli_args.marathon_user:
        request_kwargs.update(auth=HTTPBasicAuth(cli_args.marathon_user, cli_args.marathon_pass))

    response = requests.put(*request_args, **request_kwargs)

    LOG.info(response.headers)
    LOG.info(response.status_code)
    LOG.info(response.content)


if __name__ == "__main__":
    try:
        args, args_other = parse_cli_args()
        main(args)
    except Exception as main_ex:
        LOG.error("An error occurred in running the application!")
        LOG.error(main_ex)
        LOG.error(traceback.print_tb(sys.exc_info()[2]))
    finally:
        sys.exit(0)
