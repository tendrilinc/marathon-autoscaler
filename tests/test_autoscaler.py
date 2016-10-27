import os
import sys
import json

import pytest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib", "marathon-autoscaler"))
from scaler import AutoScaler
import settings


class fake_marathon_client():
    def scale_app(app_id, scale_size):
        return


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def auto_scaler():
    fake_client = fake_marathon_client()
    _autoscaler = AutoScaler(fake_client)
    assert (type(_autoscaler) is AutoScaler)
    return _autoscaler


@pytest.fixture(scope="session")
def metric_summaries():
    with open(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "simulation_data/app_metric_summaries.json"
            ), "r") as f:
        fake_data = json.load(f)
    assert(fake_data.get("summaries") is not None)
    return fake_data.get("summaries")


@pytest.fixture
def app_def():
    with open(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "simulation_data/app_definition.json"
            ), "r") as f:
        test_app_def = json.load(f)
    return test_app_def


def test_autoscale_decisions(testsettings, auto_scaler, app_def, metric_summaries):
    assert(type(app_def) is dict)
    for summary in metric_summaries:
        summary["test-service"]["application_definition"] = app_def
        auto_scaler.decide(summary)
    assert(type(auto_scaler) is AutoScaler)
