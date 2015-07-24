"""
Generate the HTML needed to display a table as a datatable

"""

from dominate import tags

from abed import settings

def generate_html(table):
    h = tags.html()
    with h.add(tags.body()).add(tags.div(id='content')):
        tags.h1('ABED results for %s' % settings.PROJECT_NAME)
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
    with open('/tmp/test.html', 'w') as fid:
        fid.write(str(h))
