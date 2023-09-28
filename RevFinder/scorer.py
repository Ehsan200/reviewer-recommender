import os

import pandas as pd

adviced_authors_path = './RevFinder'
old_real_authors_path = './apache-'
new_real_authors_path = './new_data/apache-'
projects = [
    #'beam',
    #'flink',
    #'kafka', 
    #'spark', 
    'zookeeper'
]
ms = [1, 2, 3, 5,10]

def f1_score(recall, prec):
    return 2 * (recall * prec) / (recall + prec)

def accuracy_score(real_reviewers, predicted_reviewers, m):
    rr_len = len(predicted_reviewers['pull_number'].unique()) * m
    ar_len = len(real_reviewers[real_reviewers['pull_number'].isin(predicted_reviewers['pull_number'])]['pull_number'])
    a = predicted_reviewers.groupby(['pull_number'])['reviewer'].apply(list).reset_index()
    correct_predicted = 0
    for pull in a['pull_number']:
        reviewers = a[a['pull_number'] == pull]['reviewer']
        reviewers = (reviewers.to_list())[0]
        reviewers = reviewers[0:m]
        for reviewer in reviewers:
            if ((real_reviewers['pull_number'] == pull) & (real_reviewers['author_login'] == reviewer)).any():
                correct_predicted += 1
    return correct_predicted / ar_len, correct_predicted / rr_len

def merge_old_and_new_data(project: str):
    fname = 'datedpullauthors.csv'
    new_path = os.path.join(new_real_authors_path + project, fname)
    old_path = os.path.join(old_real_authors_path + project, fname)
    old_df = pd.read_csv(old_path)
    new_df = pd.read_csv(new_path)
    df = pd.concat([old_df, new_df])
    df.sort_values('date', inplace=True)
    return df

def load_predicted_reviewers(project: str):
    file_path = os.path.join(adviced_authors_path, project + '.csv')
    return pd.read_csv(filepath_or_buffer=file_path)

def find_accuracy_and_error(project: str, m: int, real_reviewers: pd.DataFrame):
    predicted_reviewers = load_predicted_reviewers(project=project)
    recall_s, prec = accuracy_score(real_reviewers, predicted_reviewers, m)
    f1 = f1_score(recall_s, prec)
    return f1, prec, recall_s

def main():
    for project in projects:
        print('start ' + project)
        real_reviewers = merge_old_and_new_data(project=project)
        for m in ms:
            f1, acc, recall = find_accuracy_and_error(project=project, m=m, real_reviewers=real_reviewers)
            print('f1 score = ' + str(f1))
            print('acc = ' + str(acc))
            print('recall = ' + str(recall))

if __name__ == '__main__':
    main()