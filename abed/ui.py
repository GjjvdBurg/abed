import argparse
import sys

from .conf import settings
from .models import Abed
from .utils import info, error

DESCRIPTION = ("Abed is a utility for Automated BEnchmark Distribution")

COMMANDS_HELP = {
        'auto': ('Automate push and pull to facilitate '
            'continuous operation'),
        'compress_results': 'Compress completed dataset directories.',
        'explain_tbd_tasks': ('Print the task ID and command '
            'of remaining tasks'),
        'explain_all_tasks': ('Print the task ID and command '
            'of all defined tasks'),
        'init': 'Initialize a skeleton for abed',
        'local': 'Run the computations locally.',
        'parse_results': 'Parse the results into summary files',
        'process_zips': 'Process result zip files',
        'pull': 'Pull all results from the cluster and process them',
        'push': 'Push all necessary data to the cluster using fabric',
        'reload_tasks': 'Reload the task file based on config and results',
        'repull': ('Repull results for all jobids in the auto log file'),
        'run': 'Run the master/worker MPI program of abed on the cluster',
        'setup': ('Setup the remote directory structure and transfer the '
            'datasets'),
        'status': 'Status of abed task list',
        'update_tasks': 'Update the task list (part of pull)',
        'view_results': 'Open the HTML results in the default browser'
}

COMMAND_CATEGORIES = [
        ("Initialization commands:", ["init", "setup"]),
        ("Compute cluster job management:", ["push", "pull", "auto", 
            "repull"]),
        ("Task management:", ["update_tasks", "reload_tasks"]),
        ("Computations:", ["run", "local"]),
        ("Abed status:", ["status", "explain_tbd_tasks", "explain_all_tasks"]),
        ("Result management:", ["view_results", "compress_results"]),
        ("Manual intervention:", ["parse_results", "process_zips"]),
        ]

def parse_command(command):
    choices = list(COMMANDS_HELP.keys())
    choices.append('help')
    if not command in choices:
        print("abed: '%s' is not a valid command. See 'abed --help'" % command)
        print("")
        raise SystemExit
    return command

def parse_arguments():
    cmdargs = sys.argv[1:]
    if len(cmdargs) == 0 or "-h" in cmdargs or "--help" in cmdargs:
        print(helptext())
        raise SystemExit

    args = {'skip_cache': False, 'cmd': None}
    if cmdargs[0] in ["-s", "--skip-cache"]:
        args['skip_cache'] = True
        args['cmd'] = parse_command(cmdargs[1])
    else:
        args['cmd'] = parse_command(cmdargs[0])

    return args


def make_sentences(text):
    words = []
    for part in text.split('\n'):
        words.extend(part.split(' '))
        words.append('\n')
    sentences = []
    max_length = 60
    current_length = 0
    sentence = ''
    for word in words:
        if word == '\n':
            sentences.append(sentence)
            sentence = ''
            current_length = 0
            continue
        if (current_length + len(word) + 1 <= max_length):
            current_length += len(word) + 1
            sentence += word + ' '
        else:
            current_length = len(word) + 1
            sentences.append(sentence)
            sentence = word + ' '
    return sentences


def cmd_strings(cmds):
    txt = []
    space_before = "   "
    maxlen = max((len(k) for k in COMMANDS_HELP))
    for cmd in cmds:
        first = True
        sentences = make_sentences(COMMANDS_HELP[cmd])
        space_after = ' ' * (maxlen + 2 - len(cmd))
        line = ''
        while sentences:
            arg = cmd if first else ' '*len(cmd)
            lead = '%s%s%s' % (space_before, arg, space_after)
            line += lead + sentences.pop(0) + '\n'
            first = False
        line = line.rstrip('\n')
        txt.append(line)
    txt.append("")
    return txt

def helptext():
    text = ["usage: abed [--help] [-s | --skip-cache] <command>",
            "",
            DESCRIPTION,
            "",
            "Available Abed commands are:",
            ""
            ]

    for tup in COMMAND_CATEGORIES:
        text.append(tup[0])
        text.extend(cmd_strings(tup[1]))

    text += ["Optional arguments:",
            "   -h, --help        Show this help and exit",
            "   -s, --skip-cache  Skip cache regeneration check",
            "",
            "See also the online documentation at: "
            "http://gjjvdburg.github.io/abed"]

    return "\n".join(text)


def main():
    args = parse_arguments()

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
