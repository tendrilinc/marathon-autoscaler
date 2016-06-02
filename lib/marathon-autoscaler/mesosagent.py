import json
import logging

from apiclientbase import ApiClientBase


class MesosAgent(ApiClientBase):
    @staticmethod
    def load_paths():
        """
        :return:
        """
        return """
        {
            "/monitor/statistics": {"verb": "GET"},
            "/metrics/snapshot": {"verb": "GET"},
            "/api/v1/executor": {"verb": "GET"},
            "/flags": {"verb": "GET"},
            "/health": {"verb": "GET"},
            "/state": {"verb": "GET"},
            "/system/stats": {"verb": "GET"},
            "/version": {"verb": "GET"},
            "/{slave_id}/api/v1/executor": {"verb": "GET"},
            "/{slave_id}/flags": {"verb": "GET"},
            "/{slave_id}/health": {"verb": "GET"},
            "/{slave_id}/state": {"verb": "GET"},
            "/{slave_id}/state.json": {"verb": "GET"}
        }
        """

    def get_statistics(self):
        """
        :return:
        """
        return self._call_endpoint("/monitor/statistics")

    def get_metrics(self):
        """
        :return:
        """
        return self._call_endpoint("/metrics/snapshot")

    def get_health(self):
        """
        :return:
        """
        return self._call_endpoint("/health")

    def get_state(self):
        """
        :return:
        """
        return self._call_endpoint("/state")

    def get_executor(self):
        """
        :return:
        """
        return self._call_endpoint("/api/v1/executor")

    def get_flags(self):
        """
        :return:
        """
        return self._call_endpoint("/flags")

    def get_slave_health(self, slave_id):
        """
        :param slave_id:
        :return:
        """
        return self._call_endpoint("/{slave_id}/health", slave_id=slave_id)

    def get_slave_state(self, slave_id):
        """
        :param slave_id:
        :return:
        """
        return self._call_endpoint("/{slave_id}/state", slave_id=slave_id)

    def get_slave_executor(self, slave_id):
        """
        :param slave_id:
        :return:
        """
        return self._call_endpoint("/{slave_id}/api/v1/executor", slave_id=slave_id)

    def get_slave_flags(self, slave_id):
        """
        :param slave_id:
        :return:
        """
        return self._call_endpoint("/{slave_id}/flags", slave_id=slave_id)

    def get_system_stats(self):
        """
        :return:
        """
        return self._call_endpoint("/system/stats")

    def __init__(self, uri, creds=None, logger=None):
        """
        :param uri:
        :param creds:
        :return:
        """
        super(MesosAgent, self).__init__(uri, creds)
        self.paths = json.loads(self.load_paths())
        self.logger = logger or logging.getLogger(__name__)
