# -*- coding: utf-8 -*-

"""

This file generates the index.html file, using Bootstrap

"""

import dominate
import os

from .common import navbar
from .utils import AbedHTMLTypes, copy_data_file
from ..conf import settings
from ..tasks import init_tasks
from ..io import info

tags = dominate.tags


def create_index_html(task_dict):
    idx = generate_index_html(task_dict)
    write_index_html(idx)


def get_status_perc(task_dict):
    all_tasks = init_tasks()
    done = len(all_tasks) - len(task_dict)
    perc = float(done) / float(len(all_tasks)) * 100.0
    return int(round(perc))


def generate_index_html(task_dict):
    doc = dominate.document(title="ABED Main page")

    with doc.head:
        # meta tags
        tags.meta(charset="utf-8")
        tags.meta(http_equiv="X-UA-Compatible", content="IE=edge")
        tags.meta(name="viewport", content="width=device-width, initial-scale=1")
        tags.meta(name="description", content="")
        tags.meta(name="author", content="")
        # tags.link(rel='icon', href=copy_data_file('ABED/images/favicon.ico'))

        # JQuery & Bootstrap JS
        tags.comment("Bootstrap core JavaScript")
        tags.script(src=copy_data_file("jquery/1.11.3/jquery.min.js"))
        tags.script(src=copy_data_file("bootstrap-3.3.5-dist/js/bootstrap.min.js"))

        # Bootstrap core CSS
        tags.link(
            rel="stylesheet",
            href=copy_data_file("bootstrap-3.3.5-dist/css/bootstrap.min.css"),
        )

        # ABED CSS
        tags.link(rel="stylesheet", href=copy_data_file("abed/css/abed.css"))

    with doc:
        navbar(active=AbedHTMLTypes.INDEX)
        with tags.div(_class="container"):
            with tags.div(_class="abed-title"):
                tags.h1("ABED Results Overview for project %s" % settings.PROJECT_NAME)
            tags.p("Percentage of tasks completed:")
            with tags.div(_class="progress"):
                perc = str(get_status_perc(task_dict))
                tags.div(
                    "%s%%" % perc,
                    _class="progress-bar",
                    role="progressbar",
                    aria_valuenow=perc,
                    aria_minvalue="0",
                    aria_maxvalue="100",
                    style="width: %s%%;" % perc,
                )
        tags.comment("/.container")

    return str(doc)


def write_index_html(doc):
    fname = "%s%s%s%s%s" % (
        settings.OUTPUT_DIR,
        os.sep,
        "html",
        os.sep,
        "index.html",
    )
    with open(fname, "w") as fid:
        fid.write(doc)
    info("Created output file: %s" % fname)
