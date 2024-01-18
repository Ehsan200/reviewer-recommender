from collections import defaultdict
from functools import cached_property
from itertools import combinations

from models import Manager
from utils import Cache
from utils.logger import info_logger
from .string_compare import METHODOLOGIES


class ProjectFilesSimilarity:

    def __init__(self, manager: Manager, from_cache=True):
        self._manager = manager
        self._scores = {_.__name__: defaultdict(float) for _ in METHODOLOGIES}
        self._from_cache = from_cache

    @staticmethod
    def _get_file_path_similarity(f1, f2, methodology) -> float:
        return methodology(f1, f2) / max(len(f1), len(f2))

    @property
    def _cache_filepath(self):
        return f'{self._manager.project}.files-similarities'

    @cached_property
    def _cached_scores(self):
        return Cache.load(self._cache_filepath)

    def calculate_scores(self):
        if self._from_cache and self._cached_scores:
            self._scores = self._cached_scores
            info_logger.info('File similarity scores loaded from cache')
            return

        combinations_files = list(
            combinations(
                [_.filepath for _ in self._manager.files_list],
                2,
            )
        )
        info_logger.info('Combinations files calculated')
        info_logger.info('File similarity scores calculating...')

        for index, (f1, f2) in enumerate(combinations_files):
            for methodology in METHODOLOGIES:
                score = self._get_file_path_similarity(f1, f2, methodology)
                self._scores[methodology.__name__][(f1, f2)] = score
                self._scores[methodology.__name__][(f2, f1)] = score

        info_logger.info('File similarity scores calculated')
        Cache.store(self._cache_filepath, self._scores, chunk=True)

    def get_file_similarity(self, f1, f2, methodology):
        return self._scores[methodology.__name__][(f1, f2)]
