import os
import sys
import json

import pytest


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib", "marathon-autoscaler"))

from application_definition import ApplicationDefinition
from rules_manager import RulesManager
import settings


@pytest.fixture
def testsettings():
    fake_settings = dict(sleep_interval=5,
                         mesos_uri=None,
                         agent_port=5051,
                         marathon_uri=None,
                         marathon_user=None,
                         marathon_pass=None,
                         cpu_fan_out=None,
                         datadog_api_key=None,
                         datadog_app_key=None,
                         datadog_env=None,
                         log_config="/app/logging_config.json",
                         enforce_version_match=False,
                         rules_prefix="mas_rule"
                         )
    for name, value in fake_settings.items():
        setattr(settings, name, value)


@pytest.fixture
def app_def():
    with open(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "simulation_data/app_definition.json"
            ), "r") as f:
        test_app_def = json.load(f)
    return test_app_def

@pytest.fixture
def rules_mgr(testsettings, app_def):
    _rules_mgr = RulesManager(app_def=ApplicationDefinition(app_def))
    assert (type(_rules_mgr) is RulesManager)
    return _rules_mgr


def test_is_app_participating(rules_mgr):
    assert (rules_mgr.is_app_participating() is True)


def test_is_app_ready(rules_mgr):
    assert (rules_mgr.is_app_ready() is True)


def test_has_rules(rules_mgr):
    assert (rules_mgr.rules is not None)


def test_is_app_within_min_or_max(rules_mgr):
    assert (rules_mgr.is_app_within_min_or_max() is True)


def test_has_rules(rules_mgr):
    assert (rules_mgr.rules is not None)


def test_triggering_scaledown_rules(rules_mgr):
    fake_metrics = dict(cpu=80, memory=80)
    triggered_rules = rules_mgr.trigger_rules(fake_metrics)
    for rule in triggered_rules:
        assert("slowscaledown" in rule.get("ruleInfo").get("ruleName"))


def test_triggering_fastscaleup_rules(rules_mgr):
    fake_metrics = dict(cpu=97, memory=89)
    triggered_rules = rules_mgr.trigger_rules(fake_metrics)
    for rule in triggered_rules:
        assert ("fastscaleup" in rule.get("ruleInfo").get("ruleName"))
