import sys

from .conf import settings
from .help import get_help, get_command_help
from .models import Abed
from .utils import info, error

def parse_command(command):
    choices = list(Abed.commands)
    choices.append('help')
    if not command in choices:
        print("abed: '%s' is not a valid command. See 'abed help'" % command)
        print("")
        raise SystemExit
    return command

def parse_arguments():
    cmdargs = sys.argv[1:]
    if len(cmdargs) == 0:
        print(get_help())
        raise SystemExit

    args = {'skip_cache': False, 'cmd': None, 'topic': None}
    idx = 0
    args['cmd'] = parse_command(cmdargs[idx])
    idx += 1
    if args['cmd'] == 'help' and len(cmdargs) > idx:
        args['topic'] = parse_command(cmdargs[idx])
    elif args['cmd'] == 'parse_results' and len(cmdargs) > idx:
        if cmdargs[idx] in ["-s", "--skip-cache"]:
            args['skip_cache'] = True
        else:
            error("Unknown command line argument: %s." % cmdargs[idx])
            error("See 'abed help parse_results' for help.")
            raise SystemExit
    elif len(cmdargs) > idx:
            error("Unknown command line argument: %s." % cmdargs[idx])
            error("See 'abed help' for help.")
            raise SystemExit

    return args

def main():
    args = parse_arguments()
    if args['cmd'] == 'help':
        if args['topic'] is None:
            print(get_help())
            raise SystemExit
        else:
            print(get_command_help(args['topic']))
            raise SystemExit

    skip_init = False
    if args['cmd'] == 'reload_tasks':
        skip_init = True

    if settings is None:
        if not args['cmd'] == 'init':
            error("No ABED configuration file found in this directory. "
                    "Run 'abed init' to initialize one. Exiting.")
            raise SystemExit
        skip_init = True
    abed = Abed(skip_init=skip_init, skip_cache=args['skip_cache'])

    info("Running abed command: %s" % args['cmd'])
    try:
        getattr(abed, args['cmd'])()
    except KeyboardInterrupt:
        info("Exiting.")
        pass
