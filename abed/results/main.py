"""
Main functions for generating ABED results

"""

from abed import settings
from abed.results.cache import update_result_cache
from abed.results.cv_tt import cvtt_tables
from abed.results.tables import make_tables

def make_results(task_dict):
    """ This is the main function for result generation. """
    abed_cache = update_result_cache(task_dict)
    if settings.TYPE == 'ASSESS':
        make_tables(abed_cache)
    elif settings.TYPE == 'CV_TT':
        cvtt_tables(abed_cache)
