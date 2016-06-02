from constants import TRUTHINESS, RE_VERSION_CHECK, __version__ as marathon_autoscaler_version
import logging
import re
import settings


class ApplicationDefinition(dict):
    """
    A class that helps make interaction with the application definition document just a little nicer.
    """
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, item):
        return dict.get(self, item)

    @property
    def app_name(self):
        """
        A helper property to return the application name
        :return: str
        """
        result = None
        app_id = dict.get(self, "id")
        if app_id:
            result = app_id.lstrip("/")
        return result

    @property
    def is_app_participating(self):
        """ Determine if the application is ready for scale actions
        :return: application's participation in auto_scaling
        """
        result = False
        if self.labels:
            use_label = next((node for label, node in self.labels.items()
                              if "use_marathon_autoscaler" in label), {})
            if settings.enforce_version_match:
                if use_label is not {} and \
                   re.match(RE_VERSION_CHECK, str(use_label)) is not None and \
                   str(use_label) == marathon_autoscaler_version:
                    self.logger.debug("Version matching is enforced. Version: {0}".format(marathon_autoscaler_version))
                    self.logger.debug("{0}: participating".format(self.app_name))
                    result = True
            else:
                if use_label is not {} and \
                    (str(use_label).lower() in TRUTHINESS or
                        (re.match(RE_VERSION_CHECK, str(use_label)) is not None and
                            str(use_label) == marathon_autoscaler_version)):
                    self.logger.debug("{0}: participating".format(self.app_name))
                    result = True

        return result
