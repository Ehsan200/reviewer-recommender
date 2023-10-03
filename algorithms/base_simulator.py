import abc
from datetime import date
from typing import Union

from models import Manager, PullRequest


class BaseSimulator:
    _manager: Manager

    def __init__(self, manager: Manager):
        self._manager = manager

    @staticmethod
    def calc_diff_date(start: str, end: str):
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        return abs((end_date - start_date).days)

    @staticmethod
    def get_date_month(date_str: str):
        return date.fromisoformat(date_str).month

    @staticmethod
    def get_max_date(data_list):
        return max(data_list, key=lambda c: c.date).date

    @staticmethod
    def get_min_date(data_list):
        return min(data_list, key=lambda c: c.date).date

    @staticmethod
    def obj_time_is_between_prs(obj, prev_pr: Union[PullRequest, None], pr: PullRequest):
        if prev_pr is None:
            return obj.date <= pr.date
        return prev_pr.date <= obj.date <= pr.date

    @abc.abstractmethod
    def simulate(self):
        pass
