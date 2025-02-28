import os
from enum import Enum

from stkutils.ini_file import ini_file


class CompileConfig:
    flags: str
    idx_file: str


class SplitConfig:
    use_graph: bool


class ConvertConfig:
    new_version: str
    ini: str


class ParseConfig:
    old_gvid: str
    new_gvid: str


class CommonOptions:
    src: str
    out: str
    af: str
    way: str
    scan_dir: str
    graph_dir: str
    level_spawn: str
    nofatal: str
    sort: str
    log: str

    sections_ini: ini_file | None
    user_ini: ini_file | None
    prefixes_ini: ini_file | None


class Mode(str, Enum):
    DECOMPILE = "decompile"
    COMPILE = "compile"
    CONVERT = "convert"
    SPLIT = "split"
    PARSE = "parse"
    COMPARE = "compare"
    UPDATE = "update"


class BaseConfig:
    mode: Mode
    common: CommonOptions
    compile: CompileConfig
    split: SplitConfig
    convert: ConvertConfig
    parse: ParseConfig

    def set_mode(self, mode: str) -> None:
        self.mode = Mode[mode]

    def with_scan(self, *args, **kwargs):
        return (self.common.scan_dir is not None) or (os.path.exists("sections.ini"))
