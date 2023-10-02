from typing import Dict

from models import Developer, PullRequest
from .base_simulator import BaseSimulator


class TurnoverRec(BaseSimulator):
    def _calc_ReviewerKnows(self, developer: Developer, pr: PullRequest):
        # {[int: review_id]: [float: score]}
        res: Dict[int, float] = {}
        all_reviews = [_ for _ in self._manager.reviews_list if _.pull_number == pr.number]
        all_review_files = [_ for _ in self._manager.review_files_list if _.pull_number == pr.number]

        for review in all_reviews:
            review_files = [_ for _ in all_review_files if _.review_id == review.id]
            review_files_paths = [_.filepath for _ in review_files]

            previous_reviews = [
                _ for _ in self._manager.reviews_list if
                review.date > _.date and _.reviewer_username == developer.username
            ]
            previous_reviews_ids = [_.id for _ in previous_reviews]
            previous_review_files = [
                _ for _ in self._manager.review_files_list if
                _.review_id in previous_reviews_ids and _.filepath in review_files_paths
            ]

            previous_commits = [
                _ for _ in self._manager.commits_list
                if _.username == developer.username and review.date > _.date
            ]

            res[review.id] = (len(previous_review_files) + len(previous_commits)) / len(review_files)

        return res

    def _calc_learnRec(self, developer: Developer, pr: PullRequest):
        # todo: check with article
        final_res: Dict[int, float] = {}
        for review_id, score in self._calc_ReviewerKnows(developer=developer, pr=pr).items():
            final_res[review_id] = 1 - (1 / score)
        return final_res

    def _is_diff_under_year(self, f_date, e_date):
        return self.calc_diff_date(f_date, e_date) <= 365

    def _calc_totalCommitReview(self, pr: PullRequest):
        return len([
            _ for _ in self._manager.reviews_list if self._is_diff_under_year(pr.date, _.date)
        ]) + len([
            _ for _ in self._manager.commits_list if self._is_diff_under_year(pr.date, _.date)
        ])

    def _calc_contributionRatio(self, pr: PullRequest):
        result: Dict[str, float] = {}
        totalCommitReviews = self._calc_totalCommitReview(pr=pr)

        for developer in self._manager.developers_list:
            result[developer.username] = len([
                _ for _ in self._manager.reviews_list
                if self._is_diff_under_year(pr.date, _.date) and _.reviewer_username == developer.username
            ]) + len([
                _ for _ in self._manager.commits_list
                if self._is_diff_under_year(pr.date, _.date) and _.reviewer_username == developer.username
            ]) / totalCommitReviews

        return result

    def simulate(self):
        # todo: implement
        pass
