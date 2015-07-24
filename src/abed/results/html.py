"""
Generate the HTML needed to display a table as a datatable

"""

import dominate
import os
import shutil

import abed

from dominate import tags
from abed import settings

def get_data_path(filepath):
    packagedir = abed.__path__[0]
    dirname = os.path.join(os.path.dirname(packagedir), 'share', 'data')
    fullname = os.path.join(dirname, filepath)
    fullpath = os.path.abspath(fullname)
    return fullpath

def copy_data_file(filepath):
    src = get_data_path(filepath)
    dest = os.path.join(settings.OUTPUT_DIR, 'html', '.datafiles', filepath)
    shutil.copy(src, dest)
    return dest

def generate_html(table):
    doc = dominate.document(title='ABED results for %s' % settings.PROJECT_NAME)
    with doc.head:
        tags.comment('DataTables CSS')
        tags.link(rel='stylesheet', href=copy_data_file(
                    'DataTables-1.10.7/media/css/jquery.dataTables.css'))
        tags.comment('jQuery')
        tags.script(type='text/javascript', 
                src=copy_data_file('DataTables-1.10.7/media/js/jquery.js'))
        tags.comment('DataTables')
        tags.script(type='text/javascript', 
                src=copy_data_file('DataTables-1.10.7/media/js/jquery.dataTables.js'))

    with doc:
        with tags.div(id='header').add(tags.ol()):
            for i in ['home', 'about', 'contact']:
                tags.li(tags.a(i.title(), href='/%s.html' % i))

        with tags.div(id='content'):
            tags.attr(cls='body')
            tags.p('Lorem ipsum ...')
            tab = tags.table(id='table', _class='display', cellspacing='0', 
                    width='90%')
            with tab.add(tags.thead()):
                l = tags.tr()
                for head in table.header:
                    l += tags.td(head)
            with tab.add(tags.tfoot()):
                l = tags.tr()
                for head in table.header:
                    l += tags.td(head)
            for _id, row in table:
                with tab.add(tags.tbody()):
                    l = tags.tr()
                    l += tags.td(_id)
                    for elem in row:
                        l += tags.td(elem)
    return doc
