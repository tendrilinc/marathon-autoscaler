#!/usr/bin/env python
import argparse
import jinja2
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
    envvars_dict = dict(os.environ)
    template_contents = read_file_contents(main_args.template_file)
    rendered_file_contents = render_template(template_contents, envvars_dict)
    if main_args.output_file:
        sys.stdout = open(main_args.output_file, "w")
    sys.stdout.write(rendered_file_contents)
    sys.stdout.close()


def parse_cli_args():
    p = argparse.ArgumentParser(description="Template Renderer")

    p.add_argument("template_file",
                   type=str,
                   help="Path to template file")
    p.add_argument("-o", "--output",
                   dest="output_file",
                   type=str,
                   required=False,
                   help="Path to output file")
    return p.parse_known_args()


def read_file_contents(file_path):
    contents = None
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            contents = f.read()
    return contents


def render_template(template_contents, parameters_dict):
    template = jinja2.Template(template_contents)
    rendered_contents = template.render(**parameters_dict)
    return rendered_contents


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
