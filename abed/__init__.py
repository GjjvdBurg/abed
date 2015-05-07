import os

class Settings(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)
    def __getattr__(self, attr):
        if self.__dict__.has_key(attr):
            return getattr(self, attr)
        else:
            print("ERROR: You probably Britta'd the settings file, "
                    "I'm missing parameter %s" % attr)
            raise SystemExit

def parse_dirs(config, key):
    if key.endswith('_DIR'):
        config[key].rstrip(os.sep)

def init_config():
    cur = os.getcwd()
    files = os.listdir(cur)
    conf_file = next((x for x in files if x.startswith('abed_conf')), None)
    if conf_file is None:
        return None
    configfile = os.path.realpath(conf_file)
    config = {}
    exec(open(configfile).read(), config)
    keys = list(config.keys())
    for key in keys:
        if not key.upper() == key:
            del config[key]
        parse_dirs(config, key)
    settings = Settings(**config)
    return settings

settings = init_config()
