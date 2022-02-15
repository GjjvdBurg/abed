# -*- coding: utf-8 -*-

import dominate
import os
import json

from .common import navbar
from .utils import AbedHTMLTypes, copy_data_file
from ..conf import settings
from ..io import info
from ..utils import clean_str
from ..results.models import AbedTableTypes

tags = dominate.tags


def create_rank_graphs_html(tables):
    html = generate_graphs_html(tables)
    write_tables_html(html)


def get_table_id(table):
    values = []
    values.append(clean_str(table.target))
    values.append(clean_str(table.type))
    if table.is_metric:
        if settings.TYPE == "ASSESS":
            values.append(clean_str(table.metricname))
        elif settings.TYPE == "CV_TT":
            values.append(clean_str(table.trainmetricname))
            values.append(clean_str(table.testmetricname))
    if table.is_summary:
        values.append("summary")
    return "_".join(values)


def generate_graphs_html(tables):
    doc = dominate.document(title="ABED Rank Graphs")

    with doc.head:
        # meta tags
        tags.meta(charset="utf-8")
        tags.meta(http_equiv="X-UA-Compatible", content="IE=edge")
        tags.meta(name="viewport", content="width=device-width, initial-scale=1")
        tags.meta(name="description", content="Rank graphs for ABED results")
        tags.meta(name="author", content="Gertjan van den Burg")

        # JQuery & Bootstrap JS
        tags.script(
            type="text/javascript",
            src=copy_data_file("jquery/1.11.3/jquery.min.js"),
        )
        tags.script(
            type="text/javascript",
            src=copy_data_file("bootstrap-3.3.5-dist/js/bootstrap.min.js"),
        )
        # Bootstrap core CSS
        tags.link(
            rel="stylesheet",
            href=copy_data_file("bootstrap-3.3.5-dist/css/bootstrap.min.css"),
        )

        # D3 and Labella
        tags.script(type="text/javascript", src=copy_data_file("d3/d3.min.js"))
        tags.script(type="text/javascript", src=copy_data_file("d3kit/d3kit.min.js"))
        tags.script(
            type="text/javascript",
            src=copy_data_file("labella/labella.min.js"),
        )
        tags.script(
            type="text/javascript",
            src=copy_data_file("d3kit-timeline/d3kit-timeline.min.js"),
        )

        # ABED CSS & JS
        tags.link(rel="stylesheet", href=copy_data_file("abed/css/abed.css"))
        tags.script(
            type="text/javascript",
            src=copy_data_file("abed/js/abed_rankgraphs.js"),
        )

    tables = [t for t in tables if t.is_summary and t.type == AbedTableTypes.RANKS]
    labels = sorted(set([t.target for t in tables]))
    lbl_table = {}
    for lbl in labels:
        lbl_table[lbl] = [t for t in tables if t.target == lbl]

    with doc:
        with tags.div(id="header"):
            navbar(active=AbedHTMLTypes.RANK_GRAPHS)
        with tags.div(id="content"):
            with tags.div(_class="container"):
                for lbl in sorted(lbl_table.keys()):
                    with tags.div(_class="panel panel-default"):
                        with tags.div(_class="panel-heading"):
                            tags.h3("Target: %s" % lbl, _class="panel-title")
                        with tags.div(_class="panel-body"):
                            for table in lbl_table[lbl]:
                                tabid = get_table_id(table)
                                if table.is_metric:
                                    if settings.TYPE == "ASSESS":
                                        tags.p("Metric: %s" % table.metricname)
                                    elif settings.TYPE == "CV_TT":
                                        with tags.div(_class="col-xs-6"):
                                            tags.b(
                                                "Train Metric on %s: %s"
                                                % (
                                                    settings.YTRAIN_LABEL,
                                                    table.trainmetricname,
                                                )
                                            )
                                        with tags.div(_class="col-xs-6"):
                                            tags.b(
                                                "Test Metric on %s: %s"
                                                % (lbl, table.testmetricname)
                                            )
                                with tags.div(id=tabid, _class="AbedRanks"):
                                    pass
                                tags.hr()
                                write_table_json(table, tabid)
            tags.comment("./container")
        with tags.div(id="footer"):
            pass

    return str(doc)


def write_table_json(table, tabid):
    data = []
    averages = next((row for _id, row in table if _id == "Average"), None)
    headers = table.headers[1:]
    for hdr, avg in zip(headers, averages):
        data.append({"name": hdr, "time": float(avg)})
    fname = os.path.join(settings.OUTPUT_DIR, "html", tabid + ".json")
    with open(fname, "w") as fid:
        fid.write(json.dumps(data))
    info("Created output file: %s" % fname)


def write_tables_html(doc):
    fname = os.path.join(settings.OUTPUT_DIR, "html", AbedHTMLTypes.RANK_GRAPHS[-1])
    with open(fname, "w") as fid:
        fid.write(doc)
    info("Created output file: %s" % fname)
