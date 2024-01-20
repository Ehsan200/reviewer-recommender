from typing import Dict


def calc_rank_from_score(candidate: str, all_candidates: Dict[str, float]):
    sorted_candidates = {k: v for k, v in sorted(all_candidates.items(), key=lambda _: _[1], reverse=True)}
    index = list(sorted_candidates.keys()).index(candidate)
    return index
