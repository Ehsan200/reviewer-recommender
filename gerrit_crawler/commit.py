from utils import BASE_PROJECTS, ALL_REVISIONS_URL, request_gerrit, COMMIT_URL, COMMIT_FILES_URL, write_results, PROJECT_NAMES


def fetch_all_revisions_ids(proj_url: str):
    revisions_url = proj_url + ALL_REVISIONS_URL
    changes_list = request_gerrit(revisions_url)
    result = dict()
    for change_obj in changes_list:
        revisions_dict = change_obj['revisions']
        change_id = change_obj['id']
        revisions_ids = []
        for revision_obj in revisions_dict.keys():
            revisions_ids.append(revisions_dict[revision_obj]['_number'])
        result[change_id] = revisions_ids
    return result


def fetch_commits(proj_url: str, revisions_data: dict, info: dict):
    for change_id, revisions_ids in revisions_data.items():
        for revision_id in revisions_ids:
            url = proj_url + COMMIT_URL.format(change_id=change_id, revision_id=revision_id)
            commit_data = request_gerrit(url)
            commit_id = commit_data['commit']
            author = commit_data['committer']['email']
            date = commit_data['committer']['date']
            # in gerrit we do not have any unique hash or id for files
            files_url = proj_url + COMMIT_FILES_URL.format(change_id=change_id, revision_id=revision_id)
            commit_files = request_gerrit(files_url)
            files_paths = commit_files.keys()
            for path in files_paths:
                info['commit_id'].append(commit_id)
                info['author_login'].append(author)
                info['date'].append(date)
                info['file_path'].append(path)


def fetch_revisions():
    for project_url in BASE_PROJECTS:
        revision_ids = fetch_all_revisions_ids(project_url)
        information = {'commit_id': [], 'author_login': [], 'date': [], 'file_path': []}
        fetch_commits(project_url, revision_ids, information)
        write_results(PROJECT_NAMES[project_url], information, 'Revision')

if __name__ == '__main__':
    fetch_revisions()