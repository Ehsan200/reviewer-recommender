from collections import defaultdict
from itertools import combinations

from models import Manager
from .string_compare import METHODOLOGIES


class ProjectFilesSimilarity:

    def __init__(self, manager: Manager):
        self._manager = manager
        self._scores = {_.__name__: defaultdict(float) for _ in METHODOLOGIES}

    @staticmethod
    def _get_file_path_similarity(f1, f2, methodology) -> float:
        return methodology(f1, f2) / max(len(f1), len(f2))

    def calculate_scores(self):
        combinations_files = list(
            combinations(
                [_.filepath for _ in self._manager.files_list],
                2,
            )
        )
        for f1, f2 in combinations_files:
            for methodology in METHODOLOGIES:
                score = self._get_file_path_similarity(f1, f2, methodology)
                self._scores[methodology.__name__][(f1, f2)] = score
                self._scores[methodology.__name__][(f2, f1)] = score

    def get_file_similarity(self, f1, f2, methodology):
        return self._scores[methodology.__name__][(f1, f2)]
