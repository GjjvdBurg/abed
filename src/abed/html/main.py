
from .index import create_index_html
from .metric_tables import create_metric_tables_html
from .scalar_tables import create_scalar_tables_html
from .utils import copy_auxiliary_files

def generate_html(task_dict, tables):
    create_index_html(task_dict)
    metrictables = [t for t in tables if t.is_metric]
    create_metric_tables_html(metrictables)
    scalartables = [t for t in tables if not t.is_metric]
    create_scalar_tables_html(scalartables)
    copy_auxiliary_files()
