import os

from .constants import CONFIG_FILENAME
from .utils import error

class Settings(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)
    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        else:
            error("You probably Britta'd the settings file, "
                    "I'm missing parameter %s" % attr)
            raise SystemExit

def parse_dirs(config, key):
    if key.endswith('_DIR'):
        config[key] = config[key].rstrip(os.sep)

def init_config():
    configfile = os.path.join(os.getcwd(), CONFIG_FILENAME)
    if not os.path.isfile(configfile):
        return None
    config = {}
    try:
        exec(open(configfile).read(), config)
    except NameError as err:
        error("You probably Britta'd the settings file, "
                "NameError: %s" % str(err))
    except Exception as err:
        error("You probably Britta'd the settings file, "
                "an error occured parsing it: %s" % str(err))
    keys = list(config.keys())
    for key in keys:
        if not key.upper() == key:
            del config[key]
        parse_dirs(config, key)
    settings = Settings(**config)
    return settings

settings = init_config()
