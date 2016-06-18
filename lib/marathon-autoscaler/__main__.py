import argparse
import json
import logging
import logging.config
import os
import pkg_resources
import sys
from poller import Poller
import settings


def setup_logging(cli_args):
    """ Setup logging configuration
    :param cli_args: Argparse object containing parameters from the command line
    :return: Logger
    """
    logconfig_path = cli_args.log_config
    if not os.path.isabs(logconfig_path):
        resource_package = __name__
        logconfig_io = pkg_resources.resource_stream(resource_package, logconfig_path)
        logconfig_string = logconfig_io.getvalue().decode(encoding="utf-8")
        config = json.loads(logconfig_string)
    else:
        with open(logconfig_path, 'rt') as f:
            config = json.load(f)
    logging.config.dictConfig(config)


class EnvDefault(argparse.Action):
    """
    A custom argparse class to handle the consumption of environment variables in
    addition to commandline parameters.
    """
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def parse_cli_args():
    """
    A method for organizing all commandline argument and environment variable parsing.
    :return: An argparse object containing all CLI/ENV argument values.
    """
    p = argparse.ArgumentParser(description="Marathon Autoscaler")
    p.add_argument("-i", "--interval", dest="sleep_interval", action=EnvDefault, envvar="INTERVAL", type=int,
                   default=5, help="The time duration in seconds between polling events")
    p.add_argument("--mesos-uri", dest="mesos_uri", action=EnvDefault, envvar="MESOS_URI", type=str, required=True,
                   help="The Mesos Endpoint")
    p.add_argument("--mesos-agent-port", dest="mesos_agent_port", action=EnvDefault, envvar="MESOS_AGENT_PORT", type=int,
                   required=True, default=5051, help="Mesos Agent Port")
    p.add_argument("--marathon-uri", dest="marathon_uri", action=EnvDefault, envvar="MARATHON_URI", type=str,
                   required=True, help="The Marathon Endpoint")
    p.add_argument("--marathon-user", dest="marathon_user", action=EnvDefault, envvar="MARATHON_USER", type=str,
                   required=True, help="The Marathon Username")
    p.add_argument("--marathon-pass", dest="marathon_pass", action=EnvDefault, envvar="MARATHON_PASS", type=str,
                   required=True, help="The Marathon Password")
    p.add_argument("--cpu-fan-out", dest="cpu_fan_out", action=EnvDefault, envvar="CPU_FAN_OUT", type=int,
                   default=None, required=False, help="Number of subprocesses to use for gathering and sending stats to Datadog")
    p.add_argument("--dd-api-key", dest="datadog_api_key", action=EnvDefault, envvar="DATADOG_API_KEY", type=str,
                   required=False, help="Datadog API key")
    p.add_argument("--dd-app-key", dest="datadog_app_key", action=EnvDefault, envvar="DATADOG_APP_KEY", type=str,
                   required=False, help="Datadog APP key")
    p.add_argument("--dd-env", dest="datadog_env", action=EnvDefault, envvar="DATADOG_ENV", type=str,
                   required=False, help="Datadog ENV variable")
    p.add_argument("--log-config", dest="log_config", action=EnvDefault, envvar="LOG_CONFIG", type=str,
                   default="/app/logging_config.json",
                   help="Path to logging configuration file")
    p.add_argument("--enforce-version-match", dest="enforce_version_match", action=EnvDefault,
                   envvar="ENFORCE_VERSION_MATCH", type=bool, default=False,
                   required=False, help="If set, version matching will be required of applications to participate")
    p.add_argument("--rules-prefix", dest="rules_prefix", action=EnvDefault,
                   envvar="RULES_PREFIX", type=str, default="mas_rule",
                   required=False, help="The prefix for rule names")
    return p.parse_args()


def add_args_to_settings(cli_args):
    for name, value in vars(cli_args).iteritems():
        setattr(settings, name, value)

if __name__ == "__main__":
    args = parse_cli_args()
    add_args_to_settings(args)
    setup_logging(args)
    logging.info(args)
    poller = Poller(args)
    poller.start()
    sys.exit(0)
