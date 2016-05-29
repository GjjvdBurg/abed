"""Sphinx plugin for Abed documentation.

This file defines a cross-reference type for a setting of the Abed 
configuration file. It is copied from the similar structure used in Django.

"""


def setup(app):
    app.add_crossref_type(
            directivename="setting",
            rolename="setting",
            indextemplate="pair: %s; setting",
    )
    return {'parallel_read_safe': True}
