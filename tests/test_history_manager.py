import os
import sys
import json
import dateutil.parser
from datetime import timedelta, datetime
import pytest
import logging

logging.basicConfig(level=logging.DEBUG)

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib", "marathon_autoscaler"))
from history_manager import HistoryManager
import settings

rightnow = datetime.now()

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
def history_mgr(testsettings):
    _history_mgr = HistoryManager()
    assert (type(_history_mgr) is HistoryManager)
    return _history_mgr


def datetime_parser(obj):
    for k, v in obj.items():
        if "timestamp" in k:
            try:
                obj[k] = rightnow
            except ValueError as ve:
                pass
    return obj

_counter = 1


def _decrement_time(date_time, time_span):
    new_date_time = date_time - timedelta(seconds=time_span * _counter)
    global _counter
    _counter += 1
    return new_date_time


@pytest.fixture(scope="session")
def app_recommendations():
    with open(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "simulation_data/app_recommendations.json"
            ), "r") as f:
        test_app_recommendations = json.load(f, object_hook=datetime_parser)
    return test_app_recommendations.get("recommendationsList")


def test_add_to_perf_tail(history_mgr, app_recommendations):
    for recommendation in app_recommendations:
        history_mgr.add_to_perf_tail(recommendation)
    assert len(history_mgr.app_performance_tail) > 1


def test_tolerance_reached(history_mgr):
    [event.update({"timestamp": _decrement_time(event.get("timestamp"), 6)})
     for recommendation in history_mgr.app_performance_tail
     for app, event in recommendation.items()]

    assert history_mgr.tolerance_reached("test-service", "PT10S", 1)


def test_within_backoff(history_mgr):
    assert not history_mgr.within_backoff("test-service", "PT2M", 1)


def test_is_time_window_filled(history_mgr):
    rightnow = datetime.now()
    assert history_mgr.is_time_window_filled("test-service", rightnow - timedelta(seconds=10))


def test_get_timedelta(history_mgr):
    timespan_obj = history_mgr.get_timedelta("PT3M34S")
    assert timespan_obj.seconds == 214
