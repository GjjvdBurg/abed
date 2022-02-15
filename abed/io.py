# -*- coding: utf-8 -*-

"""
I/O stuff
"""

import colorama
import sys


def color_string(msg, color=None, style=None):
    if not hasattr(cprint, "init"):
        cprint.init = False
    if not cprint.init:
        colorama.init()
        cprint.init = True

    colors = {
        "red": colorama.Fore.RED,
        "green": colorama.Fore.GREEN,
        "cyan": colorama.Fore.CYAN,
        "yellow": colorama.Fore.YELLOW,
        "magenta": colorama.Fore.MAGENTA,
        None: "",
    }
    styles = {
        "bright": colorama.Style.BRIGHT,
        "dim": colorama.Style.DIM,
        None: "",
    }
    pre = colors[color] + styles[style]
    post = colorama.Style.RESET_ALL
    return f"{pre}{msg}{post}"


def cprint(msg, color=None, style=None, file=sys.stdout):
    print(color_string(msg, color=color, style=style))
    file.flush()


def info(txt):
    cprint(txt)


def error(txt):
    cprint(f"ERROR: {txt}", color="red", file=sys.stderr)


def warning(txt):
    cprint(f"WARN: {txt}", color="yellow", file=sys.stderr)
