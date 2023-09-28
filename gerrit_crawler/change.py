from utils import BASE_PROJECTS, CHANGE_URL_DETAIL, CHANGE_FILES_URL, CHANGE_URL_APPENDIX, PROJECT_NAMES, request_gerrit, write_results


def get_change_details(url: str, change_id: str):
    detail = request_gerrit(url.format(change_id=change_id))
    status = detail['status']
    created_at = detail['created']
    owner = detail['owner']['email']
    reviewer_objs_list = detail['reviewers']['REVIEWER']
    reviewers = []
    for reviewer_obj in reviewer_objs_list:
        reviewers.append(reviewer_obj['email'])
    return status, created_at, owner, reviewers


def get_change_files(url: str, change_id: str):
    files_data = request_gerrit(url.format(change_id=change_id))
    return list(files_data.keys())


def save_change_information(change_id, status, created_at, owner, reviewers, files, information: dict):
    for reviewer in reviewers:
        for file in files:
            information['pull_id'].append(change_id)
            information['status'].append(status)
            information['created_at'].append(created_at)
            information['owner'].append(owner)
            information['file_path'].append(file)
            information['reviewer'].append(reviewer)


def extract_change_data(data: list, proj: str):
    information = {'pull_id': [], 'status': [], 'created_at': [], 'owner': [], 'file_path': [], 'reviewer': []}
    for datum in data:
        change_id = datum['id']
        status, created_at, owner_email, reviewers_email = get_change_details(proj + CHANGE_URL_DETAIL, change_id)
        file_paths = get_change_files(proj + CHANGE_FILES_URL, change_id)
        save_change_information(change_id, status, created_at, owner_email, reviewers_email, file_paths, information)
    return information


def fetch_changes():
    for project in BASE_PROJECTS:
        data = request_gerrit(project + CHANGE_URL_APPENDIX)
        result = extract_change_data(data, project)
        write_results(PROJECT_NAMES[project], result, 'Change')


if __name__ == '__main__':
    fetch_changes()
    print('finished')
