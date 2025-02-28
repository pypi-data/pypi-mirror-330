# Module providing some useful methods
# Update history:
# 	27/08/2012 - fix read_file() and write_file() for binmode
# 	26/08/2012 - fix for new fail() syntax, merging with filehandler.pm, add get_includes()
#############################################
# package stkutils::utils;
# use strict;
# use stkutils::debug qw(fail);
# use IO::File;
# use vars qw(@ISA @EXPORT_OK);
# require Exporter;
#
# @ISA		= qw(Exporter);
# @EXPORT_OK	= qw(get_filelist get_includes read_file write_file get_path get_all_includes);
import re

from stkutils.perl_utils import is_dir, is_file, join, split


def read_file(fn):
    fh = open(fn, "rb")  # or fail("$!: $_[0]\n");
    # binmode $fh;
    data = ""
    data = fh.read()
    fh.close()
    return data


def write_file(fn: str, data: bytes) -> None:
    fh = open(fn, "wb")  # or fail("$!: $_[0]\n");

    fh.write(data)
    fh.close()


def glob():
    pass


def get_filelist(folder: str, ext: str):
    # $_[0] - folder, $_[1] - file extensions
    ext_list: list[str] = _prepare_extensions_list(ext)
    files = []
    if folder == "":

        files = glob("*")
    else:
        # if (!(-d $_[0])) {fail("not a folder\n")};
        files = glob("$_[0]/*")

    out = []
    for file in files:
        if is_dir(file):
            temp = get_filelist(file, ext)
            out.append(temp)
        elif is_file(file) and _has_desired_extension(file, ext_list):
            out.append(file)

    return out


def _prepare_extensions_list(ext_lst: str) -> list[str]:
    return split(",", ext_lst)


def _has_desired_extension(arg0, *args):
    if not args:
        return 1
    for ext in args:
        if re.match("$ext$") or (ext == ""):
            return 1

    return 0


def get_all_includes(arg1: str, arg2: str) -> list[list[str]]:
    out = []
    base = arg2
    if arg1 != "":
        base = arg1 + "\\" + base
    list_ = get_includes(base)
    for f in list_:
        if re.match("^mp\\/|^mp\\", f):
            continue
        (path, file) = get_path(f)
        # 		print "$_[0]\\$path\\$file\n";
        in_l = get_all_includes(arg1 + "\\" + path, file)
        in_l = [path + "\\" + l for l in (in_l)]

        out.append(in_l)

    out.append(list_)
    return out


def get_includes(fn: str) -> list[str]:
    with open(fn, encoding="cp1251") as file:  # or return undef;
        inc = [line for line in file if (re.match('^(?<!;)#include "(.*)"', line))]

    return inc


def get_path(p: str) -> tuple[list[str], str]:
    temp = split("\\", p)
    temp = temp.pop()
    return join("/", temp), temp


##############################
