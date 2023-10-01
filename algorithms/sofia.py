from functools import cached_property
from typing import Dict

from .base_simulator import BaseSimulator
from .chrev import ChRev
from .turnoverRec import TurnoverRec


# todo: implement
class Sofia(BaseSimulator):

    @cached_property
    def _chRev_simulator(self):
        return ChRev(self._manager)

    @cached_property
    def _turnoverRec_simulator(self):
        return TurnoverRec(self._manager)

    def simulate(self):
        chRev_result = self._chRev_simulator.simulate()
        turnoverRec_result = self._turnoverRec_simulator.simulate()

        # {[pr_number]: { [dev_username]: score }}
        result: Dict[int, Dict[str, float]] = {}

        for pr in self._manager.pull_requests_list:
            result[pr.number] = {}
            for developer in self._manager.developers_list:
                pass

        return result
