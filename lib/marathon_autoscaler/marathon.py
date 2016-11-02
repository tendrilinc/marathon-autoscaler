import json
import logging

from apiclientbase import ApiClientBase


class Marathon(ApiClientBase):
    @staticmethod
    def load_paths():
        """
        :return:
        """
        return """
        {
            "/v2/apps": {"verb": "GET"},
            "/v2/apps/{appId}": {"verb": "GET"},
            "/v2/apps/{appId}/versions": {"verb": "GET"},
            "/v2/apps/{appId}/versions/{versionId}": {"verb": "GET"},
            "/v2/apps/{appId}/tasks": {"verb": "GET"},
            "/v2/groups": {"verb": "GET"},
            "/v2/groups/{groupId}": {"verb": "GET"},
            "/v2/tasks": {"verb": "GET"},
            "/v2/deployments": {"verb": "GET"},
            "/v2/events": {"verb": "GET"},
            "/v2/eventSubscriptions": {"verb": "GET"},
            "/v2/queue": {"verb": "GET"},
            "/v2/info": {"verb": "GET"},
            "/v2/leader": {"verb": "GET"},
            "/ping": {"verb": "GET"},
            "/logging": {"verb": "GET"},
            "/help": {"verb": "GET"},
            "/metrics": {"verb": "GET"}
        }
        """

    def __init__(self, uri, creds=None, logger=None):
        """
        :param uri:
        :param creds:
        :return:
        """
        super(Marathon, self).__init__(uri, creds)
        self.paths = json.loads(self.load_paths())
        self.logger = logger or logging.getLogger(__name__)

    def get_all_apps(self):
        """
        :return:
        """
        return self._call_endpoint("/v2/apps")

    def get_all_app_names(self):
        """
        :return:
        """
        return [app.get("id").lstrip("/") for app in self.get_all_apps().get("apps")]

    def get_app_details(self, marathon_app):
        """
        :param marathon_app:
        :return:
        """
        return self._call_endpoint("/v2/apps/{appId}", appId=marathon_app)

    def get_app_tasks(self, marathon_app):
        """
        :param marathon_app:
        :return:
        """
        return self._call_endpoint("/v2/apps/{appId}/tasks", appId=marathon_app)

    def get_all_groups(self):
        """
        :return:
        """
        return self._call_endpoint("/v2/groups")

    def get_group(self, group):
        """
        :param group:
        :return:
        """
        return self._call_endpoint("/v2/groups/{groupId}", groupId=group)

    def get_info(self):
        """
        :return:
        """
        return self._call_endpoint("/v2/info")

    def get_tasks(self):
        """
        :return:
        """
        return self._call_endpoint("/v2/tasks")

    def get_deployments(self):
        """
        :return:
        """
        return self._call_endpoint("/v2/deployments")

    def get_events(self):
        """
        :return:
        """
        return self._call_endpoint("/v2/events")

    def get_event_subscriptions(self):
        """
        :return:
        """
        return self._call_endpoint("/v2/eventSubscriptions")

    def get_queue(self):
        """
        :return:
        """
        return self._call_endpoint("/v2/queue")

    def get_leader(self):
        """
        :return:
        """
        return self._call_endpoint("/v2/leader")

    def get_metrics(self):
        """
        :return:
        """
        return self._call_endpoint("/metrics")

    def update_app(self, marathon_app, data):
        """
        :param marathon_app: name of the application
        :param data: json segment to update
        :return:
        """
        json_data = json.dumps(data)
        response = self._call_endpoint("/v2/apps/{appId}", appId=marathon_app, verb="PUT", data=json_data)
        self.logger.debug(response)
        return response

    def scale_app(self, marathon_app, instances):
        """
        :param marathon_app: name of the application
        :param instances: number of instances to scale to.
        :return:
        """
        data = {"instances": instances}
        json_data = json.dumps(data)
        response = self._call_endpoint("/v2/apps/{appId}", appId=marathon_app, verb="PUT", data=json_data)
        self.logger.debug(response)
        return response

    def create_app(self, marathon_app_definition):
        """
        :param marathon_app_definition: JSON representation of the application to be created
        :return: response
        """
        json_data = json.dumps(marathon_app_definition)
        response = self._call_endpoint("/v2/apps", verb="POST", data=json_data)
        self.logger.debug(response)
        return response
