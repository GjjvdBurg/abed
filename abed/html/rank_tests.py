# -*- coding: utf-8 -*-

import dominate
import os

from .common import navbar
from .rank_graphs import get_table_id
from .utils import AbedHTMLTypes, copy_data_file
from ..conf import settings
from ..io import info
from ..results.models import AbedTableTypes
from ..results.significance import global_difference, reference_difference

tags = dominate.tags


def create_rt_html(tables):
    html = generate_rt_html(tables)
    write_tables_html(html)


def generate_label_panel(lbl, lbl_table):
    headers = ["Method", "Z-statistic", "P-value", "Sig. diff."]
    with tags.div(_class="panel panel-default") as panel:
        with tags.div(_class="panel-heading"):
            tags.h3("Target: %s" % lbl, _class="panel-title")
        with tags.div(_class="panel-body"):
            for table in lbl_table[lbl]:
                if len(settings.METHODS) <= 1:
                    continue
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
                                "Test Metric on %s: %s" % (lbl, table.testmetricname)
                            )
                with tags.div(id=tabid, _class="AbedRankTests"):
                    fval, fprob = global_difference(table)
                    tags.p("Friedman Test: F = %.4f with p-value %.6f" % (fval, fprob))
                    if settings.REFERENCE_METHOD is None:
                        continue
                    holms, CD = reference_difference(table)
                    tags.p(
                        "Holm's procedure, comparing all with %s:"
                        % settings.REFERENCE_METHOD
                    )
                    tags.p("Critical difference: %f" % CD)
                    with tags.table(
                        id="rt_" + tabid,
                        _class="display",
                        cellspacing="0",
                        width="100%",
                    ):
                        with tags.thead():
                            tr = tags.tr()
                            for hdr in headers:
                                tr += tags.th(hdr)
                        with tags.tbody():
                            for method, zscore, pval, sigdiff in holms:
                                tr = tags.tr()
                                tr += tags.td(method)
                                tr += tags.td(zscore)
                                tr += tags.td(pval)
                                tr += tags.td(str(int(sigdiff)))
                tags.hr()
    return panel


def generate_rt_html(tables):
    doc = dominate.document(title="ABED Rank Tests")

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

        # ABED CSS & JS
        tags.link(rel="stylesheet", href=copy_data_file("abed/css/abed.css"))

    tables = [t for t in tables if t.is_summary and t.type == AbedTableTypes.RANKS]
    labels = sorted(set([t.target for t in tables]))
    lbl_table = {}
    for lbl in labels:
        lbl_table[lbl] = [t for t in tables if t.target == lbl]

    with doc:
        with tags.div(id="header"):
            navbar(active=AbedHTMLTypes.RANK_TESTS)
        with tags.div(id="content"):
            with tags.div(_class="container"):
                for lbl in sorted(lbl_table.keys()):
                    generate_label_panel(lbl, lbl_table)
            tags.comment("./container")
        with tags.div(id="footer"):
            pass

    return str(doc)


def write_tables_html(doc):
    fname = os.path.join(settings.OUTPUT_DIR, "html", AbedHTMLTypes.RANK_TESTS[-1])
    with open(fname, "w") as fid:
        fid.write(doc)
    info("Created output file: %s" % fname)
