"""Datadog functions for autoscaler"""
import logging
from datadog import initialize, api


class DatadogClient:

    def __init__(self, cli_args, logger=None):
        if cli_args.datadog_api_key and cli_args.datadog_app_key:
            self.dd_auth = dict(api_key=cli_args.datadog_api_key,
                                app_key=cli_args.datadog_app_key)
            self.dd_env = cli_args.datadog_env
            self.cpu_fan_out = cli_args.cpu_fan_out
            self.logger = logger or logging.getLogger(__name__)
            self.enabled = True
            initialize(**self.dd_auth)
        else:
            self.enabled = False

    def send_datadog_metrics(self, stats):
        """ Enumerates metrics from stats object to send to Datadog
        :param stats: a complex dictionary of marathon application metrics information
        :return: None
        """
        try:
            if self.enabled:
                metrics = []
                for app, items in stats.items():
                    tags = ["env:{}".format(self.dd_env),
                            "app:{}".format(app)]

                    # Avg CPU for entire app
                    metrics.append(dict(metric='marathon.app.cpu_avg',
                                        points=items['cpu_avg_usage'],
                                        host='n/a',
                                        tags=tags))

                    # Avg mem for entire app
                    metrics.append(dict(metric='marathon.app.mem_avg',
                                        points=items['memory_avg_usage'],
                                        host='n/a',
                                        tags=tags))

                    tags = ["env:{}".format(self.dd_env),
                            "app:{}".format(app),
                            "executor:{}".format(items['max_cpu'][1])]

                    # Max CPU for entire app
                    metrics.append(dict(metric='marathon.app.cpu_max',
                                        points=items['max_cpu'][0],
                                        host='n/a',
                                        tags=tags))

                    # Max mem for entire app
                    tags = ["env:{}".format(self.dd_env),
                            "app:{}".format(app),
                            "executor:{}".format(items['max_memory'][1])]

                    metrics.append(dict(metric='marathon.app.mem_max',
                                        points=items['max_memory'][0],
                                        host='n/a',
                                        tags=tags))

                    # Per-executor metrics
                    for item in items['executor_metrics']:
                        tags = ["env:{}".format(self.dd_env),
                                "app:{}".format(app),
                                "executor:{}".format(item['executor_id'])]

                        metrics.append(dict(metric='marathon.executor.cpu',
                                            points=item['cpu_total_usage'],
                                            host=item['host'],
                                            tags=tags))
                        metrics.append(dict(metric='marathon.executor.mem',
                                            points=item['memory_total_usage'],
                                            host=item['host'],
                                            tags=tags))

                api.Metric.send(metrics=metrics)
        except Exception as err:
            self.logger.error(err)

    def send_counter_event(self, app, metric, points=None, tags=None, **kwargs):
        """
        marathon_autoscaler.counters.min_instances [tags- app:{app_name} env:{env}]
        marathon_autoscaler.counters.max_instances [tags- app:{app_name} env:{env}]
        marathon_autoscaler.counters.current_instances [tags- app:{app_name} env:{env}]
        :param app: the marathon application name
        :param metric: the metric name
        :param points: the metric value(s)
        :param tags: datadog tags for categorization
        :param kwargs: kwargs for additional future input
        :return: None
        """
        if self.enabled:
            all_tags = ["env:{}".format(self.dd_env), "app:{}".format(app)]

            if tags:
                all_tags = tags + all_tags

            try:
                api.Metric.send(metric=metric,
                                points=points if points else 1,
                                tags=all_tags,
                                type='counter')
            except Exception as err:
                self.logger.error(err)

    def send_scale_event(self, app, factor, direction, tags=None):
        """
        marathon_autoscaler.events.scale_up [tags- app:{app_name} env:{env}]
        marathon_autoscaler.events.scale_down [tags- app:{app_name} env:{env}]
        :param app: the marathon application name
        :param factor: the scaling factor
        :param direction: the scaling direction
        :param tags: datadog tags for categorization
        :return: None
        """
        if self.enabled:
            all_tags = ["env:{}".format(self.dd_env), "app:{}".format(app)]

            if tags:
                all_tags = tags + all_tags
            metrics = {
                        1: "marathon_autoscaler.events.scale_up",
                        -1: "marathon_autoscaler.events.scale_down",
                        0: "marathon_autoscaler.events.idle"
                      }
            try:
                api.Metric.send(metric=metrics[direction],
                                points=factor,
                                tags=all_tags,
                                type='counter')
            except Exception as err:
                self.logger.error(err)
