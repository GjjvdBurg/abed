"""Functions for loading the configuration file

The Abed configuration is loaded into a Settings object, after some 
preprocessing of the options. The preprocessing functions and the Settings 
class are defined here.

This module also creates a ``settings`` variable, which is an instance of the 
:class:`.Settings` class. It is supposed to be used as singleton object, by 
importing it from this module::

    from abed.conf import settings

"""

import os

from .constants import CONFIG_FILENAME
from .io import error


class Settings(object):
    """Simple Settings class

    This class functions as a simple key/value store, with one exception. If a
    key is not available in the class, an error is displayed and the program
    exits cleanly.

    """

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        else:
            error(
                "You probably Britta'd the settings file, "
                "I'm missing parameter %s" % attr
            )
            raise SystemExit


def init_config():
    """Initialize the Settings object from the configuration file

    This function reads the configuration file by parsing it as Python code.
    Next, it deletes all lowercase variables from the configuration and removes
    any trailing path seperators from directory names. Finally, it instantiates
    a :class:`.Settings` object containing the configuration.

    Returns
    -------
    settings : :class:`.Settings`
        The :class:`.Settings` object containing the configuration from the
        configuration file.

    """
    configfile = os.path.join(os.getcwd(), CONFIG_FILENAME)
    if not os.path.isfile(configfile):
        return None
    config = {}
    try:
        exec(open(configfile).read(), config)
    except NameError as err:
        error("You probably Britta'd the settings file, " "NameError: %s" % str(err))
    except Exception as err:
        error(
            "You probably Britta'd the settings file, "
            "an error occured parsing it: %s" % str(err)
        )
    keys = list(config.keys())
    for key in keys:
        if not key.upper() == key:
            del config[key]
        if key.endswith("_DIR"):
            config[key] = config[key].rstrip(os.sep)
    settings = Settings(**config)
    return settings


settings = init_config()
