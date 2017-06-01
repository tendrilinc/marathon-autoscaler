from aniso8601 import parse_duration
from collections import defaultdict
from constants import FLAP_SIGNATURES
from datetime import datetime, timedelta
import logging


class HistoryManager(object):
    """
    A keeper of the recent history of scaling decisions.
    """
    def __init__(self, logger=None, dd_client=None):
        self.logger = logger or logging.getLogger(__name__)
        self.dd_client = dd_client
        self.app_performance_tail = []

    def add_to_perf_tail(self, app_scale_recommendations):
        """
        The app performance tail is the time series list of votes, decisions, timestamps and
        checksums (app version) for all participating applications. Upon adding to this list,
        it is truncated to hold the last 300 items.  It is truncated to keep memory usage
        stable as this will be a long running application.
        :param app_scale_recommendations: list of scaling recommendations per app
        :return: tail of app_scale_recommendations list
        """
        self.app_performance_tail.append(app_scale_recommendations)
        self.check_for_flapping()
        del self.app_performance_tail[:(len(self.app_performance_tail) - 300)]
        return self.app_performance_tail[::-1]

    def check_for_flapping(self):
        """ Searches through the app_performance_tail for decision flapping patterns
        :return: None
        """
        decisions = defaultdict(list)
        # gather all decisions by application
        _ = [decisions[app].append(event)
             for recommendations in self.app_performance_tail
             for app, event in recommendations.items()
             if "decision" in event.keys()]
        # clean up the list of values by sorting them by datetime
        decisions = {k: sorted(v, key=lambda x: x.get("timestamp")) for k, v in dict(decisions).items()}

        # loop over key, value to reduce value down to list of just decision values and pass to search_tail
        search_results = {k: self.__search_tail([d.get("decision") for d in v], FLAP_SIGNATURES)
                          for k, v in decisions.items()}

        [self.dd_client.send_counter_event(k, 'marathon_autoscaler.events.flapping_detected')
         for k, v in search_results.items() if len(v) > 0]

    def get_performance_tail_slice(self, app_name, after_date_time):
        """
        Gets a select portion of the application performance tail by application name
        after the specified date/time, after_date_time.
        :param app_name: Application's name
        :param after_date_time: DateTime
        :return: A slice of the application's performance tail (votes, decisions, version checksums, timestamps)
        """
        results = [event for recommendations in self.app_performance_tail
                   for app, event in recommendations.items()
                   if app_name in app and event["timestamp"] > after_date_time]
        return results

    def get_timedelta(self, iso8601_time_duration_string):
        """ A facade method for the iso8601.parse_duration method that reads a string,
        containing an iso8601 time duration value, and returns a datetime.timedelta object.
        :param iso8601_time_duration_string: a string containing an iso8601 time duration.
        :return: datetime.timedelta
        """
        time_delta = None
        try:
            time_delta = parse_duration(iso8601_time_duration_string)
        except Exception as ex:
            self.logger.error("Time Duration Unparseable: {td}".format(td=iso8601_time_duration_string))
            self.logger.error(ex)
        finally:
            return time_delta or timedelta(seconds=0)

    def is_time_window_filled(self, app_name, before_date_time):
        """
        Does the application have events that precede the tolerance time window? This function
        is necessary to determine we have filled the entire window of tolerance.
        :param app_name: Application's name
        :param before_date_time: Date/Time to validate if the tolerance window is filled.
        :return: (bool)
        """
        result = False
        past_events = [event for recommendations in self.app_performance_tail
                       for app, event in recommendations.items()
                       if app_name in app and event["timestamp"] < before_date_time]
        if len(past_events) > 0:
            result = True

        msg = "{app_name}: tolerance window filled: {result} / {before_date_time:%H:%M:%S.%f}"
        self.logger.info(msg.format(**locals()))

        dmsg = "{app_name}: {past_events}"
        self.logger.debug(dmsg.format(**locals()))

        return result

    def tolerance_reached(self, app_name, tolerance, vote):
        """
        Has an application reached the point of needing to make a decision on a
        scaling event? It ensures 3 things:
            - Is tolerance window completely filled?
            - Do all time periods have the same application version (checksum)?
            - Are all votes in the tolerance window unanimous?
        :param app_name: Application's name
        :param tolerance: ISO8601 time duration
        :param vote: A vote on an upcoming decision
        :return: (bool)
        """
        result = False
        time_difference = self.get_timedelta(tolerance)
        right_now = datetime.now()
        go_back_this_far = right_now - time_difference
        vote_list = []
        if self.is_time_window_filled(app_name, go_back_this_far):
            app_tolerated_tail = self.get_performance_tail_slice(app_name, go_back_this_far)

            if len(app_tolerated_tail) != 0:
                checksums = set([item.get("checksum") for item in app_tolerated_tail])
                vote_list = [item.get("vote") for item in app_tolerated_tail]
                votes = set(vote_list)
                if len(checksums) == 1 and len(votes) == 1 and votes == {vote}:
                    result = True

        msg = "{app_name}: tolerance reached: {result} / {go_back_this_far:%H:%M:%S.%f} - " \
              "{right_now:%H:%M:%S.%f}"
        self.logger.info(msg.format(**locals()))
        dmsg = "{app_name}: vote_list: {vote_list}; tolerance: {tolerance}; right_now: {right_now}; time_difference: {time_difference}; go_back_this_far: {go_back_this_far};"
        self.logger.debug(dmsg.format(**locals()))
        return result

    def within_backoff(self, app_name, backoff, decision):
        """
        Answers whether an application is still in its backoff period. Has a
        scaling event (of the same decision) occurred within the time duration?
        :param app_name: Application name
        :param backoff: ISO8601 time duration
        :param decision: A scaling decision
        :return: (bool)
        """
        result = False
        time_difference = self.get_timedelta(backoff)
        right_now = datetime.now()
        go_back_this_far = right_now - time_difference
        app_tail = self.get_performance_tail_slice(app_name, go_back_this_far)
        scale_events = [item for item in app_tail if item.get("decision") == decision]
        if len(scale_events) > 0:
            result = True
        msg = "{app_name}: within backoff window: {result} / {go_back_this_far:%H:%M:%S.%f} - " \
              "{right_now:%H:%M:%S.%f}"
        self.logger.info(msg.format(**locals()))
        dmsg = "{app_name}: scale events: {scale_events}"
        self.logger.debug(dmsg.format(**locals()))
        return result

    @staticmethod
    def __search_tail(corpus, *signatures):
        """ Searches the tail of corpus for matching signatures
        :param corpus: a list of elements
        :param signatures: 1 or more signatures to search for
        :return: a list of search hits
        """
        search_hits = []
        for signature in signatures:
            search_size = len(signature)
            if corpus[search_size * -1:] == signature:
                search_hits.append(signature)
        return search_hits
