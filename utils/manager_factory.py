from models import Manager
from .cache import Cache
from .data_converter import DataConverter
from .logger import info_logger


class ManagerFactory:

    def __init__(self, crawled_data_folder_path, project_name, from_cache=True):
        self._crawled_data_folder_path = crawled_data_folder_path
        self._data_converter = DataConverter(f'{crawled_data_folder_path}{project_name}')
        self._project_name = project_name
        self._from_cache = from_cache

    def get_manager(self):

        if self._from_cache:
            cached_manager = Cache.load(self._cache_file_name)
            if cached_manager is not None:
                info_logger.info('Manager loaded from cache')
                return cached_manager

        manager = Manager(self._project_name)

        converted_data = self._data_converter.load_and_convert()

        for pr in converted_data['pull_requests']:
            manager.add_pull_request(pr)
        for comment in converted_data['comments']:
            manager.add_comment(comment)
        for review in converted_data['reviews']:
            manager.add_review(review)
        for commit in converted_data['commits']:
            manager.add_commit(commit)
        for developer in converted_data['developers']:
            manager.add_developer(developer)
        for contribution in converted_data['contributions']:
            manager.add_contribution(contribution)
        for file in converted_data['files']:
            manager.add_file(file)
        for review_file in converted_data['review_files']:
            manager.add_review_file(review_file)

        info_logger.info('Manager created')

        Cache.store(self._cache_file_name, manager)
        info_logger.info('Manager stored in cache')
        return manager

    @property
    def _cache_file_name(self):
        return f'{self._project_name}.data-manager'
