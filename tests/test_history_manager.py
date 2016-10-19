import os
import sys
import json

import pytest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib", "marathon-autoscaler"))
from history_manager import HistoryManager
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
def history_mgr(testsettings):
    _history_mgr = HistoryManager()
    assert (type(_history_mgr) is HistoryManager)
    return _history_mgr
