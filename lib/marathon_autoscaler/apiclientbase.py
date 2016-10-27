import json
import logging
import requests


class ApiClientBase(object):
    def __init__(self, uri, creds=None, logger=None):
        """
        :param uri:
        :param creds:
        :return:
        """
        self.auth = creds
        self.uri = uri.rstrip('/')
        self.logger = logger or logging.getLogger(__name__)

    @staticmethod
    def _build_path(path_suffix, **kwargs):
        """
        :param path_suffix:
        :param kwargs:
        :return:
        """
        new_path = path_suffix.format(**kwargs)
        return new_path

    def _call_endpoint(self, path, **kwargs):
        """
        :param path:
        :param kwargs:
        :return:
        """
        do_request_kwargs = {"params": None, "data": None}
        if "params" in kwargs.keys():
            do_request_kwargs["params"] = kwargs.pop("params")
        if "data" in kwargs.keys():
            do_request_kwargs["data"] = kwargs.pop("data")
        verb = self.paths[path]["verb"]
        if "verb" in kwargs.keys():
            verb = kwargs.pop("verb")
        response = self._do_request(verb, self._build_path(path, **kwargs), **do_request_kwargs)
        result = None
        if response is not None:
            contents = response.content.decode('utf-8')
            try:
                result = json.loads(contents)
            except ValueError as _:
                result = response

        return result

    def _do_request(self, method, path, params=None, data=None):
        """
        :param method:
        :param path:
        :param params:
        :param data:
        :return:
        """
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = None
        url = "".join([self.uri, path])
        try:
            response = requests.request(method, url, params=params,
                                        data=data,
                                        headers=headers,
                                        auth=self.auth)
        except requests.exceptions.RequestException as e:
            self.logger.error(e)
        return response
