"""Functions for displaying command-line help

This module contains all the documentation and functionality needed for the 
'abed help' command.

"""

# Author: Gertjan van den Burg
# Date: Sat Oct  8, 2016
# License: GPL v. 2

import datetime as dt
import textwrap

from . import __version__

# General description for the Abed help
DESCRIPTION = (
    "abed is a command line tool for managing benchmark experiments."
    "\n"
    "This is abed version %s" % __version__
)


# Categories for the commands in the Abed help
COMMAND_CATEGORIES = [
    ("Initialization commands:", ["init", "setup"]),
    ("Compute cluster job management:", ["push", "pull", "auto", "repull"]),
    ("Task management:", ["update_tasks", "reload_tasks"]),
    ("Computations:", ["run", "local"]),
    ("Abed status:", ["status", "explain_tasks", "explain_tbd_tasks"]),
    (
        "Result management:",
        ["view_results", "compress_results", "move_results", "prune_results"],
    ),
    ("Manual intervention:", ["parse_results", "process_zips"]),
]


# Short help line for each command
ABED_SHORT_HELP = {
    "auto": ("Automate push and pull to facilitate continuous operation"),
    "compress_results": "Compress completed dataset directories.",
    "explain_tbd_tasks": ("Print the task ID and command of remaining tasks"),
    "explain_tasks": ("Print the task ID and command of all defined tasks"),
    "init": "Initialize a skeleton for abed",
    "help": "Show help for Abed",
    "local": "Run the computations locally.",
    "parse_results": "Parse the results into summary files",
    "process_zips": "Process result zip files",
    "pull": "Pull all results from the cluster and process them",
    "push": "Push all necessary data to the cluster using fabric",
    "reload_tasks": "Reload the task file based on config and results",
    "repull": ("Repull results for all jobids in the auto log file"),
    "run": "Run the master/worker MPI program of abed on the cluster",
    "setup": ("Setup the remote directory structure and transfer the datasets"),
    "status": "Status of abed task list",
    "update_tasks": "Update the task list (part of pull)",
    "view_results": "Open the HTML results in the default browser",
    "move_results": "Move any results from stagedir to result dir",
    "prune_results": "Remove result files that don't occur in the config",
}


# Synopsis for commands which take parameters or options
ABED_SYNOPSES = {
    "help": "abed help [<topic>]",
    "parse_results": "abed parse_results [<options>]",
    "prune_results": "abed prune_results [<options>]",
    "local": "abed local [<options>]",
    "run": "abed run [<options>]",
    "explain_tasks": "abed explain_tasks [<options>]",
    "explain_tbd_tasks": "abed explain_tbd_tasks [<options>]",
}


# See also definitions for the commands
ABED_SEE_ALSO = {
    "auto": ["pull", "push"],
    "compress_results": ["view_results"],
    "explain_tbd_tasks": ["explain_tasks", "status"],
    "explain_tasks": ["explain_tbd_tasks", "status"],
    "init": ["setup"],
    "help": [],
    "local": ["run"],
    "parse_results": ["view_results"],
    "process_zips": ["pull", "move_results"],
    "move_results": ["process_zips", "prune_results"],
    "pull": ["auto", "push", "process_zips", "update_tasks", "repull"],
    "push": ["auto", "pull", "setup", "run"],
    "reload_tasks": ["update_tasks", "status"],
    "repull": ["pull"],
    "run": ["local"],
    "setup": ["push", "init"],
    "status": [],
    "update_tasks": ["reload_tasks", "status"],
    "view_results": ["compress_results"],
    "prune_results": ["move_results"],
}

_query_opt_doc = """\
        Optional query words to select only a subset of tasks. Tasks that 
        (partially) match all query words will be selected. Multiple query 
        words must be provided as a single command line argument with terms 
        separated by spaces, so need to be included in quotes (for example: 
        abed %s -q 'one two three')."""


# Documentation of options for commands that have options
ABED_OPTIONS = {
    "parse_results": [
        (
            "--skip-cache, -s",
            """\
                    When parsing the result files, Abed checks if the result 
                    cache needs to be reconstructed.  Since this can be a 
                    time-intensive task, it can be useful in some cases to skip 
                    cache regeneration and use an existing result cache.  With 
                    this flag to the parse_result command, cache regeneration 
                    can be skipped.  The user should be aware that results are 
                    potentially outdated or incomplete if this flag is used.
                    """,
        )
    ],
    "prune_results": [
        (
            "--dry-run, -n",
            """\
                    Don't actually prune the result files, but only print what 
                    would be done.
                    """,
        )
    ],
    "local": [("--query, -q", _query_opt_doc % "local")],
    "run": [("--query, -q", _query_opt_doc % "run")],
    "explain_tasks": [("--query, -q", _query_opt_doc % "explain_tasks")],
    "explain_tbd_tasks": [("--query, -q", _query_opt_doc % "explain_tbd_tasks")],
    "init": [("--no-commit, -n", "Don't automatically git commit changes.")],
    "update_tasks": [("--no-commit, -n", "Don't automatically git commit changes")],
    "reload_tasks": [("--no-commit, -n", "Don't automatically git commit changes")],
}


# Long help description for each command, for 'abed help <command>' calls
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
    "explain_tbd_tasks": """\
                Print an overview with the mapping from hash to task for the 
                tasks that remain to be done.
                """,
    "explain_tasks": """\
                Print an overview with the mapping from hash to task for all 
                tasks.
                """,
    "init": """\
                Initialize a new Abed experiment. This is the first step to 
                starting a new Abed experiment and should be done only once.  
                This command creates the initial files: the settings file, an 
                empty task file, an empty auto file, and two directories for 
                the datasets and executables respectively.  Additionally, Abed 
                will create a Git repository and add the settings file and the 
                task file to it.
                """,
    "help": """\
                Display help on the commands to Abed. For available commands, 
                simply type 'abed help', for help on a certain command type 
                'abed help <command>'.
                """,
    "local": """\
                Run the computations locally. This command is essentially the 
                same as the 'run' command, but it runs the computations 
                locally. Since the master-worker program in Abed that runs the 
                computations uses MPI, this command should be executed through 
                mpiexec: 'mpiexec abed local'. Note that this command requires 
                at least two cores on your workstation, one for the master 
                thread and the remainders for the working threads.
                """,
    "move_results": """\
                Move any results from the stage directory to the results 
                directory. This is useful when something goes wrong during 
                pull, but shouldn't be necessary to use in regular use.
                """,
    "parse_results": """\
                Process the result files into summary pages. This process will 
                be started automatically when Abed detects that there are no 
                more tasks to be done after the 'pull' command, but it can also 
                be used to generate result pages before all the results are in.  
                Both text summary files and web pages are generated. The 
                webpages can easily be viewed in the browser using 'abed 
                view_results'
                """,
    "process_zips": """\
                This command is included as a fallback command. In general, the 
                'pull' command should unpack the compressed archives of results 
                obtained from the compute cluster. However, if this fails for 
                some reason, this command can be used to unpack the archives 
                manually. Note that typically the archived files will not be 
                actual .zip files, but .bz2 (bzip) files.
                """,
    "prune_results": """\
                Move the result files of tasks that no longer occur in the 
                experiment to the PRUNE_DIR defined in the configuration file.  
                This can be useful in scenarios where the experiment 
                configuration evolves over time. At some point, result files 
                may remain that are no longer defined or needed in the 
                experiment.
                """,
    "pull": """\
                Download the results from the compute cluster and process them.  
                This command downloads the bzip2 archives from the bzips 
                directory in the current directory on the compute cluster, as 
                well as the PBS log files from the log directory on the compute 
                cluster. When the file transfers are finished, the bzip2 
                archives are first unpacked in the STAGE_DIR, after which they 
                are organized hierarchically based on dataset and method, in 
                the RESULT_DIR. After this is finished, the job ID of the 
                remote job is obtained from the log files and registred in the 
                AUTO_FILE. Finally, the list of remaining tasks is updated, 
                which is automatically registered in the Git repository.
                """,
    "push": """\
                This command transfers the Git repository to the compute 
                cluster and queues the job there. It's important to realise 
                that only the files that are registered in the Git repository 
                will be transferred. To help with this, the push command will 
                print an error is there are uncommitted changes in the Git 
                repository.

                If there are no uncommited changes, this command will continue 
                by transferring the Git repository to the compute cluster.  
                Next, it moves the datasets over that have been uploaded 
                earlier with the 'abed setup' command. Following this, if 
                compilation is required, the build command will run on the 
                compute cluster.  Finally, Abed will write the PBS batch file 
                and submit it to the job queue.
                """,
    "reload_tasks": """\
                This command should be used when the tasks need to be 
                regenerated from the settings file. Any changes to the METHODS, 
                DATASETS, PARAMETERS, or COMMANDS settings require that this 
                command is executed. A powerful feature of Abed is that you can 
                add to these variables while some existing tasks have already 
                been completed. This allows you to extend your experiment at a 
                later time when more methods, datasets, or paramter 
                configurations are necessary.

                Important: When using the CV_TT experiment type, only add to 
                the above settings at the _end_ of the lists. Due to technical 
                reasons related to the random seed that Abed generates for this 
                experiment type, if you add them anywhere else it will mess up 
                the hashes of the other tasks.
                """,
    "repull": """\
                With this command you can pull the results from previously 
                finished jobs. This is useful when you wish to download results 
                from the compute cluster on a different workstation. This will 
                read the job IDs from the AUTO_FILE, and pull the results from 
                the corresponding directories on the compute cluster.
                """,
    "run": """\
                This command starts the computations on the compute cluster, 
                and will typically not be run by the user, but through a (PBS) 
                job file. If for whatever reason you're running this command 
                manually, bare in mind that it should be run through mpiexec.  
                For running computations on your local workstation, use the 
                'local' command to Abed.
                """,
    "setup": """\
                This command sets up the directory structure that Abed uses on 
                the compute cluster, as well as transferring the datasets to 
                the cluster. Run this command after you've finished selecting 
                your datasets and have configured your Abed project, just 
                before the first time you run 'abed push'. This command should 
                be run only once for a project. If you need to add datasets to 
                your simulations at a later stage, copy them manually to the 
                'current/datasets' directory on the compute cluster.
                """,
    "status": """\
                Get an overview of the current status of an Abed project. This 
                command will give the number of tasks that have been defined, 
                as well as the number of tasks that remain to be done.

                Note that after you've added to the settings file to extend the 
                computations with more tasks, running this command will not 
                give the correct total. In that case, run the 'reload_tasks' 
                command first, to update the task list correctly.
                """,
    "update_tasks": """\
                This command updates the task list based on the definitions in 
                the settings file, and the result files in the RESULT_DIR 
                directory. It is automatically run after the pull command, but 
                if this fails for some reason, you can use this to update the 
                task list.
                """,
    "view_results": """\
                Open the default browser to view the results. This function is 
                included for convenience.
                """,
}


def bold(text):
    """Add bold escape sequences to text

    This adds the ``'\\033[1m'`` before the string, and ``'\\033[0m'`` after
    the string.

    Parameters
    ----------
    text : str
        Text to include in escape sequences for bold text

    Returns
    -------
    str
        Text surrounded by escape sequences

    """
    return "\033[1m" + text + "\033[0m"


def paragraph_wrapper(all_text, width=70, indent="\t"):
    """Format text to have a maximum length while maintaining paragraphs

    This function is very similar to `textwrap.wrap()
    <https://docs.python.org/3/library/textwrap.html#textwrap.wrap>`_, with the
    exception that paragraphs in the triple-quoted string will be maintained.

    Parameters
    ----------
    all_text : str
        Text to format, expected to be a triple-quoted string.

    width : int, optional
        Maximum width of the formatted text.

    indent : str, optional
        Indentation of the paragraph in the output.

    Returns
    -------
    str
        Indented formatted paragraphs

    """
    # split on paragraphs in the triple-quoted string
    texts = all_text.split("\n\n")
    # remove indentation of paragraphs
    dedents = [textwrap.dedent(text) for text in texts]
    # clean out double spaces
    cleans = [" ".join([x for x in dedented.split(" ") if x]) for dedented in dedents]
    # remove newlines
    cleaner = [clean.replace("\n", "") for clean in cleans]
    # use textwrap.fill() to wrap the text
    filled = []
    for para in cleaner:
        filled.append(
            textwrap.fill(
                para,
                width=width,
                initial_indent=indent,
                subsequent_indent=indent,
            )
        )
    # join paragraphs
    return "\n\n".join(filled)


def cmd_strings(cmds):
    """Format commands with short help for general help text

    Given a list of commands, this formats the help text in the form::

        command     short description

    The formatting is done such that the short descriptions of all the commands
    line up in the same way, and long descriptions are continued on the next
    line at the correct indentation.

    Parameters
    ----------
    cmds : list
        The command names (as strings) for which the help text should be
        generated

    Returns
    -------
    str
        Formatted help text

    """
    txt = []
    space_before = "   "
    maxlen = max((len(k) for k in ABED_SHORT_HELP))
    for cmd in cmds:
        first = True
        sentences = textwrap.wrap(ABED_SHORT_HELP[cmd], 60)
        space_after = " " * (maxlen + 2 - len(cmd))
        line = ""
        while sentences:
            arg = cmd if first else " " * len(cmd)
            lead = "%s%s%s" % (space_before, arg, space_after)
            line += lead + sentences.pop(0) + "\n"
            first = False
        line = line.rstrip("\n")
        txt.append(line)
    txt.append("")
    return txt


def get_help():
    """Generate the main help text

    Generate the main help text for Abed. This is the help text that is shown
    with the commands ``abed help`` and ``abed``. The help text is modelled on
    the help text that is shown when you run ``git`` without arguments.

    Returns
    -------
    str
        Help text for Abed

    """

    # Generate the basis text
    text = [
        "This is abed, version %s" % __version__,
        "Copyright (c) 2015-%i G.J.J. van den Burg." % dt.datetime.now().year,
        "This program is free software, see the LICENSE file for details.",
        "",
        "Usage: abed <command> [<options>]",
        "",
        "Available commands are:",
        "",
    ]

    # Expand the help text with different categories
    for category, commands in COMMAND_CATEGORIES:
        text.append(category)
        text.extend(cmd_strings(commands))

    # Add the remainder of the help text
    text += [
        "",
        "Use 'abed help <command>' to learn about a specific command,",
        "or check the online documentation at: ",
        "http://gjjvdburg.github.io/abed",
    ]

    return "\n".join(text)


def get_command_help(command):
    """Generate help text for a command

    This function generates the help text for a command that is printed when
    you call ``abed help <command>``. This command formats the help text
    similar to the structure of manual pages on Linux. The help text consists
    of several paragraphs: name, synopsis, description, and optionally a see
    also and options paragraph. The content of these paragraphs comes from the
    variables ABED_SHORT_HELP, ABED_SYNOPSES, ABED_LONG_HELP, ABED_SEE_ALSO,
    and ABED_OPTIONS.

    Parameters
    ----------
    command : str
        The command to generate help text for

    Returns
    -------
    str
        Help text formatted appropriately, None if nonexisting command.

    """
    if not command in ABED_LONG_HELP:
        return None

    # Build the required paragraphs
    synop = ABED_SYNOPSES.get(command, "abed %s" % command)
    txt = [
        "Abed Help",
        "",
        "NAME",
        "\tabed-%s - %s" % (command, ABED_SHORT_HELP[command]),
        "",
        "SYNOPSIS",
        "\t%s" % (synop),
        "",
        "DESCRIPTION",
        paragraph_wrapper(ABED_LONG_HELP[command]),
    ]

    # If the command has options, build the options paragraph
    if command in ABED_OPTIONS:
        txt += ["", "OPTIONS"]
        for option in ABED_OPTIONS[command]:
            txt.append("\t" + option[0])
            txt.append(paragraph_wrapper(option[1], width=62, indent="\t\t"))

    # If the command has see also's, build that paragraph
    if command in ABED_SEE_ALSO and ABED_SEE_ALSO[command]:
        txt += ["", "SEE ALSO", "\t" + ", ".join(ABED_SEE_ALSO[command])]

    return "\n".join(txt)
