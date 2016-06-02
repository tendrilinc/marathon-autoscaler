from datetime import datetime
from constants import IDLE
import logging
from utils import clamp
from rules_manager import RulesManager
from history_manager import HistoryManager
from application_definition import ApplicationDefinition


class AutoScaler(object):
    """
    The source of the scaling decision.
    """
    def __init__(self, marathon_client, logger=None, dd_client=None, cli_args=None):
        self.marathon_client = marathon_client
        self.logger = logger or logging.getLogger(__name__)
        self.dd_client = dd_client
        self.enforce_version_match = False
        self.hm = HistoryManager(dd_client=dd_client)
        if cli_args is not None:
            self.enforce_version_match = cli_args.enforce_version_match

    def scale(self, app_def, rule_manager):
        """ Take scale action
        :param app_def: dict of marathon application settings
        :param rule_manager: object of scaling properties.
        :return: marathon response
        """
        if not app_def.is_app_participating:
            return

        scale_factor = int(rule_manager.last_triggered_criteria.get("scale_factor"))
        min_instances = int(rule_manager.min_instances)
        max_instances = int(rule_manager.max_instances)

        scale_to = app_def.instances + scale_factor
        scale_to_size = clamp(scale_to, min_instances, max_instances)

        if app_def.instances == scale_to_size:
            msg = "{app_name}: application already scaled to {size}"
            self.logger.info(msg.format(app_name=app_def.app_name,
                                        size=scale_to_size))
            return

        self.marathon_client.scale_app(app_def.id, scale_to_size)
        msg = "{app_name}: scaled to {size}"
        self.logger.info(msg.format(app_name=app_def.app_name,
                                    size=scale_to_size))

    def decide(self, app_metrics_summary):
        """
        The decision-maker of the autoscaler.
        :param app_metrics_summary: dict of app definitions and metrics
        :return: None
        """
        self.logger.info("Decision process beginning.")

        app_scale_recommendations = {}
        for app, metrics_summary in app_metrics_summary.items():
            app_def = ApplicationDefinition(metrics_summary.get("application_definition"))
            rm = RulesManager(app_def)
            if rm.is_app_participating():
                vote = 0
                scale_factor = 0
                cpu = metrics_summary.get("cpu_avg_usage")
                mem = metrics_summary.get("memory_avg_usage")
                metrics = dict(cpu=cpu,
                               mem=mem)

                rm.trigger_rules(metrics)

                if rm.last_triggered_criteria:
                    scale_factor = int(rm.last_triggered_criteria.get("scale_factor"))
                    vote = 1 if scale_factor > 0 else -1

                app_scale_recommendations[app] = dict(vote=vote,
                                                      checksum=app_def.version,
                                                      timestamp=datetime.now(),
                                                      rule=rm.last_triggered_rule)
                info_msg = "{app_name}: vote: {vote} ; scale_factor requested: {scale_factor}"
                self.logger.info(info_msg.format(app_name=app_def.app_name,
                                                 vote=vote,
                                                 scale_factor=scale_factor))
                # Check if app is participating
                # Check if app is ready
                # Check if app instances is greater than or equal to min and less than max

                if (rm.is_app_ready() and
                        rm.is_app_within_min_or_max() and
                        rm.last_triggered_criteria):
                    tolerance_reached = self.hm.tolerance_reached(app,
                                                                  rm.last_triggered_criteria.get("tolerance"),
                                                                  vote)
                    within_backoff = self.hm.within_backoff(app,
                                                            rm.last_triggered_criteria.get("backoff"),
                                                            vote)

                    if vote is not IDLE and tolerance_reached and not within_backoff:
                        self.logger.info("{app}: Decision made: Scale.".format(app=app_def.app_name))
                        app_scale_recommendations[app]["decision"] = vote
                        self.scale(app_def, rm)
                    elif vote == IDLE:
                        app_scale_recommendations[app]["decision"] = IDLE
                        self.logger.info("{app}: Decision made: No Change.".format(app=app_def.app_name))

        self.hm.add_to_perf_tail(app_scale_recommendations)
