import argparse

from abed.conf import settings
from abed.models import Abed
from abed.utils import info, error

DESCRIPTION = ("ABED is a utility for Automated BEnchmark Distribution")

COMMANDS_HELP = {
        'auto': '\tAutomate push and pull to facilitate continuous operation',
        'explain_tasks': 'Print the task ID and corresponding command',
        'init': '\tInitialize a skeleton for abed',
        'local': '\tRun the computations locally.',
        'parse_results': 'Parse the results into summary files',
        'process_zips': 'Process result zip files',
        'pull': '\tPull all results from the cluster and process them',
        'push': '\tPush all necessary data to the cluster using fabric',
        'reload_tasks': 'Reload the task file based on config and results',
        'repull': ('\tRepull the zips from the cluster for all jobids in the '
            'auto log file'),
        'run': '\tRun the master/worker MPI program of abed on the cluster',
        'setup': '\tSetup the remote directory structure for abed',
        'status': '\tStatus of abed task list',
        'update_tasks': 'Update the task list (part of pull)',
        'view_results': 'Open the HTML results in the default browser'
}

class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)

def parse_arguments():
    parser = argparse.ArgumentParser(description=DESCRIPTION,
            formatter_class=SmartFormatter)

    helptxt = ['R|Command to be performed\n']
    commands = sorted(COMMANDS_HELP.keys())
    for cmd in commands:
        helptxt.append("%s:\t%s\n" % (cmd, COMMANDS_HELP[cmd]))
    parser.add_argument('cmd', choices=commands,
            help=''.join(helptxt), metavar='cmd')
    return parser.parse_args()

def main():
    args = parse_arguments()

    skip_init = False
    if args.cmd == 'reload_tasks':
        skip_init = True
    if settings is None:
        if not args.cmd == 'init':
            error("No ABED configuration file found in this directory. "
                    "Run 'abed init' to initialize one. Exiting.")
            raise SystemExit
        skip_init = True
    abed = Abed(skip_init=skip_init)

    info("Running abed command: %s" % args.cmd)
    try:
        getattr(abed, args.cmd)()
    except KeyboardInterrupt:
        info("Exiting.")
        pass
