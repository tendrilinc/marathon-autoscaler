from collections import defaultdict, Counter
from constants import compare, RE_THRESHOLD, RE_DELIMITERS
from utils import list_get
import logging
import re
import settings


class RulesManager(object):
    """
    To manage all of the rules. A rule is a single description centered around a metric.  A rule can have a part denoted
    by an underscore followed by a part value (it is useful to use a numerical part value).  Multiple rule parts are
    automatically combined by having the same rule name.
    A single rule is a dict object:
    {
        "{{ prefix__rule_name__rule_part }}": {
            "ruleInfo": {
                "ruleName": "{{rule_name}}",
                "rulePart": "{{rule_part}}"
            },
            {
            "ruleValue": {
                "metric",
                "threshold": {op, val},
                "backoff",
                "scale_factor",
                "tolerance",
                "weight"
            }
        }
    }
    """
    def __init__(self, app_def, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.app_def = app_def
        self.rules = self._find_autoscaler_rules()
        self._last_triggered_rule = None

    def trigger_rules(self, metrics):
        """
        Consumes a dict of metrics and attempts to match an application's rules to its metric information.
        :param metrics: dict of metric values
        :return: The recently triggered rule
        """

        triggered_rule = self._get_matched_rule(metrics)

        self._last_triggered_rule = triggered_rule
        info_msg = "{app_name}: metrics: {metrics}"
        self.logger.info(info_msg.format(app_name=self.app_def.app_name,
                                         metrics=metrics))
        info_msg = "{app_name}: last_triggered_rule set to: {triggered_rule}"
        self.logger.info(info_msg.format(app_name=self.app_def.app_name,
                                         triggered_rule=triggered_rule))
        return self._last_triggered_rule

    @property
    def last_triggered_rule(self):
        """
        The last rule triggered by the RuleManager
        :return:
        """
        triggered_rule = None
        if self._last_triggered_rule is not None:
            triggered_rule = self._last_triggered_rule
        return triggered_rule

    @property
    def last_triggered_criteria(self):
        """
        A helper property to aim at providing the core criteria of the last triggered rule.
        :return: A dict of rule criteria
        """
        criteria = {}
        if self._last_triggered_rule is not None:
            rule_value = self._last_triggered_rule[0].get("ruleValue")
            criteria = dict(scale_factor=rule_value.get("scale_factor"),
                            tolerance=rule_value.get("tolerance"),
                            backoff=rule_value.get("backoff"))
        return criteria

    def _find_autoscaler_rules(self):
        rules_found = {}
        if self.app_def.labels:
            for k, v in self.app_def.labels.items():
                rule_match = re.match(r"^{prefix}_(?P<ruleName>[A-Za-z0-9]+)_?(?P<rulePart>[A-Za-z0-9]+)*".format(
                    prefix=settings.rules_prefix), k)
                if rule_match is not None:
                    rule_values = re.split(RE_DELIMITERS, v)
                    if len(rule_values) < 5:
                        self.logger.warn("Scaling rule identified, but wrong number of arguments. Disregarding "
                                         "{rule_name} = {rule_values}".format(rule_name=k,
                                                                              rule_values=rule_values))
                        continue

                    rule_values_dict = dict(metric=rule_values[0],
                                            threshold=self._parse_threshold(rule_values[1]),
                                            tolerance=rule_values[2],
                                            scale_factor=rule_values[3],
                                            backoff=rule_values[4],
                                            weight=list_get(rule_values, 5, 1.0))
                    rules_found[k] = dict(ruleValue=rule_values_dict, ruleInfo=rule_match.groupdict())
                elif "max_instances" in k.lower():
                    self.max_instances = int(v)
                elif "min_instances" in k.lower():
                    self.min_instances = int(v)
        interpreted_rules = defaultdict(list)
        if rules_found:
            [interpreted_rules[v.get("ruleInfo").get("ruleName")].append(v)
             for k, v in rules_found.items()]

        return dict(interpreted_rules)

    def is_app_participating(self):
        """ Determine if the application is ready for scale actions
        :return: application's participation in auto_scaling
        """
        return self.app_def.is_app_participating

    def is_app_within_min_or_max(self):
        """ Determine if the application is ready for scale actions.
        :return: application's participation in auto_scaling
        """
        msg = "{0}: instances: min:{1}, running:{2}, max:{3}"
        self.logger.info(msg.format(self.app_def.app_name,
                                    int(self.min_instances),
                                    int(self.app_def.tasksRunning),
                                    int(self.max_instances)
                                    ))
        return int(self.min_instances) <= \
            int(self.app_def.tasksRunning) <= \
            int(self.max_instances)

    def is_app_ready(self):
        """ Determine if the application is ready for scale actions
        :return: application's readiness for scale actions
        """
        result = False
        if self.app_def.tasksRunning == self.app_def.instances:
            result = True

        self.logger.info("{0}: application ready: {1}".format(
            self.app_def.app_name, result))
        return result

    def _get_matched_rule(self, metrics):
        matched_rule = None
        rules_found = []
        for rule_name, rule in self.rules.items():
            rule_criteria_count = len(rule)
            matched_rule_criteria = [rule_item
                                     for rule_item in rule
                                     for metric_name, metric_value in metrics.items()
                                     if rule_item.get("ruleValue").get("metric") in metric_name and
                                     self._beyond_threshold(metric_value, rule_item.get("ruleValue").get("threshold"))]
            if len(matched_rule_criteria) == rule_criteria_count:
                rules_found.append(rule)

        self.logger.debug("triggering rules by metrics: {rules_found}".format(rules_found=rules_found))

        if len(rules_found) > 1:
            matched_rule = self._find_best_matched_rule_by_criteria(rules_found)
        elif len(rules_found) == 1:
            matched_rule = rules_found[0]

        return matched_rule

    def _find_best_matched_rule_by_criteria(self, rules):
        """
        This is the Highlander method; there can only be one...
        Round 1 : Who has the most rule criteria matched?
        :param rules:
        :return:
        """
        rule_criteria_counter = Counter()
        for rule in rules:
            rule_criteria_counter[rule[0].get("ruleInfo").get("ruleName")] = len(rule)

        most_critical_rule_names = [k for k, v in rule_criteria_counter.items()
                                    if v == rule_criteria_counter.most_common()[0][1]]

        if len(most_critical_rule_names) > 1:
            critical_rules = {name: next(rule
                                         for rule_parts in rules
                                         for rule in rule_parts
                                         if name in rule.get("ruleInfo").get("ruleName"))
                              for name in most_critical_rule_names}
            winning_rule = self._find_best_matched_rule_by_weight(critical_rules)
        else:
            winning_rule = [rule
                            for rule_parts in rules
                            for rule in rule_parts
                            if most_critical_rule_names[0] in
                            rule.get("ruleInfo").get("ruleName")]
        self.logger.debug("winning rule by criteria: {winning_rule}".format(winning_rule=winning_rule))
        return winning_rule

    def _find_best_matched_rule_by_weight(self, rules):
        """
        Round 2 : Which rule has the most weight? Weight is multiplied against scale_factor
        :param rules: A dict of rules
        :return: One rule with the maximum weight
        """
        self.logger.debug(rules)
        rule_weights = {rule.get("ruleInfo").get("ruleName"): abs(rule.get("ruleValue").get("scale_factor") *
                                                                  rule.get("ruleValue").get("weight"))
                        for rule_name, rule in rules.items()}
        self.logger.debug("winning rule by weight: {weighted_rule}".format(weighted_rule=rules.get(max(rule_weights))))

        return rules.get(max(rule_weights))

    def _parse_threshold(self, threshold):
        """
        Parses the string representing the threshold. A threshold is a comparison operator and number.
        :param threshold: String
        :return: Lambda expression matching the operator
        """
        m = re.search(RE_THRESHOLD, threshold)
        return m.groupdict()

    def _beyond_threshold(self, metric, threshold):
        """
        This will answer whether the metric has met or exceeded the threshold. It uses
        the dictionary created above, compare, to look up the operation, th["op"] and
        passes the metric and threshold value, th["val"] to the lambda expression that
        corresponds with the operation.
        :param metric: The performance metric (cpu, memory, etc...)
        :param threshold: String representation of the threshold (>, <, =, ==, <=, >=)
        :return: (bool)
        """
        return compare[threshold["op"]](float(metric), float(threshold["val"]))
