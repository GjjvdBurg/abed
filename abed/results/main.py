"""
Main functions for generating ABED results

"""

from abed.results.cache import update_result_cache
from abed.results.tables import make_tables

def make_results(task_dict):
    """ This is the main function for result generation. """
    abed_cache = update_result_cache(task_dict)
    make_tables(abed_cache)
