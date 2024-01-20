from utils.logger import info_logger
from utils.rank import calc_sorted_candidates
from .base_evaluation import BaseEvaluation


class MRR(BaseEvaluation):
    def evaluate(self):
        score = 0
        total_len = 0
        simulation_results = self.get_simulation_results()
        for pr_number, pr_results in simulation_results.items():
            ground_truth = self._get_ground_truth_of_pr(pr_number=pr_number)
            if len(ground_truth) == 0:
                continue
            total_len += 1
            ranked_list = calc_sorted_candidates(all_candidates=pr_results).keys()
            for index, item in enumerate(ranked_list):
                if item in ground_truth:
                    score += 1.0 / (index + 1)
                    break
        if total_len == 0:
            info_logger.info('No data to evaluate MRR!')
            return
        res = score / total_len
        print(f'MRR: {res}')
