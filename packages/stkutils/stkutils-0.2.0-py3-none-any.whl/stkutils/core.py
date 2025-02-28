import os
import re
from pathlib import Path

from stkutils import convert, perl_utils
from stkutils.all_spawn import all_spawn
from stkutils.binary_data import unpack
from stkutils.chunked import chunked
from stkutils.conf import BaseConfig, CommonOptions
from stkutils.file.entity import entity
from stkutils.file.graph import graph
from stkutils.gg_version import gg_version
from stkutils.ini_file import ini_file
from stkutils.perl_utils import fail, substr
from stkutils.scan_test import scan


class main:
    spawn: all_spawn
    _config: BaseConfig
    common: CommonOptions

    def __init__(self, config: BaseConfig) -> None:
        self._config = config
        self.common = self._config.common
        # creating all_spawn object
        self.spawn = all_spawn()
        # parsing command line to obtain launch keys
        self.spawn.config = self._config

    def main(self):
        cwd = os.getcwd()
        if self.bin_input() and self.common.level_spawn is None:
            self.check_spawn_version()

        # scanning config folder to obtain section-class correspondence
        if (
            self.common.scan_dir
            and (os.path.exists(self.common.scan_dir))
            and not self.is_alredy_scanned()
        ):
            # idx;
            # temp;
            if self.spawn.mode() == "decompile":
                temp = all_spawn()
                fh = chunked(self.common.src, "r")  # or fail("common.src: $!\n");
                if self.common.level_spawn is not None and (
                    self.spawn.get_version() > 115
                ):
                    temp.read_service_chunk(fh)
                idx = temp.idx_file

            if os.path.is_directory(self.common.scan_dir):
                scan.launch(self.common.scan_dir, idx)
            else:
                fail("cannot open " + self.common.scan_dir)

        # set up flags
        if self.common.level_spawn is not None:
            self.spawn.set_flag(entity.FL_LEVEL_SPAWN)
        if self.common.nofatal:
            self.spawn.set_flag(entity.FL_NO_FATAL)

        # go to proper mode

        if self.spawn.mode() == "decompile":
            self.decompile()
        elif self.spawn.mode() == "compile":
            self.compile()
        elif self.spawn.mode() == "convert":
            self.convert()
        elif self.spawn.mode() == "split":
            self.splitting()
        elif self.spawn.mode() == "parse":
            self.parse()
        elif self.spawn.mode() == "compare":
            self.compare()
        elif self.spawn.mode() == "update":
            self.update()
        else:
            raise ValueError

        print("done!\n")

        if self.with_scan():
            if (
                self.spawn.get_version() == 118
                and self.spawn.get_script_version() >= 5
                and (self._config.mode not in {"compile", "parse", "compare"})
            ):
                self.refresh_sections()
            elif self.common.sections_ini:
                self.common.sections_ini.close()

        if self.common.user_ini:
            self.common.user_ini.close()  # if -e 'user_sections.ini';
        if self.common.prefixes_ini:
            self.common.prefixes_ini.close()  # if -e 'way_prefixes.ini';
        os.chdir(cwd)

    def decompile(self):
        # 	check_spawn_version();
        print("opening common.src...\n")
        # unlink 'guids.ltx';
        self.spawn.read()
        if self.spawn.graph_data is None and self.common.level_spawn is None:
            self.read_graph()
        self.create_outdir(self.common.out)
        print("exporting alife objects...\n")
        self.spawn.export("all.ltx")

    def compile(self):
        cwd = os.getcwd()
        # handles flags of sections (i.e. [4569]: f1)
        if self._config.compile.flags is not None:
            for flag in perl_utils.split(","):
                if not re.match(r"\s*(\w+)\s*", flag):
                    fail(
                        f"bad flag '{flag}'\n",
                    )  # unless  re.match("\s*(\w+)\s*", $flag);
                self._config.compile.flags_hash[flag] = 1

        # 	read_graph() if (!defined spawn.graph_data and !defined common.level_spawn);
        if self.common.src != "":
            if not os.path.exists(self.common.src):
                fail("cannot change dir to " + self.common.src)
        os.chdir(self.common.src)
        if not self.common.out:
            self.common.out = "all.spawn.new"  # unless defined
        print("importing alife objects...\n")
        self.spawn.import_()
        # check story ids
        self.check_story_ids()
        print("writing common.src...\n")
        # chdir $wd or fail('cannot change path to '.$wd);
        os.chdir(cwd)
        self.spawn.write()

    def convert(self, *args, **kwargs):
        # check existance of proper keys
        if not os.path.exists(convert.convert.new_version):
            fail("define new spawn version for converting spawn")  # unless exists ;
        if substr(self.common.src, -5) == "spawn":
            # 		check_spawn_version();
            print("opening common.src...\n")
            # unlink 'guids.ltx';
            self.spawn.read()

            if self.spawn.graph_data is None:
                self.read_graph()
            self.common.out = self.common.src + ".converted"
            self.process_converting()
            self.spawn.write()
        elif substr(self.common.src, -3) == "ltx":
            if self.common.out is None:
                self.common.out = "converted"  # unless defined ;
            print("importing alife objects...\n")
            self.spawn.import_level(self.spawn.get_src())
            # 		fix_versions();
            self.process_converting()
            print("exporting alife objects...\n")
            self.spawn.export_level(self.spawn.get_out())
        else:
            fail(
                "Trouble with spawn converting: cant recognize type of file - text or binary",
            )

    def splitting(self, *args, **kwargs):
        # check existance of proper keys
        if not os.path.exists(self.common.out):
            Path(self.common.out).mkdir(parents=True)
            # self.common.out = 'levels'  # unless exists ;
        # 	check_spawn_version();
        print("opening common.src...\n")
        # unlink 'guids.ltx';
        self.spawn.read()
        if self.spawn.graph_data is None:
            self.read_graph()  # if !defined

        if self.spawn.use_graph():
            self.create_outdir(self.common.out)
            self.spawn.graph.read_edges()
            self.spawn.prepare_graph_points()
            self.prepare_level_folders(self.spawn.graph)
        else:
            # chdir  or fail('you must define levels folder using -out');
            self.spawn.read_level_spawns()

        self.spawn.write_splitted_spawns()
        if self.spawn.way():
            self.spawn.split_ways()  # if ;

    def parse(self, *args, **kwargs):
        # check existance of proper keys
        if (self._config.parse.old_gvid) is None:
            fail("define old gvid0 for spawn parsing")  # unless exists
        if (self._config.parse.new_gvid) is None:
            fail("define new gvid0 for spawn parsing")  # unless exists ;
        print("parsing common.src...\n")
        self.spawn.import_level(self.spawn.get_src())
        if not self.common.out:
            self.common.out = "parsed_spawn"  # unless defined common.out;
        self.create_outdir(self.common.out)
        # 	fix_versions();
        for object in self.spawn.alife_objects:
            object.cse_object.game_vertex_id += (
                self.spawn.get_new_gvid() - self.spawn.get_old_gvid()
            )

        print("exporting common.out...\n")
        out = perl_utils.split(r"\/", self.spawn.get_src())
        self.spawn.export_level(out[len(out) - 1])
        if self.spawn.way() == 1:
            self.spawn.parse_way(out[len(out) - 1])

    def compare(self, *args, **kwargs):
        # check existance of proper keys
        # if not os.path.exists(self._config.common.src):
        #     fail("type files to compare")  # unless exists ;
        files = perl_utils.split(",", self._config.common.src)
        if len(files) == 1:
            fail("there are must be two files")  # unless $#files == 1;
        print(f"parsing {files[0]}...\n")
        self.spawn.config = self._config
        self.spawn.import_level(files[0])
        # creating new all_spawn object
        spawn_new = all_spawn()
        print(f"parsing {files[1]}...\n")
        spawn_new.config = self._config
        spawn_new.import_level(files[1])
        for object_n in spawn_new.alife_objects:
            is_founded = 0
            for object in self.spawn.alife_objects:
                if (object_n.cse_object.name != object.cse_object.name) or (
                    object_n.cse_object.section_name != object.cse_object.section_name
                ):
                    continue
                is_founded = 1
                break
            # print(f"checking {object_n.cse_object.name}, found={is_founded}")
            if is_founded == 1:
                continue
            self.spawn.alife_objects.append(object_n)

        to_delete: list[int] = []
        i = 0
        for object in self.spawn.alife_objects:
            is_founded = 0
            for object_n in spawn_new.alife_objects:
                if (object_n.cse_object.name != object.cse_object.name) or (
                    object_n.cse_object.section_name != object.cse_object.section_name
                ):
                    continue
                is_founded = 1
                break
            # print(f"checking {object.cse_object.name}, found={is_founded}")
            if is_founded == 0:
                to_delete.append(i)
            i += 1

        for idx in to_delete:
            self.spawn.alife_objects[idx] = None

        self.spawn.export_level(self._config.common.out)

    def update(self, *args, **kwargs):
        # 	check_spawn_version();
        print("opening common.src...\n")
        # unlink 'guids.ltx';
        self.spawn.read()

        if self.spawn.graph_data is None and self.common.level_spawn is None:
            self.read_graph()
        out = open("all_spawn.ltx", "w", encoding="cp1251")
        print("exporting alife objects...\n")
        # print $out ;
        out.write("[objects]\n")
        i = 0
        for obj in self.spawn.alife_objects:
            # 		ref = ref($obj.cse_object);
            # 		if (
            # 			($ref == 'cse_alife_object_hanging_lamp') or
            # 			($ref == 'cse_alife_object_breakable') or
            # 			($ref == 'cse_alife_object_climable') or
            # 			($ref == 'cse_alife_object_physic') or
            # 			($ref == 'cse_alife_object_projector')) {
            # 			++$i;
            # 			next;
            # 		}
            # 		temp
            level_name = self.spawn.graph.level_name(obj.cse_object.game_vertex_id)
            if (level_name == "_level_unknown") and (
                obj.cse_object.name == "secret_af_vyvert"
            ):
                level_name = "l03_agroprom"

            out.write(
                f"{i}"
                + f"_{obj.cse_object.name} = "
                + level_name
                + " "
                + ",".join(obj.cse_object.position)
                + f",{i}\n",
            )
            i += 1

        print("exporting way objects...\n")
        # print $out ;
        out.write("[ways]\n")
        i = 0
        prefixes = self.spawn.init_way_prefixes()
        for obj in self.spawn.way_objects:

            p = 0
            level_name = self.spawn.get_level_name(obj, prefixes)
            for point in obj.points:
                pname = point.name
                if re.match(r"^(\w+)\|/", pname):  # pname =~ /):
                    pname = 1

                out.write(
                    f"{i}"
                    + f"_{p}"
                    + f"_{obj.name}"
                    + f"_{pname} = "
                    + level_name
                    + " "
                    + ",".join(point.position)
                    + f",{i},{p}\n",
                )
                p += 1

            i += 1

        out.close()

        print("calling vertex.exe...\n")
        res = "vertex all_spawn.ltx"
        print("control was returned\n")

        ini = ini_file("all_spawn.ltx.processed", "r")
        # fail("can't open all_spawn.ltx.processed") if !defined $ini;
        print("updating alife objects...\n")
        for _str in ini.sections_hash["objects"].values():

            if re_match := re.match(
                r"^(\w+),([+-]?\d+),(\w+),(.+)",
                _str,
            ):  # re.match("", _str)):
                (rm1, rm2, rm3, rm4) = re_match
                gvid = rm1
                # 			print("$1, $2, $3\n")
                if gvid != 65535:
                    self.spawn.alife_objects[rm3].cse_object.game_vertex_id = gvid
                    self.spawn.alife_objects[rm3].cse_object.level_vertex_id = rm2
                    self.spawn.alife_objects[rm3].cse_object.distance = rm3

            else:
                fail("template mismatch")

        print("updating way objects...\n")
        for _str in ini.sections_hash["ways"].values():

            if re_match := re.match(r"^(\w+),([+-]?\d+),(\w+),(\w+)", str):
                (rm1, rm2, rm3, rm4) = re_match
                gvid = rm1
                if gvid != 65535:
                    self.spawn.way_objects[rm3].points[rm4].game_vertex_id = gvid
                    self.spawn.way_objects[rm3].points[rm4].level_vertex_id = rm2

            else:
                fail("template mismatch")

        ini.close()
        if self.common.out is None:
            self.common.out = (
                self.common.src + ".processed"
            )  # unless defined common.out;
        self.spawn.write(1)

    # 	unlink 'all_spawn.ltx';
    # 	unlink 'all_spawn.ltx.processed';
    # }

    # service subs
    def is_alredy_scanned(*args, **kwargs):
        if os.path.exists("sections.ini"):
            size = os.path.getsize("sections.ini")
            return size > 0

        return 0

    def check_spawn_version(self):
        filepath = self.common.src
        print(f"checking version of {filepath}...\n")

        is_level = False
        with open(filepath, "rb") as fh:
            data = fh.read(0x12C)

            if is_level:
                (
                    garb_1,
                    section_name,
                    name,
                    garb_2,
                    version,
                    script_version,
                    backup,
                ) = unpack("a[10]Z*Z*a[36]vvv", data)
            else:
                switch, header_size = unpack("VV", data)
                if switch == 0:
                    if header_size == 0x2C:
                        format_str = "a[118]Z*Z*a[36]vvv"
                    else:
                        format_str = "a[76]Z*Z*a[36]vvv"
                    (
                        garb_1,
                        section_name,
                        name,
                        garb_2,
                        version,
                        script_version,
                        backup,
                    ) = unpack(format_str, data)
                else:
                    format_str = "a[32]Z*Z*a[36]vv"
                    (garb_1, section_name, name, garb_2, version, script_version) = (
                        unpack(format_str, data)
                    )

            if script_version == 0xFFFF:
                script_version = backup
            if version <= 0x45:
                script_version = 0

            build = (
                gg_version().build_by_version(version, script_version)
                or "unknown,  spawn ver. " + version
            )
            print(build)

            if version == 118 and script_version == 6:
                fh = chunked(filepath, "r")
                if fh.find_chunk(0x4):
                    print("	This is a spawn of S.T.A.L.K.E.R. xrCore build 3120\n")
                    fh.close_found_chunk()
                else:
                    print(f"	This is a spawn of S.T.A.L.K.E.R. {build}\n")

                fh.close()
            else:
                print(f"	This is a spawn of S.T.A.L.K.E.R. {build}\n")

            self.spawn.set_version(version)
            self.spawn.set_script_version(script_version)

    def prepare_level_folders(self, graph):
        print("preparing level folders...\n")
        for level in graph.level_by_guid.values():
            if not os.path.exists(level):
                os.mkdir(level)
        # File.Path.mkpath($level, 0);

    def create_outdir(self, fpath: str | None = None):
        path = Path(fpath) if fpath is not None else None
        if path is not None:
            if not path.exists():
                path.mkdir(parents=True)
            os.chdir(path)
        # File.Path.mkpath(args[0], 0);
        # chdir args[0] or fail('cannot change path to '.args[0]);

    def with_scan(self, *args, **kwargs):
        return (self.common.scan_dir is not None) or (os.path.exists("sections.ini"))

    def process_converting(self, *args, **kwargs):
        print("converting spawn...\n")
        self.spawn.prepare_objects()
        for object in self.spawn.alife_objects:
            if object is None:
                continue
            # next unless defined object;
            object.cse_object.version = convert.convert.new_version
            object.cse_object.script_version = gg_version.scr_ver_by_version(
                convert.convert.new_version,
            )
            sName = perl_utils.lc(object.cse_object.section_name)
            class_name = None
            if object.cse_object.ini is not None:
                class_name = object.cse_object.ini.value("sections", f"'{sName}'")
            if not class_name:
                class_name = scan.get_class(sName)
            if not class_name:
                fail("unknown class for section " + object.cse_object.section_name)
            # bless object.cse_object, $class_name;
            if not hasattr(object.cse_object, "state_read"):
                fail(
                    "unknown clsid "
                    + class_name
                    + " for section ".object.cse_object.section_name,
                )
            # handle SCRPTZN
            if object.cse_object.version > 124:
                if sName == "sim_faction":
                    # bless object.cse_object, 'se_sim_faction'
                    pass

            # handle wrong classes for weapon in ver 118
            if (
                object.cse_object.version == 118
                and object.cse_object.script_version > 5
            ):
                # soc
                if re.match("ak74u|vintore", sName):
                    # bless object.cse_object, 'cse_alife_item_weapon_magazined'
                    pass
            if not hasattr(object.cse_object, "state_import"):
                fail(
                    "unknown clsid "
                    + class_name
                    + " for section "
                    + object.cse_object.section_name,
                )
            object.init_abstract()
            object.init_object()

        self.spawn.print_harm_objects()  # if $#{spawn.harm_objects} != -1;
        self.spawn.print_excluded_objects()  # if $#{spawn.excluded_objects} != -1;

    def read_graph(self, *args, **kwargs):
        # graph_file;
        if self.spawn.graph_dir() is not None:
            graph_file = open(
                os.path.join(self.spawn.graph_dir(), "game.graph"),
                "rb",
            )
        else:
            graph_file = open("game.graph", "rb")  # or fail("game.graph: $!\n");

        # binmode $graph_file;
        graph_data = ""
        graph_data = graph_file.read()
        graph_file.close()
        self.spawn.graph_data = graph_data
        self.spawn.graph = graph(graph_data)
        self.spawn.graph.gg_version = gg_version().graph_build(
            self.spawn.get_version(),
            self.spawn.get_script_version(),
        )
        self.spawn.graph.decompose()
        self.spawn.graph.read_vertices()
        self.spawn.graph.show_guids("guids.ltx")

    def check_story_ids(self, *args, **kwargs):
        control_hash = perl_utils.universal_dict_object()
        for obj in self.spawn.alife_objects:

            sid = obj.cse_object.story_id
            if sid in control_hash and (sid != -1):
                fail(
                    f"object {obj.cse_object.name} has same story id as "
                    + control_hash[sid]
                    + f" ({sid})",
                )
            control_hash[sid] = obj.cse_object.name

    def is_flag_defined(self, *args, **kwargs):
        return (self._config.compile.flags_hash[args[0]]) is not None

    def bin_input(self, *args, **kwargs) -> bool:
        mode = self.spawn.mode()
        bin_mode_input_commands = {
            "decompile",
            "split",
            "update",
        }
        if mode in bin_mode_input_commands:
            return True

        return (mode == "convert") and (substr(self.common.src, -3) != "ltx")

    def refresh_sections(self, *args, **kwargs):
        ini_new = open("sections.new.ini", "w")  # or fail("sections.new.ini: $!\n")
        ini_new.write("[sections]\n")
        for section in (
            sorted(
                self.common.sections_ini.sections_hash["sections"].keys(),
                key=lambda k: self.common.sections_ini.sections_hash["sections"][k],
            )
            # sort {common.sections_ini.sections_hash{'sections'}{$a} cmp common.sections_ini.sections_hash{'sections'}{$b}} keys %{common.sections_ini.sections_hash{'sections'}}
        ):
            ini_new.write(
                f"{section} = common.sections_ini.sections_hash{'sections'}{section}\n",
            )

        ini_new.close()
        ini.close()
