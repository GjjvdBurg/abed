# -*- coding: utf-8 -*-

"""
Common HTML shared between all pages (the navbar for instance)

"""

import dominate

tags = dominate.tags

from .utils import AbedHTMLTypes
from ..utils import clean_str


def navbar_content(active):
    nav = tags.ul(_class="nav navbar-nav")
    for html_type in AbedHTMLTypes.types:
        curli = tags.li(_class="active") if html_type == active else tags.li()
        curli += tags.a(html_type[0], href=html_type[1])
        nav += curli
    return nav


def navbar(active=AbedHTMLTypes.INDEX):
    with tags.nav(_class="navbar navbar-inverse navbar-fixed-top") as bar:
        with tags.div(_class="container"):
            with tags.div(_class="navbar-header"):
                with tags.button(
                    type="button",
                    _class="navbar-toggle collapsed",
                    data_toggle="collapse",
                    data_target="#navbar",
                    aria_expanded="false",
                    aria_controls="navbar",
                ):
                    tags.span("Toggle navigation", _class="sr-only")
                    tags.span(_class="icon-bar")
                    tags.span(_class="icon-bar")
                    tags.span(_class="icon-bar")
                tags.a("ABED", _class="navbar-brand", href="#")
            with tags.nav(_class="collapse navbar-collapse", id="navbar"):
                navbar_content(active)
            tags.comment("/.nav-collapse")
    return bar


def generate_buttons(tables, attribute):
    values = sorted(set([getattr(t, attribute) for t in tables]))
    buttons = []
    for value in values:
        clean = clean_str(value)
        btn = {
            "_id": "%s_%s" % (attribute, clean),
            "name": attribute,
            "value": clean,
            "label": value,
            "active": False,
        }
        buttons.append(btn)
    if buttons:
        buttons[0]["active"] = True
    return buttons


def bootstrap_radio_btn(_id, name, value, label, active=False):
    cls = "btn btn-primary active" if active else "btn btn-primary"
    btn = tags.label(_class=cls)
    if active:
        btn += tags.input(type="radio", id=_id, name=name, value=value, checked=True)
    else:
        btn += tags.input(type="radio", id=_id, name=name, value=value)
    btn += dominate.util.text(label)
    return btn


def bootstrap_radio_group(btndefs):
    with tags.div(_class="btn-group", data_toggle="buttons") as bgrp:
        for btndef in btndefs:
            bootstrap_radio_btn(**btndef)
    return bgrp
