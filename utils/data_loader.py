import os
import json

from glob import glob


class DataLoader:

    def __init__(self, folder_path):
        self._folder_path = folder_path

    def read_list_raw_data_from_json_files(self, folder_name):
        final_folder = os.path.join(self._folder_path, folder_name)
        json_files = glob(os.path.join(final_folder, '*.json'))

        all_data = []

        for file_name in json_files:
            with open(file_name, 'r') as f:
                all_data += json.load(f)

        return all_data

    def read_raw_json_data_from_file(self, folder_name, file_name):
        final_path = os.path.join(self._folder_path, f'{folder_name}/{file_name}.json')
        with open(final_path, 'r') as f:
            return json.load(f)
