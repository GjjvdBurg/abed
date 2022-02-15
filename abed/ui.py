# -*- coding: utf-8 -*-


import sys

from pydoc import pager

from .conf import settings
from .help import get_help, get_command_help
from .models import Abed
from .io import error


def parse_command(command):
    choices = list(Abed.commands)
    choices.append("help")
    if not command in choices:
        print("abed: '%s' is not a valid command. See 'abed help'" % command)
        print("")
        raise SystemExit(1)
    return command


def parse_arguments():
    cmdargs = sys.argv[1:]
    if len(cmdargs) == 0 or "-h" in cmdargs:
        print(get_help())
        raise SystemExit(1)

    args = {
        "skip_cache": False,
        "prune_dry_run": False,
        "cmd": None,
        "topic": None,
        "query_words": None,
        "no_commit": False,
    }
    idx = 0
    args["cmd"] = parse_command(cmdargs[idx])
    idx += 1
    if args["cmd"] == "help" and len(cmdargs) > idx:
        args["topic"] = parse_command(cmdargs[idx])
    elif args["cmd"] == "parse_results" and len(cmdargs) > idx:
        if cmdargs[idx] in ["-s", "--skip-cache"]:
            args["skip_cache"] = True
        else:
            error("Unknown command line argument: %s." % cmdargs[idx])
            error("See 'abed help parse_results' for help.")
            raise SystemExit(1)
    elif args["cmd"] == "prune_results" and len(cmdargs) > idx:
        if cmdargs[idx] in ["-n", "--dry-run"]:
            args["prune_dry_run"] = True
        else:
            error("Unknown command line argument: %s." % cmdargs[idx])
            error("See 'abed help prune_results' for help.")
            raise SystemExit(1)
    elif (
        args["cmd"] in ["local", "run", "explain_tbd_tasks", "explain_tasks"]
        and len(cmdargs) > idx
    ):
        if cmdargs[idx] in ["-q", "--query"]:
            args["query_words"] = cmdargs[idx + 1].strip().split(" ")
        else:
            error("Unknown command line argument: %s." % cmdargs[idx])
            error("See 'abed help %s' for help." % args["cmd"])
            raise SystemExit(1)
    elif args["cmd"] in ["init", "update_tasks", "reload_tasks"] and len(cmdargs) > idx:
        if cmdargs[idx] in ["-n", "--no-commit"]:
            args["no_commit"] = True
    elif len(cmdargs) > idx:
        error("Unknown command line argument: %s." % cmdargs[idx])
        error("See 'abed help' for help.")
        raise SystemExit(1)

    return args


def main():
    args = parse_arguments()
    if args["cmd"] == "help":
        if args["topic"] is None:
            print(get_help())
            raise SystemExit(1)
        else:
            pager(get_command_help(args["topic"]))
            raise SystemExit(1)

    skip_init = False
    if args["cmd"] == "reload_tasks":
        skip_init = True

    if settings is None:
        if not args["cmd"] == "init":
            error(
                "No ABED configuration file found in this directory. "
                "Run 'abed init' to initialize one. Exiting."
            )
            raise SystemExit(1)
        skip_init = True
    abed = Abed(
        skip_init=skip_init,
        skip_cache=args["skip_cache"],
        prune_dry_run=args["prune_dry_run"],
        query_words=args["query_words"],
        no_commit=args["no_commit"],
    )

    try:
        getattr(abed, args["cmd"])()
    except KeyboardInterrupt:
        pass
