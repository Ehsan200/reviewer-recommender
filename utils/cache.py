import _pickle as pickle
import os

CACHE_DIR = '.cache'
if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)


class Cache:

    @staticmethod
    def _get_file_location(key):
        return f'{CACHE_DIR}/{key}'

    @classmethod
    def load(cls, key):
        final_filepath = cls._get_file_location(key)
        if not os.path.exists(final_filepath):
            return None

        with open(final_filepath, 'rb') as f:
            return pickle.load(f)

    @classmethod
    def store(cls, key, data):
        final_filepath = cls._get_file_location(key)
        with open(final_filepath, 'wb') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
