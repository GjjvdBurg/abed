"""Functions for displaying command-line help

This module contains all the documentation and functionality needed for the 
'abed help' command.

"""

# Author: Gertjan van den Burg
# Date: Sat Oct  8, 2016
# License: GPL v. 2

import textwrap

DESCRIPTION = ("Abed is a utility for Automated BEnchmark Distribution")

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

ABED_SHORT_HELP = {
        'auto': ('Automate push and pull to facilitate '
            'continuous operation'),
        'compress_results': 'Compress completed dataset directories.',
        'explain_tbd_tasks': ('Print the task ID and command '
            'of remaining tasks'),
        'explain_all_tasks': ('Print the task ID and command '
            'of all defined tasks'),
        'init': 'Initialize a skeleton for abed',
        'help': 'Show help for Abed',
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

ABED_SYNOPSES = {
        "parse_results": "abed parse_results [<options>]",
        "help": "abed help [<topic>]"
        }

ABED_OPTIONS = {
        "parse_results": [
            ("--skip-cache, -s", """\
                    When parsing the result files, Abed checks if the result 
                    cache needs to be reconstructed.  Since this can be a 
                    time-intensive task, it can be useful in some cases to skip 
                    cache regeneration and use an existing result cache.  With 
                    this flag to the parse_result command, cache regeneration 
                    can be skipped.  The user should be aware that results are 
                    potentially outdated or incomplete if this flag is used.
                    """)
            ]
        }


ABED_LONG_HELP = {
        "auto": """\
                The 'auto' command automates repeated uses of 'push' and 'pull' 
                commands. It regularly checks the compute cluster to see if the 
                current job is queued, running, or finished. If the job is 
                queued but not yet running, Abed will attempt to get the 
                expected starting time of the job and display this to the user.  
                If a job is running, Abed will attempt to get the remaining 
                computation time of the job, and display this to the user. If 
                no running job can be found, Abed assumes that the job is 
                finished and will try to get the job ID of the job from the log  
                files, and subsequently pull the results from the cluster. When 
                this is finished, Abed will mark the job ID in the AUTO_FILE,  
                to ensure it isn't pulled twice. After the pull command is done 
                and there are still tasks remaining, Abed will execute a push 
                command.

                The 'auto' command should only be run after a job has already 
                been submitted by using the 'push' command. Note that for the 
                'auto' command to work properly, password-less login to the 
                compute cluster should be configured. This can be done by 
                exchanging SSH keys with the cluster.
                """,
        "compress_results": """\
                The 'compress_results' command can be used when the disk space 
                used by the raw results is too large. This command finds out 
                for which datasets all tasks have been finished, and compresses 
                the corresponding directories with the highest compression 
                level possible. Since this can be a time-consuming command, it 
                is best to run it when you're asleep. The type of compression 
                algorithm used by Abed can be set using the COMPRESSION 
                setting.

                Note that after Abed creates a compressed archive of a results 
                directory for a dataset, it doesn't remove the original dataset 
                directory. This should be done by the user.
                """,
        'explain_tbd_tasks': """\
                """,
        'explain_all_tasks': """\
                """,
        'init': """\
                """,
        'help': """\
                """,
        'local': """\
                """,
        'parse_results': """\
                """,
        'process_zips': """\
                """,
        'pull': """\
                """,
        'push': """\
                """,
        'reload_tasks': """\
                """,
        'repull': """\
                """,
        'run': """\
                """,
        'setup': """\
                """,
        'status': """\
                """,
        'update_tasks': """\
                """,
        'view_results': """\
                """,
                }

def bold(text):
    return '\033[1m' + text + '\033[0m'

def paragraph_wrapper(all_text, width=60, indent='\t'):
    texts = all_text.split('\n\n')
    dedents = [textwrap.dedent(text) for text in texts]
    cleans = [' '.join([x for x in dedented.split(' ') if x]) for dedented in 
            dedents]
    cleaner = [clean.replace('\n', '') for clean in cleans]
    filled = []
    for para in cleaner:
        filled.append(textwrap.fill(para, width=width, initial_indent=indent, 
            subsequent_indent=indent))
    return '\n\n'.join(filled)

def cmd_strings(cmds):
    txt = []
    space_before = "   "
    maxlen = max((len(k) for k in ABED_SHORT_HELP))
    for cmd in cmds:
        first = True
        sentences = textwrap.wrap(ABED_SHORT_HELP[cmd], 60)
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

def get_help():
    text = ["usage: abed [-s | --skip-cache] <command>",
            "",
            DESCRIPTION,
            "",
            "Available Abed commands are:",
            ""
            ]

    for category, commands in COMMAND_CATEGORIES:
        text.append(category)
        text.extend(cmd_strings(commands))

    text += ["",
            "Use 'abed help <command>' to learn about a specific command,",
            "or check the online documentation at: ",
            "http://gjjvdburg.github.io/abed"
            ]

    return "\n".join(text)

def get_topic_help(topic, width):
    if topic in ABED_LONG_HELP:
        synop = ABED_SYNOPSES.get(topic, "abed %s" % topic)
        txt = ["Abed Help",
                "",
                bold("NAME"),
                "\tabed-%s - %s" % (topic, ABED_SHORT_HELP[topic]),
                "",
                bold("SYNOPSIS"),
                "\t%s" % (synop),
                "",
                bold("DESCRIPTION"),
                paragraph_wrapper(ABED_LONG_HELP[topic])
                ]
        if topic in ABED_OPTIONS:
            txt += [bold("OPTIONS"),
                    ]
            for option in ABED_OPTIONS[topic]:
                txt.append("\t" + option[0])
                txt.append(paragraph_wrapper(option[1], indent='\t\t'))
        return '\n'.join(txt)
    return None
