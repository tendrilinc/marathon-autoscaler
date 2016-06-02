import json
import logging

from apiclientbase import ApiClientBase


class MesosMaster(ApiClientBase):
    @staticmethod
    def load_paths():
        """
        :return:
        """
        return """
        {
            "/master/api/v1/scheduler": {"verb": "POST"},
            "/master/create-volumes": {"verb": "POST"},
            "/master/destroy-volumes": {"verb": "POST"},
            "/master/flags": {"verb": "GET"},
            "/master/frameworks": {"verb": "GET"},
            "/master/health": {"verb": "GET"},
            "/master/machine/down": {"verb": "POST"},
            "/master/machine/up": {"verb": "POST"},
            "/master/maintenance/schedule": {"verb": "GET"},
            "/master/maintenance/status": {"verb": "GET"},
            "/master/observe": {"verb": "POST"},
            "/master/quota": {"verb": "GET"},
            "/master/redirect": {"verb": "GET"},
            "/master/reserve": {"verb": "POST"},
            "/master/roles": {"verb": "GET"},
            "/master/slaves": {"verb": "GET"},
            "/master/state": {"verb": "GET"},
            "/master/state-summary": {"verb": "GET"},
            "/master/state": {"verb": "GET"},
            "/master/tasks": {"verb": "GET"},
            "/master/teardown": {"verb": "POST"},
            "/master/unreserve": {"verb": "POST"},
            "/monitor/statistics": {"verb": "GET"},
            "/metrics/snapshot": {"verb": "GET"},
            "/system/stats": {"verb": "GET"},
            "/version": {"verb": "GET"}
        }
        """

    def __init__(self, uri, creds=None, logger=None):
        """
        :param uri:
        :param creds:
        :return:
        """
        super(MesosMaster, self).__init__(uri, creds)
        self.paths = json.loads(self.load_paths())
        self.logger = logger or logging.getLogger(__name__)

    def find_master(self):
        self.uri = self._call_endpoint("/master/redirect").url

    def get_health(self):
        """
        :return:
        """
        self.find_master()
        return self._call_endpoint("/master/health")

    def get_slaves(self):
        """
        :return:
        """
        self.find_master()
        return self._call_endpoint("/master/slaves")

    def get_state(self):
        """
        :return:
        """
        self.find_master()
        return self._call_endpoint("/master/state")

    def get_tasks(self):
        """
        :return:
        """
        self.find_master()
        return self._call_endpoint("/master/tasks")

    def get_statistics(self):
        """
        :return:
        """
        self.find_master()
        return self._call_endpoint("/monitor/statistics")

    def get_system_stats(self):
        """
        :return:
        """
        self.find_master()
        return self._call_endpoint("/system/stats")

    def get_metrics(self):
        """
        :return:
        """
        self.find_master()
        return self._call_endpoint("/metrics/snapshot")

    def get_version(self):
        """
        :return:
        """
        self.find_master()
        return self._call_endpoint("/version")
