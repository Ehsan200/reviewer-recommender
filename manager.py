import argparse

from algorithms import Sofia, RevFinder, ChRev, TurnoverRec
from evaluation import MRR
from utils import ManagerFactory
from const import DATA_BASE_DIR
from utils.logger import info_logger

parser = argparse.ArgumentParser(description='Run algorithms on a GitHub project.')
parser.add_argument(
    '--r_owner',
    type=str,
    help="The owner of the GitHub project.",
    nargs=1,
)
parser.add_argument(
    '--r_name',
    type=str,
    help="The name of the GitHub project.",
    nargs=1,
)
parser.add_argument('--no-cache', action='store_true', help='If set, the cache will not be used.')


def validate(args):
    if args.r_owner is None or args.r_name is None:
        raise Exception('please provide both owner and name of your repo')

    if not DATA_BASE_DIR:
        raise Exception('DATA_BASE_DIR is not set.')


def run_algorithm(algorithm, args):
    validate(args)
    info_logger.info(f'algorithm {args.algorithm} for project={args.r_owner[0]}/{args.r_name[0]} started')
    manager = ManagerFactory(
        DATA_BASE_DIR,
        f'{args.r_owner[0]}-{args.r_name[0]}',
    ).get_manager()
    algorithm_instance = algorithm(manager, from_cache=not args.no_cache)
    if args.evaluate and args.mrr:
        MRR(manager, algorithm_instance).evaluate()


FUNCTION_MAP = {
    'revFinder': lambda args: run_algorithm(RevFinder, args),
    'chRev': lambda args: run_algorithm(ChRev, args),
    'turnoverRec': lambda args: run_algorithm(TurnoverRec, args),
    'sofia': lambda args: run_algorithm(Sofia, args),
}

parser.add_argument('algorithm', choices=FUNCTION_MAP.keys(), help='The algorithm to run.')
parser.add_argument('--evaluate', action='store_true', help='If set, the algorithm will be evaluated.')
parser.add_argument('--mrr', action='store_true', help='If set, the algorithm will be evaluated with MRR.')

global_args = parser.parse_args()
func = FUNCTION_MAP[global_args.algorithm]
func(global_args)
