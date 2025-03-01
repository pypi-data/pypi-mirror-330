#!/usr/bin/env python
# -*- coding: utf-8 - *-

# Copyright (c) 2020 Romeet Chhabra

__author__ = "Romeet Chhabra"
__copyright__ = "Copyright 2020, Romeet Chhabra"
__license__ = "GPL-3.0-or-later"

import argparse
import os
import shutil
import sys
import time
from importlib.resources import files
from configparser import ConfigParser
from pathlib import Path
from stat import filemode


# https://en.wikipedia.org/wiki/ANSI_escape_code
def _print_format_table():
    for style in range(9):
        for fg in range(30, 40):
            s1 = ""
            for bg in range(40, 50):
                fmt = ";".join([str(style), str(fg), str(bg)])
                s1 += f"\x1b[{fmt}m {fmt} \x1b[0m"
            print(s1)
        print("\n")


if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
    from pwd import getpwuid
    from grp import getgrgid

    UID_SUPPORT = True
else:
    UID_SUPPORT = False


def _get_config(fp=None):
    config = ConfigParser()
    # Read config file from (in order) bundled config,
    # XDG_CONFIG_HOME, HOME, or parent folder.
    if __name__ != "__main__":
        conf = files("colorls.config").joinpath("colorls.toml")
    else:
        conf = Path(__file__).parent.absolute() / "config/colorls.toml"
    config.read(
        [
            conf,
            Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
            / "colorls/colorls.toml",
            Path("~/.colorls.toml").expanduser(),
        ],
        encoding="utf8",
    )
    return config


def write_config(filepath):
    config = _get_config()
    print(f"Writing config to {filepath}... ", end="")
    with open(filepath, "w") as fp:
        config.write(fp)
    print("DONE")


def get_config():
    config = _get_config()
    return (
        dict(config["COLOR"]),
        dict(config["ICONS"]),
        dict(config["ALIASES"]),
        dict(config["SUFFIXES"]),
    )


COLOR, ICONS, ALIAS, SUFFIX = get_config()
METRIC_PREFIXES = ["b", "K", "M", "G", "T", "P", "E", "Z", "Y"]
METRIC_MULTIPLE = 1024.0
SI_MULTIPLE = 1000.0


def get_human_readable_size(size, base=METRIC_MULTIPLE):
    for pre in METRIC_PREFIXES:
        if size < base:
            return f"{size:4.0f}{pre}"
        size /= base


def get_keys(path):
    n, ext = path.stem.lower(), path.suffix.lower()
    if ext == "":
        ext = n  # Replace ext with n if ext empty
    if ext.startswith("."):
        ext = ext[1:]  # Remove leading period

    if path.is_symlink():
        fmtkey = "link"
        icokey = "link"
    elif path.is_mount():
        fmtkey = "mount"
        icokey = "mount"
    elif path.is_dir():
        fmtkey = "dir"
        icokey = "dir"
    elif path.is_file():
        fmtkey = "file"
        icokey = "file"
        if filemode(os.stat(path).st_mode)[3] == "x":
            fmtkey = "exec"
            icokey = "exec"
    else:
        fmtkey = "none"

    if n.startswith("."):
        fmtkey = "hidden"

    if (
        fmtkey in ["hidden", "file", "exec"]
        and ext in ALIAS
        and ALIAS[ext] in ICONS
    ):
        if ALIAS[ext] in COLOR:
            fmtkey = ALIAS[ext]
        icokey = ALIAS[ext]

    if (
        fmtkey in ["hidden", "dir"]
        and ext in ALIAS
        and f"{ALIAS[ext]}_dir" in ICONS
    ):
        icokey = f"{ALIAS[ext]}_dir"

    return fmtkey.lower(), icokey.lower()


def print_tree_listing(
    path,
    level=0,
    inode=False,
    suff=False,
    format_override=None,
    display_icons=True,
):
    tree_str = "   |   " * level + "   " + "---"
    print(tree_str, end="")
    print_short_listing(
        path,
        inode=inode,
        expand=True,
        suff=suff,
        format_override=format_override,
        display_icons=display_icons,
        end="\n",
    )


def print_long_listing(
    path,
    is_numeric=False,
    use_si=False,
    inode=False,
    timefmt=None,
    suff=False,
    format_override=None,
    display_icons=True,
):
    try:
        st = path.stat()
        size = st.st_size
        sz = get_human_readable_size(
            size, SI_MULTIPLE if use_si else METRIC_MULTIPLE
        )
        mtime = time.localtime(st.st_mtime)
        if timefmt:
            mtime = time.strftime(timefmt, mtime)
        else:
            mtime = time.strftime(
                f"%b %d {'%H:%M' if time.strftime('%Y') == time.strftime('%Y', mtime) else ' %Y'}",
                mtime,
            )
        mode = os.path.stat.filemode(st.st_mode)
        ug_string = ""
        if UID_SUPPORT:
            uid = (
                getpwuid(st.st_uid).pw_name
                if not is_numeric
                else str(st.st_uid)
            )
            gid = (
                getgrgid(st.st_gid).gr_name
                if not is_numeric
                else str(st.st_gid)
            )
            ug_string = f"{uid:4} {gid:4}"
        hln = st.st_nlink

        ino = f"{path.stat().st_ino: 10d} " if inode else ""

        print(f"{ino}{mode} {hln:3} {ug_string} {sz} {mtime} ", end="")
        print_short_listing(
            path,
            expand=True,
            suff=suff,
            format_override=format_override,
            display_icons=display_icons,
            end="\n",
        )
    except FileNotFoundError:
        ...


def print_short_listing(
    path,
    inode=False,
    expand=False,
    suff=False,
    format_override=None,
    sep_len=None,
    display_icons=True,
    end="",
):
    fmt, ico = format_override if format_override else get_keys(path)
    name = path.name + (SUFFIX.get(fmt, "") if suff else "")
    ino = f"{path.stat().st_ino: 10d}" if inode else ""
    sep_len = sep_len if sep_len else len(name)
    icon_str = f" {ICONS.get(ico, '')}  " if display_icons else ""
    if expand and path.is_symlink():
        name += " -> " + str(path.resolve())
    print(f"{ino}\x1b[{COLOR[fmt]}m{icon_str}{name:<{sep_len}}\x1b[0m", end=end)


def _get_entries(directory, args):
    contents = list()
    try:
        p = Path(directory)
        if not p.exists():
            print(f"lx: {p}: No such file or directory")
            sys.exit(1)
        if p.is_dir():
            contents = list(p.iterdir())
        elif p.is_file():
            contents = [p]
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    remove_list = list()
    if args.ignore:
        remove_list += list(p.glob(args.ignore))
    if not args.all:
        remove_list += list(p.glob(".*"))
    if args.ignore_backups:
        remove_list += list(p.glob("*~"))
    contents = [c for c in contents if c not in remove_list]

    entries = contents
    if args.reverse:
        entries = sorted(contents, reverse=True)
    elif not args.unsorted:
        entries = sorted(contents, reverse=False)

    if args.directory:
        entries = [x for x in contents if x.is_dir()]
    elif args.file:
        entries = [x for x in contents if x.is_file()]
    elif args.sd:
        entries = [x for x in contents if x.is_dir()]
        entries += [x for x in contents if x.is_file()]
    elif args.sf:
        entries = [x for x in contents if x.is_file()]
        entries += [x for x in contents if x.is_dir()]

    return entries


def process_dir(directory, args, level=0, size=None):
    end = "\n" if vars(args)["1"] else ""

    # get entries for directory. If empty exit
    entries = _get_entries(directory, args)
    if not entries:
        return
    num_entries = len(entries)

    if args.header and level == 0:
        p = Path(directory)
        # We know p exists since _get_entries would have failed if it did not
        print_short_listing(
            p.absolute(),
            inode=args.inode,
            format_override=("this", "this"),
            display_icons=args.x,
            end=":\n",
        )

    # to ensure no overlap Additional padding of 3 added to length for better
    # differentiation between entries (aesthetic choice)
    longest = max([len(str(x.name)) for x in entries]) + 3
    # Additional padding when calculating number of entries
    # Padding of 4 to account for icons as used in print_short_listing
    # (<space><icon><space><space>) Padding of 11 to account for inode
    # printing (<inode aligned to 10 units><space>)
    # If size of terminal or size of file list can not determined, default
    # to one item per line
    max_items = (
        0
        if not size
        else size[0]
        // (longest + (4 if args.x else 0) + (11 if args.inode else 0))
    )

    run = 0
    subdirs = []
    for i, path in enumerate(entries):
        if path.is_dir():
            subdirs.append(path)
        if args.long or args.numeric_uid_gid:
            print_long_listing(
                path,
                is_numeric=args.numeric_uid_gid,
                use_si=args.si,
                inode=args.inode,
                suff=args.classify,
                display_icons=args.x,
            )
        elif args.tree and args.tree > 0:
            print_tree_listing(
                path,
                level=level,
                inode=args.inode,
                suff=args.classify,
                display_icons=args.x,
            )
            if path.is_dir() and level < args.tree - 1:
                process_dir(path, args, level=level + 1, size=size)
        else:
            print_short_listing(
                path,
                inode=args.inode,
                sep_len=longest,
                suff=args.classify,
                display_icons=args.x,
                end=end,
            )
            run += 1
            if run >= max_items or i == num_entries - 1:
                print()
                run = 0

    if args.recursive and not args.tree:
        for sub in subdirs:
            print()
            if not args.header:
                print_short_listing(
                    sub.absolute(),
                    inode=args.inode,
                    format_override=("this", "this"),
                    display_icons=args.x,
                    end=":\n",
                )
            process_dir(sub, args, size=size)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Pure Python implementation of `ls` command. "
            "Only a subset of available arguments are implemented"
        ),
        epilog=(
            "Feature Requests/Bugs should be reported at "
            "https://gitlab.com/compilation-error/colorls/-/issues"
        ),
    )

    parser.add_argument(
        "-1",
        action="store_true",
        default=False,
        help="list items on individual lines",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        default=False,
        help="do not ignore entries starting with .",
    )
    parser.add_argument(
        "-B",
        "--ignore-backups",
        action="store_true",
        default=False,
        help="do not list implied entries ending with ~",
    )
    parser.add_argument(
        "-d",
        "--directory",
        action="store_true",
        default=False,
        help="list directories themselves, not their contents",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store_true",
        default=False,
        help="list files only, not directories",
    )
    parser.add_argument(
        "--sd",
        "--sort-directories",
        action="store_true",
        default=False,
        help="list directories first",
    )
    parser.add_argument(
        "--sf",
        "--sort-files",
        action="store_true",
        default=False,
        help="list files first",
    )
    parser.add_argument(
        "-F",
        "--classify",
        action="store_true",
        default=False,
        help="append indicator (one of */=>@|) to entries",
    )
    parser.add_argument(
        "-i",
        "--inode",
        action="store_true",
        default=False,
        help="display inode number",
    )
    parser.add_argument(
        "-I",
        "--ignore",
        metavar="PATTERN",
        help="do not list implied entries matching shell PATTERN",
    )
    parser.add_argument(
        "-l",
        "--long",
        action="store_true",
        default=False,
        help="use a long listing format",
    )
    parser.add_argument(
        "-n",
        "--numeric-uid-gid",
        action="store_true",
        default=False,
        help="like -l, but list numeric user and group IDs",
    )
    parser.add_argument(
        "-R",
        "--recursive",
        action="store_true",
        default=False,
        help="list subdirectories recursively",
    )
    parser.add_argument(
        "-t",
        "--tree",
        metavar="DEPTH",
        type=int,
        nargs="?",
        const=3,
        help="max tree depth",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        default=False,
        help="display current version number and exit",
    )
    parser.add_argument(
        "--si",
        action="store_true",
        default=False,
        help="display file size in SI units",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        default=False,
        help="reverse sorting order",
    )
    parser.add_argument(
        "-U",
        "--unsorted",
        action="store_true",
        default=False,
        help="do not sort; list entries in directory order. --reverse supercedes this.",
    )
    parser.add_argument(
        "-H",
        "--header",
        action="store_true",
        default=False,
        help="do not display header",
    )
    parser.add_argument(
        "-x", action="store_false", default=True, help="do not display icons"
    )
    parser.add_argument(
        "--dump-config",
        action="store_true",
        default=False,
        help="dump default config to file `colorls.toml`",
    )
    parser.add_argument(
        "FILE",
        default=".",
        nargs=argparse.REMAINDER,
        help="List information about the FILE(s).",
    )
    args = parser.parse_args()

    if args is None:
        sys.exit(2)

    if args.version:
        from . import __version__

        print("color-ls version " + __version__)
        sys.exit(0)

    if args.dump_config:
        filepath = "./colorls.toml"
        write_config(Path(filepath))
        print(
            "Copy `colorls.toml` to `~/.colorls.toml` or `~/.config/colorls/colorls.toml`"
        )
        sys.exit(0)

    if not args.FILE:
        args.FILE = ["."]

    if len(args.FILE) > 1:
        args.header = True

    term_size = shutil.get_terminal_size()
    for FILE in args.FILE:
        process_dir(FILE, args, size=term_size)

    return 0


if __name__ == "__main__":
    sys.exit(main())


# vim: ts=4 sts=4 sw=4 et syntax=python:
