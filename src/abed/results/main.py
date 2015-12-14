"""
Main functions for generating ABED results

"""

from abed.conf import settings
from abed.html.main import generate_html

from .cache import update_result_cache
from .cv_tt import cvtt_tables
from .assess import assess_tables
from .export import export_tables

def make_results(task_dict):
    """ This is the main function for result generation. """
    abed_cache = update_result_cache(task_dict)
    if settings.TYPE == 'ASSESS':
        tables = assess_tables(abed_cache)
    elif settings.TYPE == 'CV_TT':
        tables = cvtt_tables(abed_cache)
    summary_tables = export_tables(tables)
    tables.extend(summary_tables)
    generate_html(task_dict, tables)
