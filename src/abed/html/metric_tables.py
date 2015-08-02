import dominate
import os

from abed import settings
from abed.utils import info, clean_str

from .common import navbar, bootstrap_radio_group, generate_buttons
from .utils import AbedHTMLTypes, copy_data_file

tags = dominate.tags

def create_metric_tables_html(tables):
    html = generate_tables_html(tables)
    write_tables_html(html)

def get_table_id(table):
    values = []
    values.append(clean_str(table.target))
    if settings.TYPE == 'ASSESS':
        values.append(clean_str(table.metricname))
    elif settings.TYPE == 'CV_TT':
        values.append(clean_str(table.trainmetricname))
        values.append(clean_str(table.testmetricname))
    values.append(clean_str(table.type))
    if table.is_summary:
        values.append('summary')
    return '_'.join(values)

def generate_tables_html(tables):
    doc = dominate.document(title='ABED Main page')

    with doc.head:
        # meta tags
        tags.meta(charset='utf-8')
        tags.meta(http_equiv='X-UA-Compatible', content='IE=edge')
        tags.meta(name='viewport',
                content='width=device-width, initial-scale=1')
        tags.meta(name='description', content='')
        tags.meta(name='author', content='')
        #tags.link(rel='icon', href=copy_data_file('ABED/images/favicon.ico'))

        # JQuery & Bootstrap JS
        tags.script(src=copy_data_file('jquery/1.11.3/jquery.min.js'))
        tags.script(
                src=copy_data_file('bootstrap-3.3.5-dist/js/bootstrap.min.js'))
        # Bootstrap core CSS
        tags.link(rel='stylesheet', href=copy_data_file(
            'bootstrap-3.3.5-dist/css/bootstrap.min.css'))

        # Datatables CSS & JS
        tags.link(rel='stylesheet', href=copy_data_file(
            'DataTables-1.10.7/media/css/jquery.dataTables.css'))
        tags.script(type='text/javascript', src=copy_data_file(
            'DataTables-1.10.7/media/js/jquery.dataTables.js'))

        # ABED CSS & JS
        tags.link(rel='stylesheet', href=copy_data_file('abed/css/index.css'))
        tags.script(type="text/javascript", 
                src=copy_data_file('abed/js/abed_showtables.js'))
        tags.script(type="text/javascript", 
                src=copy_data_file('abed/js/abed_metrictables.js'))

    with doc:
        navbar(active=AbedHTMLTypes.METRIC_TABLES)
        with tags.div(_class='container'):
            with tags.table(id='AbedButtons', _class='display',
                    cellspacing='0', width='100%'):
                with tags.thead():
                    tr = tags.tr()
                    tr += tags.td('Target')
                    if settings.TYPE == 'ASSESS':
                        tr += tags.td('Metric')
                    elif settings.TYPE == 'CV_TT':
                        tr += tags.td('Train Metric')
                        tr += tags.td('Test Metric')
                    tr += tags.td('Output Type')
                with tags.tbody():
                    tr = tags.tr()
                    tr += tags.td(bootstrap_radio_group(generate_buttons(
                        tables, 'target')))
                    if settings.TYPE == 'ASSESS':
                        tr += tags.td(bootstrap_radio_group(generate_buttons(
                            tables, 'metricname')))
                    elif settings.TYPE == 'CV_TT':
                        tr += tags.td(bootstrap_radio_group(generate_buttons(
                            tables, 'trainmetricname')))
                        tr += tags.td(bootstrap_radio_group(generate_buttons(
                            tables, 'testmetricname')))
                    tr += tags.td(bootstrap_radio_group(generate_buttons(
                        tables, 'type')))
        tags.comment('/.container')
        with tags.div(_class='container'):
            for table in tables:
                with tags.div(id='div_'+get_table_id(table),
                        _class='AbedTable'):
                    with tags.table(id='tbl_'+get_table_id(table), 
                            _class='display', cellspacing='0', width='100%'):
                        with tags.thead():
                            tr = tags.tr()
                            for hdr in table.headers:
                                tr += tags.th(hdr)
                        with tags.tfoot():
                            tr = tags.tr()
                            for hdr in table.headers:
                                tr += tags.th(hdr)
        tags.comment('/.container')
    return str(doc)

def write_tables_html(doc):
    fname = '%s%s%s%s%s' % (settings.OUTPUT_DIR, os.sep, 'html', os.sep, 
            'metric_tables.html')
    with open(fname, 'w') as fid:
        fid.write(doc)
    info("Created output file: %s" % fname)
