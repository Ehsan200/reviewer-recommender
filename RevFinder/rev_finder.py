import os
import threading
import pandas as pd
from utils import DataFinder, ProjectFileSimilarity, PullRequest, RevFinder

reviews_df = None
results = {}

def prepare_csv_data(project_name):
    data_finder = DataFinder(project_name)
    reviews_df = data_finder.get_review_files_obj()
    a = reviews_df.groupby(['pull_number', 'date'])['file_path'].apply(list).reset_index()
    b = reviews_df.groupby(['pull_number', 'date'])['reviewer_login'].apply(set).reset_index()
    result = a.join(b, how='inner', lsuffix='_a')
    result = result[['pull_number', 'date', 'file_path', 'reviewer_login']]
    pull_req_files_df = PullRequest.get_pull_request_files(project_name)
    pull_req_files_df = pull_req_files_df.groupby(['pull_number', 'date'])['file_path'].apply(list).reset_index()
    return pull_req_files_df, result


def write_output(project_name, result):
    temp_pull_list = []
    temp_reviewer_list = []
    for pull_number in result.keys():
        for reviewer in result[pull_number]:
            temp_pull_list.append(pull_number)
            temp_reviewer_list.append(reviewer)
    data = {'pull_number': temp_pull_list, 'reviewer': temp_reviewer_list}
    res_df = pd.DataFrame(data)
    res_df.sort_values('pull_number', inplace=True)
    folder_path = './rev-finder-dist/'
    is_exists = os.path.exists(folder_path)
    if not is_exists:
        os.makedirs(folder_path)

    res_df.to_csv(folder_path + project_name + '.csv', index=False)

def do_job(pulls, pull_number, rev_finder):
    reviewers_scores = rev_finder.combination_method_on_new_review(pulls[pull_number])
    print('pull ' + str(pull_number))
    global results
    results[pull_number] = reviewers_scores
    print(results)


if __name__ == '__main__':
    projects = [
        'beam',
        'flink',
        'kafka',
        'spark',
        'zookeeper',
    ]
    
    for project in projects:
        print('start ' + project)
        results = {}
        pulls_df, reviews_df = prepare_csv_data(project)
        file_similarity = ProjectFileSimilarity(project_name=project)
        file_similarity.calculate_scores(pulls_df)
        rev_finder = RevFinder(project_name=project, file_similarity=file_similarity, reviews_df=reviews_df)
        threads = []
        for pull_number in pulls_df['pull_number'].unique():
            th = threading.Thread(target=do_job, args=(pulls_df, pull_number, rev_finder))
            th.start()
            threads.append(th)
        for thread in threads:
            thread.join()
        write_output(project, result=results)
        print("finished")
