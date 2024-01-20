import abc
from typing import Dict, Set

from algorithms import BaseSimulator
from models import Manager


class BaseEvaluation:
    def __init__(self, manager: Manager, simulator: BaseSimulator):
        self._manager = manager
        self._simulator = simulator

    def get_simulation_results(self) -> Dict[int, Dict[str, float]]:
        return self._simulator.simulate()

    @abc.abstractmethod
    def evaluate(self):
        pass

    def _get_ground_truth_of_pr(self, pr_number: int) -> Set[str]:
        return {
            _.reviewer_username
            for _ in self._manager.reviews_list
            if _.pull_number == pr_number
        }
