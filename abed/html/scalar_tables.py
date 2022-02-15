import dominate
import os

from .common import navbar, bootstrap_radio_group, generate_buttons
from .utils import AbedHTMLTypes, copy_data_file
from ..conf import settings
from ..io import info
from ..utils import clean_str

tags = dominate.tags


def create_scalar_tables_html(tables):
    html = generate_tables_html(tables)
    write_tables_html(html)


def get_table_id(table):
    values = []
    values.append(clean_str(table.target))
    values.append(clean_str(table.type))
    if table.is_summary:
        values.append("summary")
    return "_".join(values)


def generate_tables_html(tables):
    doc = dominate.document(title="ABED Scalar Tables")

    with doc.head:
        # meta tags
        tags.meta(charset="utf-8")
        tags.meta(http_equiv="X-UA-Compatible", content="IE=edge")
        tags.meta(name="viewport", content="width=device-width, initial-scale=1")
        tags.meta(name="description", content="")
        tags.meta(name="author", content="")
        # tags.link(rel='icon', href=copy_data_file('ABED/images/favicon.ico'))

        # JQuery & Bootstrap JS
        tags.script(src=copy_data_file("jquery/1.11.3/jquery.min.js"))
        tags.script(src=copy_data_file("bootstrap-3.3.5-dist/js/bootstrap.min.js"))
        # Bootstrap core CSS
        tags.link(
            rel="stylesheet",
            href=copy_data_file("bootstrap-3.3.5-dist/css/bootstrap.min.css"),
        )

        # Datatables CSS & JS
        tags.link(
            rel="stylesheet",
            href=copy_data_file("DataTables-1.10.7/media/css/jquery.dataTables.css"),
        )
        tags.script(
            type="text/javascript",
            src=copy_data_file("DataTables-1.10.7/media/js/jquery.dataTables.js"),
        )

        # ABED CSS & JS
        tags.link(rel="stylesheet", href=copy_data_file("abed/css/abed.css"))
        tags.script(
            type="text/javascript",
            src=copy_data_file("abed/js/abed_showtables.js"),
        )
        tags.script(
            type="text/javascript",
            src=copy_data_file("abed/js/abed_scalartables.js"),
        )

    with doc:
        navbar(active=AbedHTMLTypes.SCALAR_TABLES)
        with tags.div(_class="container"):
            with tags.table(
                id="AbedButtons",
                _class="display",
                cellspacing="0",
                width="100%",
            ):
                with tags.thead():
                    tr = tags.tr()
                    tr += tags.th("Target")
                    tr += tags.th("Output Type")
                with tags.tbody():
                    tr = tags.tr()
                    tr += tags.td(
                        bootstrap_radio_group(generate_buttons(tables, "target"))
                    )
                    tr += tags.td(
                        bootstrap_radio_group(generate_buttons(tables, "type"))
                    )
            for table in tables:
                tabid = get_table_id(table)
                with tags.div(id="div_" + tabid, _class="AbedTable"):
                    if "summary" in tabid:
                        tags.p("Summary Table:")
                    with tags.table(
                        id="tbl_" + tabid,
                        _class="display",
                        cellspacing="0",
                        width="100%",
                    ):
                        with tags.thead():
                            tr = tags.tr()
                            for hdr in table.headers:
                                tr += tags.th(hdr)
                        if not "summary" in tabid:
                            with tags.tfoot():
                                tr = tags.tr()
                                for hdr in table.headers:
                                    tr += tags.th(hdr)
        tags.comment("/.container")
    return str(doc)


def write_tables_html(doc):
    fname = "%s%s%s%s%s" % (
        settings.OUTPUT_DIR,
        os.sep,
        "html",
        os.sep,
        "scalar_tables.html",
    )
    with open(fname, "w") as fid:
        fid.write(doc)
    info("Created output file: %s" % fname)
