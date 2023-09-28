import os
import pandas as pd
from collections import defaultdict
import ast
from stringCompare import LCP, LCSuff, LCSubstr, LCSubseq
import math

methodologies = [
    LCP,
    LCSubseq,
    LCSubstr,
    LCSuff,
]
current_path = './code reviewer recommendateion/'

def get_file_path_similarity(f1, f2, s) -> float:
    return s(f1, f2) / max(len(f1), len(f2))

class PullRequest:
    def __init__(self, created_at) -> None:
        self.created_at = created_at
        self.files = []

    def add_file(self, file):
        self.files.append(file)

    # get all files of each pull request -> pull_number, created_at, file_path
    @staticmethod
    def get_pull_request_files(project_name: str):
        file_name = 'datedPullFile.csv'
        old_path = 'apache-' + project_name
        new_path = project_name
        old_path = os.path.join(current_path, old_path, file_name)
        new_path = os.path.join(current_path, new_path, file_name)
        old_df = pd.read_csv(old_path)
        new_df = pd.read_csv(new_path)
        df = pd.concat([old_df, new_df])
        df = df.sort_values('date')
        return df


class DataFinder:
    def __init__(self, project_name: str) -> None:
        self.df = None
        self.project_name = project_name

    # get datedReviewFiles by order to file_path, submitted_date and pull_number and author_login
    def get_review_files_obj(self):
        file_name = 'datedReviewFile.csv'
        old_path = 'apache-' + self.project_name
        new_path = self.project_name
        old_path = os.path.join(current_path, old_path, file_name)
        new_path = os.path.join(current_path, new_path, file_name)
        old_df = pd.read_csv(old_path)
        new_df = pd.read_csv(new_path)
        df = pd.concat([old_df, new_df])
        return df.sort_values('date')


class ProjectFileSimilarity:
    project_name: str

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.scores = {
            'LCP': defaultdict(float),
            'LCSubseq': defaultdict(float),
            'LCSubstr': defaultdict(float),
            'LCSuff': defaultdict(float),
        }

    # correct it
    def calculate_methodology_score(self, all_files):
        for i in range(2):
            for j in range(2):
                file1 = all_files[i]
                file2 = all_files[j]
                for methodology in methodologies:
                    score = get_file_path_similarity(file1, file2, methodology)
                    self.scores[methodology.__name__][(file1, file2)] = score
                    self.scores[methodology.__name__][(file2, file1)] = score
                print(f'score for {i} {j} done!')

    def calculate_scores(self, pulls_df: pd.DataFrame):
        all_files = list()
        for list_files in pulls_df['file_path']:
            all_files.append(ast.literal_eval(list_files))
        print('all_files: {}'.format(len(all_files)))
        self.calculate_methodology_score(all_files)

    def get_file_similarity(self, file1, file2, methodology):
        return self.scores[methodology.__name__][(file1, file2)]


class RevFinder:
    project_name: str

    def __init__(self, project_name: str, file_similarity: ProjectFileSimilarity, reviews_df: pd.DataFrame):
        self.project_name = project_name
        self.file_similarity = file_similarity
        self.reviews_df = reviews_df

    @staticmethod
    def calculate_combined_rank(all_candidates: list, candidate: str):
        res = 0
        for list_candidates in all_candidates:
            if candidate not in list_candidates.keys():
                rank = math.inf
            else:
                rank = list_candidates[candidate]
            res += len(list_candidates.keys()) - rank
        return res

    def get_past_reviews(self, pull_request: PullRequest):
        return self.reviews_df[self.reviews_df['date'] < pull_request.created_at]
        
      
    def calc_candidates_for_new_review_with_methodology(self, new_pull_request: PullRequest):
        candidates = {
            LCP: defaultdict(float),
            LCSubseq: defaultdict(float),
            LCSubstr: defaultdict(float),
            LCSuff: defaultdict(float),
        }
        score = {
            LCP: 0,
            LCSubseq: 0,
            LCSubstr: 0,
            LCSuff: 0,
        }
        new_files = new_pull_request.files
        for _, review in self.get_past_reviews(new_pull_request).iterrows():
            files = review.file_path
            for methodology in methodologies:
                for new_file in new_files:
                    for file in files:
                        score[methodology] += self.file_similarity.get_file_similarity(
                            file1=file,
                            file2=new_file,
                            methodology=methodology,
                        )
                score[methodology] /= (len(new_files) * len(files))
                old_code_reviewers = review.reviewer_login
                for code_reviewer in old_code_reviewers:
                    candidates[methodology][code_reviewer] += score[methodology]

        return candidates

    def combination_method_on_new_review(self, new_pull: PullRequest):
        list_all_candidates_scores = list(self.calc_candidates_for_new_review_with_methodology(new_pull).values())
        unique_candidates = set()
        for candidates_scores in list_all_candidates_scores:
            unique_candidates = unique_candidates.union(set(candidates_scores.keys()))
        final_result = {}
        for candidate in unique_candidates:
            final_result[candidate] = self.calculate_combined_rank(list_all_candidates_scores, candidate)
        return final_result
