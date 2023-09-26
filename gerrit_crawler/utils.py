import json
import requests
import pandas as pd

BASE_PROJECTS = [
    'https://android-review.googlesource.com',
]
PROJECT_NAMES = {
    'https://android-review.googlesource.com': 'android',
}
CHANGE_URL_APPENDIX = '/changes/'
CHANGE_URL_DETAIL = '/changes/{change_id}/detail/'
CHANGE_FILES_URL = '/changes/{change_id}/revisions/current/files/'
ALL_REVISIONS_URL = '/changes?o=CURRENT_REVISION&o=ALL_REVISIONS'
COMMIT_URL = '/changes/{change_id}/revisions/{revision_id}/commit/'
COMMIT_FILES_URL = '/changes/{change_id}/revisions/{revision_id}/files/'


def request_gerrit(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('error in request changes ' + str(response.status_code))
    response_body = response.text[4:]
    return json.loads(response_body)


def write_results(proj: str, results: dict, name: str):
    df = pd.DataFrame(results)
    df.to_csv(index=False, path_or_buf='./' + proj + name + '.csv')
