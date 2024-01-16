import math
from collections import defaultdict
from typing import Dict, List

from models import PullRequest, Manager
from utils import Cache
from utils.logger import info_logger
from .base_simulator import BaseSimulator
from .utils.rev_finder import ProjectFilesSimilarity, METHODOLOGIES


class RevFinder(BaseSimulator):

    def __init__(self, manager: Manager, from_cache=True):
        super().__init__(manager, from_cache)
        self.file_similarity = ProjectFilesSimilarity(self._manager, from_cache=self._from_cache)

    def calc_candidates_with_methodologies(self, pr: PullRequest):

        candidates = {_.__name__: defaultdict(float) for _ in METHODOLOGIES}
        scores = {_.__name__: 0 for _ in METHODOLOGIES}

        new_files = pr.file_paths

        past_reviews = [
            _ for _ in self._manager.reviews_list if _.date < pr.date
        ]

        for review in past_reviews:

            review_files = [
                filepath for _ in self._manager.pull_requests_list if
                _.number == review.pull_number for filepath in _.file_paths
            ]
            if len(review_files) == 0 or len(new_files) == 0:
                continue

            for methodology in METHODOLOGIES:
                methodology_name = methodology.__name__
                for new_file in new_files:
                    for file in review_files:
                        scores[methodology_name] += self.file_similarity.get_file_similarity(
                            f1=file,
                            f2=new_file,
                            methodology=methodology,
                        )
                scores[methodology_name] /= (len(new_files) * len(review_files))
                candidates[methodology_name][review.reviewer_username] += scores[methodology_name]

        return candidates

    @staticmethod
    def calculate_combined_rank(all_candidates: List[Dict[str, float]], candidate: str):
        res = 0
        for list_candidates in all_candidates:
            if candidate not in list_candidates.keys():
                user_rank = math.inf
            else:
                user_rank = list_candidates[candidate]
            res += len(list_candidates.keys()) - user_rank
        return res

    def simulate(self):
        info_logger.info("Simulating RevFinder...")
        if self.cached_result:
            info_logger.info("Simulating RevFinder loaded from cache")
            return self.cached_result

        self.file_similarity.calculate_scores()

        # {[pr_number]: { [dev_username]: user_rank }}
        result: Dict[int, Dict[str, float]] = {}

        pr_len = len(self._manager.pull_requests_list)
        for index, pr in enumerate(self._manager.pull_requests_list):
            info_logger.info(f'Calculating candidates: {index + 1}/{pr_len}')
            candidates_per_methodology = list(self.calc_candidates_with_methodologies(pr=pr).values())

            # todo: refactor
            all_unique_candidates_usernames = set()
            for candidates_user_scores in candidates_per_methodology:
                all_unique_candidates_usernames = all_unique_candidates_usernames.union(
                    set(candidates_user_scores.keys())
                )

            result[pr.number] = {
                candidate_username: self.calculate_combined_rank(candidates_per_methodology, candidate_username)
                for candidate_username in all_unique_candidates_usernames
            }

        Cache.store(self._cache_filename, result)
        info_logger.info("Simulating RevFinder stored in cache")
        return result
