import os

from abed.utils import error

class Settings(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)
    def __getattr__(self, attr):
        if self.__dict__.has_key(attr):
            return getattr(self, attr)
        else:
            error("You probably Britta'd the settings file, "
                    "I'm missing parameter %s" % attr)
            raise SystemExit

def parse_dirs(config, key):
    if key.endswith('_DIR'):
        config[key] = config[key].rstrip(os.sep)

def init_config():
    cur = os.getcwd()
    files = os.listdir(cur)
    conf_file = next((x for x in files if x.startswith('abed_conf')), None)
    if conf_file is None:
        return None
    configfile = os.path.realpath(conf_file)
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
