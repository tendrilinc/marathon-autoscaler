#!/usr/bin/env python

from collections import defaultdict
from application_definition import ApplicationDefinition
import logging
from datadog_metrics import DatadogClient
from marathon import Marathon
from mesosagent import MesosAgent
from mesosmaster import MesosMaster
from scaler import AutoScaler
from multiprocessing import Pool
from time import sleep
import settings

def get_mesos_agent_statistics(agent_host):
    """
    :param agent_host: A Mesos slave endpoint defined as an FQDN or IP Address
    :return: Statistics (Metrics) JSON
    """
    return agent_host, MesosAgent("http://{0}:{1}/".format(agent_host, settings.agent_port)).get_statistics()


class Poller:
    """
    A polling mechanism for gathering metrics data for the Autoscaler's decision engine.
    """

    def __init__(self, cli_args, logger=None):
        self.args = cli_args
        self.logger = logger or logging.getLogger(__name__)
        self.mesos = MesosMaster(cli_args.mesos_uri)
        self.marathon = Marathon(cli_args.marathon_uri,
            (cli_args.marathon_user, cli_args.marathon_pass)
            if cli_args.marathon_user and cli_args.marathon_pass
            else None
        )
        self.auto_scaler = AutoScaler(self.marathon, cli_args=cli_args)
        self.cpu_fan_out = cli_args.cpu_fan_out
        self.datadog_client = DatadogClient(cli_args)
        self.agent_port = cli_args.agent_port

    def poll(self, mesos_master, marathon_client, poll_time_span=3, cpu_fan_out=None):
        """ The main method for forming the applications metrics data object. A call to Marathon retrieves
        all applications, a call to Mesos Master retrieves all slaves, each slave node is queried for its
        statistics (metrics) twice (to acquire a differential), differentials are calculated, additional
        metrics are added (max_cpu, max_mem). All of this data is collected in a single dictionary object
        and returned to caller.
        :param mesos_master: A Mesos Master Client
        :param marathon_client: A Marathon Client
        :param poll_time_span: Time (in seconds) between polling events
        :param cpu_fan_out: Max number of processes in MP Pools
        :return: A dictionary object containing all Application metric data for 2 consecutive polls
        """
        try:
            marathon_apps = marathon_client.get_all_apps().get("apps")
            slaves = mesos_master.get_slaves()
            agent_hosts = [slave.get("hostname") for slave in slaves.get("slaves")]
        except Exception as ex:
            self.logger.error(ex)
            self.logger.fatal("Marathon data could not be retrieved!")
            return

        executor_stats = defaultdict(list)

        for _ in range(2):
            agent_hosts_stats = {}
            if cpu_fan_out:
                fan_out_procs = cpu_fan_out
            else:
                fan_out_procs = len(agent_hosts)

            maxtasks = int(len(agent_hosts) / fan_out_procs) if int(len(agent_hosts) / fan_out_procs) else 1
            pool = Pool(processes=fan_out_procs, maxtasksperchild=maxtasks)
            for agent_host, stats in pool.imap_unordered(get_mesos_agent_statistics, agent_hosts):
                self.logger.debug((agent_host, stats))
                agent_hosts_stats[agent_host] = stats
            pool.close()

            for host in agent_hosts_stats:
                if agent_hosts_stats[host] is not None:
                    for executor in agent_hosts_stats[host]:
                        data = {"host": host, "stats": executor["statistics"]}
                        executor_stats[executor["executor_id"]].append(data)
            sleep(poll_time_span)

        self.logger.info("Stats differentials collected.")
        all_diffs = {}

        for key, stat in executor_stats.items():

            if len(stat) != 2:
                continue

            host = stat[0].get("host")
            first_stats = stat[0].get("stats")
            second_stats = stat[1].get("stats")

            if "timestamp" in second_stats and "timestamp" in first_stats:
                sys_cpu_delta = second_stats["cpus_system_time_secs"] - \
                                first_stats["cpus_system_time_secs"]

                user_cpu_delta = second_stats["cpus_user_time_secs"] - first_stats["cpus_user_time_secs"]
                timestamp_delta = second_stats["timestamp"] - first_stats["timestamp"]
                mem_total = first_stats["mem_limit_bytes"]
                mem_used = second_stats["mem_rss_bytes"]
                cpu_total_usage = ((sys_cpu_delta + user_cpu_delta) / timestamp_delta) * 100
                memory_total_usage = (float(mem_used) / mem_total) * 100

                diffs = dict(timestamp=timestamp_delta,
                             cpus_system_time_secs=sys_cpu_delta,
                             cpus_user_time_secs=user_cpu_delta,
                             cpu_total_usage=cpu_total_usage,
                             memory_total_usage=memory_total_usage,
                             host=host,
                             executor_id=key)
                all_diffs[key] = diffs
            else:
                self.logger.error("Timestamps were not found in stats from host: {0}".format(host))

        app_metric_map = defaultdict(list)

        for key in all_diffs.keys():
            app_metric_map[key.split(".")[0]].append(all_diffs[key])

        app_metric_summation = {}

        for app, metrics in app_metric_map.items():

            metric_sums = {}

            cpu_values = [metric["cpu_total_usage"] for metric in metrics]
            metric_sums["cpu_avg_usage"] = sum(cpu_values) / len(cpu_values)

            metric_sums["max_cpu"] = max([(metric["cpu_total_usage"],
                                           metric["executor_id"],
                                           metric["host"]) for metric in metrics])

            memory_values = [metric["memory_total_usage"] for metric in metrics]
            metric_sums["memory_avg_usage"] = sum(memory_values) / len(memory_values)

            metric_sums["max_memory"] = max([(metric["memory_total_usage"],
                                              metric["executor_id"],
                                              metric["host"]) for metric in metrics])

            metric_sums["executor_metrics"] = metrics
            metric_sums["application_definition"] = next((appdef for appdef in marathon_apps
                                                          if app.replace("_", "/") == appdef.get("id")), {})
            app_metric_summation[app] = metric_sums

        return app_metric_summation

    def start(self):
        """
        This is the entry method for the Poller class.
        :return: None
        """
        self.logger.info("Mesos and Marathon Connections Established.")
        while True:
            polled_stats = self.poll(self.mesos, self.marathon, cpu_fan_out=self.cpu_fan_out)

            if polled_stats is not None:
                self.datadog_client.send_datadog_metrics(polled_stats)
                self.auto_scaler.decide(polled_stats)
                self.update_autoscaler_metrics(polled_stats)
                self.logger.info("Decisions are completed.")
            else:
                self.logger.fatal("Poller unable to reach Marathon/Mesos!")

            sleep(self.args.sleep_interval)

    def update_autoscaler_metrics(self, stats):
        """
        * Number of participating applications
        * Total min instances
        * Total max instances
        * Total number of currently running instances (only participating applications)
        * Number of currently running instances per application
        * Number of scale up events
        * Number of scale down events
        * Number of flap detection events
        :param stats: dict object containing all application metric information specific to this polling event
        :return:
        """
        participating_applications = [{"app": app,
                                       "current_instances": int(items["application_definition"]["instances"]),
                                       "min_instances": int(items["application_definition"]["labels"]["min_instances"]),
                                       "max_instances": int(items["application_definition"]["labels"]["max_instances"])}
                                      for app, items in stats.items()
                                      if ApplicationDefinition(items["application_definition"]).is_app_participating]

        # total_participating_applications = len(participating_applications)
        # total_min_instances = sum([app["min_instances"] for app in participating_applications])
        # total_max_instances = sum([app["max_instances"] for app in participating_applications])
        # total_current_instances = sum([app["current_instances"] for app in participating_applications])

        [self.datadog_client.send_counter_event(app["app"],
                                                "marathon_autoscaler.counters.min_instances",
                                                points=app["min_instances"])
         for app in participating_applications]
        [self.datadog_client.send_counter_event(app["app"],
                                                "marathon_autoscaler.counters.max_instances",
                                                points=app["max_instances"])
         for app in participating_applications]
        [self.datadog_client.send_counter_event(app["app"],
                                                "marathon_autoscaler.counters.current_instances",
                                                points=app["current_instances"])
         for app in participating_applications]
