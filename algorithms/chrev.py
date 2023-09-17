from typing import Dict
from datetime import datetime, date

from models import Manager, Developer, PullRequest


class ChRev:
    _manager: Manager
    # {[username]: { [filepath]: score }}
    _scores: Dict[str, Dict[str, float]]

    def __init__(self, manager: Manager):
        self._manager = manager

    @staticmethod
    def calc_diff_date(start, end):
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        return (end_date - start_date).days

    @staticmethod
    def get_max_date(data_list):
        return max(data_list, key=lambda c: c.date).date

    @staticmethod
    def get_min_date(data_list):
        return min(data_list, key=lambda c: c.date).date

    def _calc_xFactor(self, developer: Developer) -> Dict[str, float]:
        file_scores = {}
        for file in self._manager.files_list:
            score = 0
            all_file_comments = self._manager.comments[file.filepath]
            developer_comments = [_ for _ in all_file_comments if _.reviewer_username == developer.username]
            score += len(developer_comments) / len(all_file_comments)

            all_file_contributions = self._manager.contributions[file.filepath]
            all_developer_contributions = [_ for _ in all_file_contributions if _.username == developer.username]

            total_most_recent_comment_date = self.get_max_date(all_file_contributions)
            developer_most_recent_comment_date = self.get_max_date(all_developer_contributions)

            total_diff = self.calc_diff_date(
                self.get_min_date(all_file_contributions),
                total_most_recent_comment_date,
            )
            developer_diff = self.calc_diff_date(
                self.get_min_date(all_developer_contributions),
                developer_most_recent_comment_date,
            )

            score += (developer_diff / total_diff)

            score += 1 / (
                    self.calc_diff_date(
                        total_most_recent_comment_date,
                        developer_most_recent_comment_date,
                    ) + 1)

            file_scores[file.filepath] = score

        return file_scores

    # todo: implement
    def calc_score_for_pr(self, pr: PullRequest):
        # check
        pass

    def exec(self):
        for developer in self._manager.developers_list:
            self._scores[developer.username] = self._calc_xFactor(developer=developer)
