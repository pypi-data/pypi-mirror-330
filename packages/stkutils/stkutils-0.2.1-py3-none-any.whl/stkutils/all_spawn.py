import re
from pathlib import Path

from stkutils.binary_data import pack, unpack
from stkutils.chunked import chunked
from stkutils.conf import BaseConfig, Mode
from stkutils.convert import convert
from stkutils.data_packet import data_packet
from stkutils.file.entity import *
from stkutils.file.graph import graph
from stkutils.gg_version import gg_version
from stkutils.ini_file import ini_file
from stkutils.level.level_game import level_game
from stkutils.level.level_gct import level_gct
from stkutils.perl_utils import bless, fail, split, universal_dict_object

FL_LEVEL_SPAWN = 0x01
FL_IS_3120 = 0x02
FL_IS_2942 = 0x04
FL_IS_25XX = 0x08
FL_NO_FATAL = 0x10

FULL_IMPORT = 0x0
NO_VERTEX_IMPORT = 0x1


class all_spawn:
    alife_objects: list[entity]
    way_objects: list[level_game]
    level_spawns: "list[all_spawn]"
    unknown = None
    config: BaseConfig

    def __init__(self):
        self.spawn_version = 0
        self.script_version = 0
        # self.config = universal_dict_object()
        self.flags = 0
        self.graph_data = None
        self.alife_objects = []
        self.way_objects = []
        self.level_spawns = []

    def set_version(self, v):
        self.spawn_version = v

    def get_version(self):
        return self.spawn_version

    def set_script_version(self, script_version) -> None:
        self.script_version = script_version

    def get_script_version(self):
        return self.script_version

    def get_config(self) -> BaseConfig:
        return self.config

    def mode(self) -> Mode:
        return self.config.mode

    def idx(self):
        return self.config.compile.idx_file

    def use_graph(self) -> bool:
        return self.config.split and self.config.split.use_graph is not None

    def way(self) -> bool:
        return self.config.common.way is not None  # and self.config.common.way != False

    def graph_dir(self) -> str:
        return self.config.common.graph_dir

    def get_src(self) -> str:
        return self.config.common.src

    def get_out(self) -> str:
        return self.config.common.out

    def get_ini(self) -> ini_file | None:
        return self.config.common.sections_ini

    def get_user_ini(self) -> ini_file | None:
        return self.config.common.user_ini

    def get_prefixes_ini(self) -> ini_file | None:
        return self.config.common.prefixes_ini

    def set_ini(self, sections_ini) -> None:
        self.config.common.sections_ini = sections_ini

    def get_sort(self) -> str:
        return self.config.common.sort

    def get_af(self):
        return self.config.common.af

    def get_flag(self):
        return self.flags

    def set_flag(self, flag):
        self.flags |= flag

    def is_3120(self):
        if self.flags & FL_IS_3120:
            return True
        return None

    def get_new_gvid(self):
        return self.config.parse.new_gvid

    def get_old_gvid(self):
        return self.config.parse.old_gvid

    # reading
    def read(self):
        # my self = shift;
        cf = chunked(self.get_src(), "r")  # or fail(self.get_src().": !\n");
        if not self.level():
            if self.get_version() > 79:
                while 1:
                    (index, size) = cf.r_chunk_open()
                    if index is None:
                        break
                    # defined(index) or last;
                    if index == 0:
                        self.read_header(cf)
                    elif index == 1:
                        self.read_alife(cf)
                    elif index == 2:
                        self.read_af_spawn(cf)
                    elif index == 3:
                        self.read_way(cf)
                    elif index == 4:
                        self.read_graph(cf.r_chunk_data())
                    elif index != 5:
                        raise ValueError("unexpected chunk index " + str(index))

                    cf.r_chunk_close()

            else:
                # my count;
                (index, size) = cf.r_chunk_open()
                self.read_header(cf)
                cf.r_chunk_close()
                self.read_alife(cf)
                if self.get_version() > 16:
                    (count, size) = cf.r_chunk_open()
                    self.read_af_spawn(cf)
                    cf.r_chunk_close()

        else:
            self.read_alife(cf)

        cf.close()

    def read_header(self, cf: chunked):
        # my self = shift;
        # my (cf) = @_;
        print("reading header...\n")
        if self.get_version() > 94:
            (
                self.graph_version,
                self.guid,
                self.graph_guid,
                self.count,
                self.level_count,
            ) = unpack("Va[16]a[16]VV", cf.r_chunk_data())
        else:
            (
                self.graph_version,
                self.count,
                self.unknown,
            ) = unpack("VVV", cf.r_chunk_data())

    def read_alife(self, cf: chunked):
        # my self = shift;
        # my (cf) = @_;
        i = 0
        print("reading alife objects...\n")
        if self.get_version() > 79 and not self.level():
            while 1:
                (index, size) = cf.r_chunk_open()
                if index is None:
                    break
                if index == 0:
                    if size != 4:
                        fail("unexpected alife objects count size")
                    (alife_count,) = unpack("V", cf.r_chunk_data())
                    if alife_count != self.count:
                        fail("alife object count mismatch")
                elif index == 1:
                    while 1:
                        (index, size) = cf.r_chunk_open()
                        if index is None:
                            break
                        object = entity()
                        object.cse_object.flags = self.get_flag()
                        object.cse_object.ini = self.get_ini()
                        object.cse_object.user_ini = self.get_user_ini()
                        object.read(cf, self.get_version())
                        self.set_flag(
                            object.cse_object.flags & 0x9F,
                        )  # exclude entity specific flags
                        self.set_ini(object.cse_object.ini)
                        # push @{self.alife_objects}, object
                        self.alife_objects.append(object)
                        cf.r_chunk_close()

                elif index == 2:
                    self.unk_chunk = cf.r_chunk_data()

                cf.r_chunk_close()

        else:
            while 1:
                (index, size) = cf.r_chunk_open()
                if index is None:
                    break
                if self.count is not None and index >= self.count:
                    break
                # index < self.count or last if defined self.count;
                # die unless i == index;
                object = entity()
                object.cse_object.flags = self.get_flag()
                object.cse_object.ini = self.get_ini()
                object.read(cf, self.get_version())
                self.set_flag(object.cse_object.flags)
                self.set_ini(object.cse_object.ini)
                cf.r_chunk_close()
                i += 1
                if self.mode() == "split":
                    if (object.cse_object) == "cse_alife_graph_point":
                        self.alife_objects.append(object)
                # push (@{self.alife_objects}, object) if (ref(object.cse_object) eq 'cse_alife_graph_point');
                else:
                    self.alife_objects.append(object)
                # push @{self.alife_objects}, object;
        print("ALIFE READED ")

    def read_af_spawn(self, cf):
        # my self = shift;
        # my (cf) = @_;
        print("reading artefact spawn places...\n")
        self.af_spawn_data = cf.r_chunk_data()
        self.af_spawn_places = []
        if self.get_af():
            packet = data_packet(self.af_spawn_data)
            (obj_count,) = packet.unpack("V", 4)

            # while (obj_count-=1):
            for i in range(obj_count):
                afsp = universal_dict_object()
                afsp.position = packet.unpack("f3", 12)
                (afsp.level_vertex_id, afsp.distance) = packet.unpack("Vf", 8)
                # push @{self.af_spawn_places}, afsp;
                self.af_spawn_places.append(afsp)

    def read_way(self, cf):
        # my self = shift;
        # my (cf) = @_;
        print("reading way objects...\n")
        while 1:
            (index, size) = cf.r_chunk_open()
            # defined(index) or last;
            if index is None:
                break
            if index == 0:
                if size != 4:
                    fail("unexpected way objects count size")
                (way_count,) = unpack("V", cf.r_chunk_data())
            elif index == 1:
                while 1:
                    (index, size) = cf.r_chunk_open()
                    if index is None:
                        break
                    object = level_game()
                    object.read(cf)
                    # push @{self.way_objects}, object;
                    self.way_objects.append(object)
                    cf.r_chunk_close()
            else:
                fail("unexpected chunk index ".index)

            cf.r_chunk_close()

    def read_graph(self, data_ref):
        # my self = shift;
        # my (data_ref) = @_;
        self.graph_data = data_ref
        if self.get_version() == 118:
            self.set_flag(FL_IS_3120)
        self.graph = graph(self.graph_data)
        gg_version.gg_version = self.check_graph_build()
        self.graph.decompose()
        self.graph.read_vertices()
        self.graph.show_guids("guids.ltx")

    # writing
    def write(self):
        # my self = shift;
        if self.alife_objects:  # check if there is no objects
            self.set_version((self.alife_objects[0]).cse_object.version)
            self.set_script_version((self.alife_objects[0]).cse_object.script_version)

        self.graph_version = self.check_graph_version()
        cf = chunked(self.get_out(), "w")  # or fail(self.get_out().": !\n");
        if not self.level():
            self.write_header(cf)
            self.write_alife(cf)
            self.write_af_spawn(cf)
            self.write_way(cf)
            self.write_graph(cf)  # if !defined _[0];
            self.write_service_chunk(cf)
        else:
            self.write_alife(cf)

        cf.close()

    def write_header(self, cf: chunked):
        # my self = shift;
        # my (cf) = @_;
        print("writing header...\n")
        if self.get_version() > 94:
            data = pack(
                "Va[16]a[16]VV",
                self.graph_version,
                self.guid,
                self.graph_guid,
                len(self.alife_objects),
                self.level_count,
            )
            cf.w_chunk(0, data)
        else:
            data = pack(
                "VVV",
                self.graph_version,
                len(self.alife_objects),
                self.unknown,
            )
            if self.get_version() > 79:
                cf.w_chunk(0, data)
            else:
                cf.w_chunk(0xFFFF, data)

    def write_alife(self, cf: chunked):
        # my self = shift;
        # my (cf) = @_;
        print("writing alife objects...\n")
        if self.get_version() > 79 and not self.level():
            cf.w_chunk_open(1)
            cf.w_chunk(0, pack("V", len(self.alife_objects)))
            cf.w_chunk_open(1)
            id = 0
            file = self.idx()
            if file is not None and file == "":
                file = "spawn_ids"  # if (defined file && file eq '');
            if file is not None and not file.endswith("ltx"):
                file += ".ltx"  # if (defined file and (substr(file, -3) ne 'ltx'));
            log = None
            guids_file = None
            if self.idx() is not None:
                log = open(file, "w", encoding="cp1251")  # if defined self.idx();
                guids_file = ini_file("guids.ltx", "r")  # if defined self.idx();
            if self.idx() is not None and not guids_file:
                fail(
                    "guids.ltx: !\n",
                )  # if (defined self.idx() && !defined guids_file);
            for object in self.alife_objects:
                # print(f"Writing #{id} {object.cse_object.name}. Debug {cf.offset=}")
                # foreach my object (@{self.alife_objects}) {
                if not object:
                    continue
                # next unless defined object;
                # enable this if you want inventory boxes always online
                # 			if (object.cse_object.section_name eq "inventory_box") {
                # 				object.cse_object.object_flags = 0xffffff3b;
                # 			}
                class_name = object.cse_object
                cf.w_chunk_open(id)
                if self.idx() is not None:  # {
                    level_id = self.get_level_id(
                        guids_file,
                        object.cse_object.game_vertex_id,
                    )
                    # print log "\n[".level_id."_".object.cse_object.name."]\n";
                    # print log "id = id\n";
                    # print log "story_id = object.cse_object.story_id\n";
                    log.write(f"\n [{level_id}_{object.cse_object.name}]")
                    log.write(f"id={id}\n")
                    log.write(f"story_id = {object.cse_object.story_id}\n")
                # }
                object.write(cf, id)
                # cf.w_chunk_close()
                id += 1
            # }
            if self.idx() is not None:
                log.close()  # if defined self.idx();
                guids_file.close()  # if defined self.idx();
            # cf.w_chunk_close()
            chunk_2 = ""
            if self.get_version() == 85:
                chunk_2 = self.unk_chunk  # if self.get_version() == 85;
            cf.w_chunk(2, chunk_2)
            # cf.w_chunk_close()
        else:
            id = 0
            for object in self.alife_objects:
                # print(f"Writing #{id} {object.cse_object.section_name}({object.cse_object.name})")
                cf.w_chunk_open(id)
                object.write(cf, id)
                id += 1
                cf.w_chunk_close()

    def write_af_spawn(self, cf: chunked):
        # my self = shift;
        # my (cf) = @_;
        if self.get_af():
            data = b""
            for afsp in self.af_spawn_places:
                data += pack(
                    "f3Vf",
                    *afsp.position,
                    afsp.level_vertex_id,
                    afsp.distance,
                )

            # self.af_spawn_data = \data;
            self.af_spawn_data = data

        if self.af_spawn_data is not None:
            print("writing artefact spawn places...\n")
            if self.get_version() > 79:
                cf.w_chunk(2, self.af_spawn_data)
            else:
                cf.w_chunk(len(self.alife_objects) + 1, self.af_spawn_data)

    def write_way(self, cf: chunked):
        # my self = shift;
        # my (cf) = @_;
        if self.way_objects:
            print("writing way objects...\n")
            cf.w_chunk_open(3)
            cf.w_chunk(0, pack("V", len(self.way_objects)))
            cf.w_chunk_open(1)
            id_ = 0

            for object in self.way_objects:
                cf.w_chunk_open(id_)
                id_ += 1
                object.write(cf)
                cf.w_chunk_close()

            cf.w_chunk_close()
            cf.w_chunk_close()

    def write_graph(self, cf: chunked):
        # my self = shift;
        # my (cf) = @_;
        new_graph_ver = self.check_graph_build()
        print("writing graph...\n")
        if (
            getattr(self, "graph", None) is None
            or self.graph.gg_version is None
            or self.graph.gg_version == new_graph_ver
        ):
            # -compile
            if new_graph_ver != "cop":
                return
            cf.w_chunk(4, self.graph_data)
        elif self.graph.gg_version == "cop":
            # convert from cs/cop spawn, so we need to split graph
            # write cross tables
            # Path::mkpath('levels', 0);
            # my wd = getcwd();
            # chdir 'levels' or fail('cannot change path to levels');
            levels_path = Path("levels")
            for level in self.graph.level_by_guid.values():
                # Path::mkpath(level, 0);
                ctfh = open(
                    levels_path / "level.gct",
                    "w",
                    encoding="cp1251",
                )  # or fail("level/level.gct: !\n");
                ct = level_gct(self.graph.raw_cross_tables[level])
                ct.read()
                ct.set_version(self.check_graph_version())
                ct.write()
                data = ct.get_data()
                ctfh.write(data)
                ctfh.close()

            # chdir wd or fail('cannot change path to '.wd);
            gg_version.gg_version = new_graph_ver
            graph_data = self.graph.compose()
            # write graph
            fh = open("game.graph", "wb")
            # binmode fh;
            fh.write(graph_data, len(graph_data))
            fh.close()
        elif new_graph_ver == "cop":
            # convert to cs/cop spawn, so we need to form graph
            # read cross tables
            for level in self.graph.level_by_guid.values():
                ctfh = open(
                    Path("levels/") / level / "/level.gct",
                    "rb",
                )  # or fail("levels/level/level.gct: !\n");
                # binmode ctfh;
                data = ""
                ctfh.read(data, (ctfh.stat())[7])
                ctfh.close()
                ct = level_gct(data)
                ct.read()
                ct.set_version(self.check_graph_version())
                ct.write()
                self.graph.raw_cross_tables[level] = ct.get_data()

            gg_version.gg_version = "cop"
            graph_data = self.graph.compose()
            # write graph
            cf.w_chunk(4, graph_data)

    # importing
    def import_(self):
        # my self = shift;
        if not self.level():
            if_ = ini_file("all.ltx", "r")  # or fail("all.ltx: !\n");
            self.import_header(if_)
            self.import_alife(if_)
            self.set_version((self.alife_objects[0]).cse_object.version)
            self.import_af_spawn(if_)
            self.import_way(if_)
            self.import_graph(if_)
            if_.close()
        else:
            self.import_level("level_spawn.ltx")

    def import_header(self, if_):
        # my self = shift;
        # my (if) = @_;

        self.graph_version = if_.value("header", "graph_version")
        if (guid := if_.value("header", "guid")) is not None:
            self.guid = pack("H*", guid)  # if defined
        if (graph_guid := if_.value("header", "graph_guid")) is not None:
            self.graph_guid = pack("H*", graph_guid)  # if defined
        self.level_count = int(if_.value("header", "level_count"))
        self.unknown = if_.value("header", "unknown")
        if if_.value("header", "flags") is not None:
            self.flags = if_.value("header", "flags")

    def import_alife(self, if_):
        # my self = shift;
        # my (if) = @_;
        # unlink 'spawn_ids.log' if -e 'spawn_ids.log';
        id = 0
        if self.idx() is not None:
            idx_log = open(
                "spawn_ids.log",
                "w",
                encoding="cp1251",
            )  # if !defined self.idx();
        actor_flag = 0
        version = 0
        script_version = 0
        source_file = if_.value("alife", "source_files")
        for fn in split(",", source_file):
            # fn =~ s/^\s*|\s*//g;
            # some_re = r"s/^\s*|\s*//g"
            fn = fn.strip()

            lif = None
            if fn == r"alife_debug\y_selo.ltx":
                lif = ini_file(
                    "alife_debug_y_selo.ltx",
                    "r",
                )  # or fail("alife_debug_y_selo.ltx: !\n")
            else:
                lif = ini_file(fn, "r")  # or fail("fn: !\n")

            print(f"importing alife objects from file {fn}...\n")
            for section in lif.sections_list:
                object = entity()
                object.cse_object.flags |= self.get_flag()
                object.cse_object.user_ini = self.get_user_ini()
                object.cse_object.ini = self.get_ini()
                object.import_ltx(lif, section, FULL_IMPORT)
                if (object.cse_object.version != 0) and (
                    (version == 0) or (script_version == 0)
                ):

                    version = object.cse_object.version
                    script_version = object.cse_object.script_version
                    if script_version is None:
                        script_version = gg_version().scr_ver_by_version(
                            version,
                        )  # if !defined script_version;
                elif object.cse_object.version == 0:
                    if (version != 0) and (script_version != 0):

                        object = entity()
                        object.cse_object.flags |= self.get_flag()
                        object.cse_object.user_ini = self.get_user_ini()
                        object.cse_object.ini = self.get_ini()
                        object.cse_object.version = version
                        object.cse_object.script_version = script_version
                        object.import_ltx(lif, section, NO_VERTEX_IMPORT)
                    # 					print "object.cse_object.version\n";
                    else:
                        fail("you must define version in first section")

                # 			print "object.cse_object.game_vertex_id\n";

                if object.cse_object.section_name == "actor":
                    actor_flag += 1
                if actor_flag > 1:
                    fail("second actor object in " + str(fn))

                if object.cse_object.custom_data is not None:
                    if rm := re.match(
                        r"^(.*)\[(spawn_id)\]",
                        object.cse_object.custom_data,
                        flags=re.DOTALL,
                    ):
                        rm1 = rm[0]
                        object.cse_object.custom_data = (
                            rm1 + "[spawn_id]\nobject.cse_object.name = id"
                        )
                    # print idx_log "\n[object.cse_object.name]\nnew_idx = id\n" if !defined self.idx();

                # push @{self.alife_objects}, object;
                self.alife_objects.append(object)
                id += 1

            lif.close()

        if if_.section("unk") is not None:
            fn = if_.value("unk", "binary_files")
            bin_fh = open(fn, "rb")  # or fail("fn: !\n");
            # binmode bin_fh;
            data = ""
            bin_fh.read(data, (bin_fh.stat())[7])
            # self.unk_chunk = \data;
            self.unk_chunk = data
            bin_fh.close()

        if self.idx() is not None:
            idx_log.close()  # if !defined self.idx();

    # }

    def import_level(self, _if):
        # my self = shift;
        # my (if) = @_;
        lif = ini_file(_if, "r")  # or fail("if: !\n");
        print(f"importing alife objects from {_if}\n")
        for i, section in enumerate(lif.sections_list):
            # print(f"#{i} {section}")
            object = entity()
            object.cse_object.flags = self.get_flag()
            object.cse_object.ini = self.get_ini()
            object.import_ltx(lif, section)
            self.alife_objects.append(object)

        lif.close()

    def import_af_spawn(self, _if):
        # my self = shift;
        # my (if) = @_;
        self.af_spawn_places = []
        if self.get_af():
            fh = ini_file(
                "af_spawn_places.ltx",
                "r",
            )  # or fail("af_spawn_places.ltx: !\n");
            for id in fh.sections_list:
                afsp = universal_dict_object()
                # afsp.position = split /,\s*/, fh.value(id, 'position');
                afsp.position = [float(f) for f in split(",", fh.value(id, "position"))]
                afsp.level_vertex_id = int(fh.value(id, "level_vertex_id"))
                afsp.distance = float(fh.value(id, "distance"))
                self.af_spawn_places.append(afsp)
            fh.close()
        else:
            if _if.value("section2", "binary_files") is None:
                return
            fn = _if.value("section2", "binary_files")
            bin_fh = open(fn, "rb")  # or fail("fn: !\n");
            # binmode bin_fh;
            print("importing artefact spawn places data...\n")
            data = ""
            bin_fh.read(data, (bin_fh.stat())[7])
            self.af_spawn_data = data
        # self.af_spawn_data = \data;

    # }

    def import_way(self, _if):
        # my self = shift;
        # my (if) = @_;
        fn = _if.section("way")
        if fn is None:
            return
        sources = _if.value("way", "source_files")
        if not sources:
            return
        # for fn (split /,/, (_if.value('way', 'source_files').split(',') or return))
        for fn in split(",", sources):
            # fn =~ s/^\s*|\s*//g;
            fn = fn.strip()
            # my lif;
            if fn == r"way_debug\y_selo.ltx":
                lif = ini_file("way_debug_y_selo.ltx", "r") or fail(
                    "way_debug_y_selo.ltx: !\n",
                )
            else:
                lif = ini_file(fn, "r") or fail("fn: !\n")

            print(f"importing way objects from file {fn}...\n")
            for section in lif.sections_list:
                object = level_game()
                object.importing(lif, section)
                self.way_objects.append(object)

            lif.close()

    def import_graph(self, _if):
        # my self = shift;
        # my (if) = @_;
        # 	return if !defined if.section('unk');
        if _if.section("graph") is None:
            return
        print("importing graph...\n")
        fn = _if.value("graph", "binary_files")
        bin_fh = open(fn, "rb")  # or fail("fn: !\n");
        # binmode bin_fh;
        data = ""
        data = bin_fh.read()
        bin_fh.close()
        # self.graph_data = \data;
        if self.get_version() == 118:
            self.set_flag(FL_IS_3120)

    # exporting
    def export(self, fn):
        # my self = shift;
        # my (fn) = @_;
        if not self.level():
            _if = ini_file(fn, "w") or fail("fn: !\n")
            self.export_header(_if)
            self.export_alife(_if)
            self.export_af_spawn(_if)
            self.export_way(_if)
            if self.get_version() > 118 or self.is_3120():
                self.export_graph(_if)
            _if.close()
        else:
            self.export_level("level_spawn.ltx")

    def export_header(self, _if):
        # my self = shift;
        # my (if) = @_;

        fh = _if.fh
        fh.write("[header]\n; don't touch these\n")
        fh.write(f"graph_version = {self.graph_version}\n")
        if self.guid is not None:
            fh.write(
                "guid = " + unpack("H*", self.guid)[0] + "\n",
            )  # if (defined self.guid);
        if self.graph_guid is not None:
            fh.write(
                "graph_guid = " + unpack("H*", self.graph_guid)[0] + "\n",
            )  # if (defined self.graph_guid);
        if self.level_count is not None:
            fh.write(
                f"level_count = {self.level_count}\n",
            )  # if (defined self.level_count);
        if self.unknown is not None:
            fh.write(f"unknown = {self.unknown}\n")  # if (defined self.unknown);
        if self.flags != 0:
            fh.write(f"flags = {self.flags}\n")
        fh.write("\n")

    def export_alife(self, _if):
        id = 0
        if_by_level = universal_dict_object()
        levels = []

        objects_by_level_id = (
            universal_dict_object()
        )  # key = level_id, value = array_ref
        # split objects by level id
        for object in self.alife_objects:
            level_name = self.graph.level_name(object.cse_object.game_vertex_id)
            level_id = self.graph.level_id(level_name)
            if level_id not in objects_by_level_id:
                objects_by_level_id[level_id] = []
            objects_by_level_id[level_id].append(object)
        # push @{objects_by_level_id{}}, object;

        # sort objects in arrays by section name
        sort = self.get_sort()
        sorter = None
        if sort is not None:
            if sort == "simple":
                sorter = lambda a: a.cse_object.name
            elif sort == "complex":
                sorter = lambda a: (a.cse_object.section_name, a.cse_object.name)
        if sorter is not None:
            for key in objects_by_level_id.keys():
                arr = objects_by_level_id[key]
                sorted_arr = sorted(arr, key=sorter)
                objects_by_level_id[key] = sorted_arr
            # if (sort == 'simple'):
            #     for arr in (objects_by_level_id.values()):
            #         # my @new = sort {a.cse_object.name cmp b.cse_object.name} @arr;
            #         # arr = \@new;
            #         pass
            #
            # elif (sort == 'complex'):
            #     for arr in (objects_by_level_id.values()):
            #         # my @new = sort {(a.cse_object.section_name cmp b.cse_object.section_name) || (a.cse_object.name cmp b.cse_object.name)} @arr;
            #         # arr = \@new;
            #         pass

        keys = sorted(objects_by_level_id.keys(), key=lambda i: str(i))
        # export objects
        for i in keys:
            arr = objects_by_level_id[i]
            if not arr:
                continue
            # next if !defined arr;
            level = self.graph.level_name_by_id(i)
            # next if !defined level;
            if not level:
                continue
            lif = if_by_level.get(level)
            if lif is None:
                levels.append(f"alife_{level}.ltx")
                if level == r"debug\y_selo":
                    lif = ini_file(
                        "alife_debug_y_selo.ltx",
                        "w",
                    )  # or fail("alife_debug_y_selo.ltx: !\n");
                else:
                    lif = ini_file(
                        f"alife_{level}.ltx",
                        "w",
                    )  # or fail("alife_level.ltx: !\n");

                print("exporting alife objects on level level...\n")
                if_by_level[level] = lif

            out_sects = open(level + ".sections", "w", encoding="cp1251")
            for object in arr:
                # print(f"Exporting {object.cse_object.section_name} {object.cse_object.name}")
                object.export_ltx(lif, id)
                id += 1
                out_sects.write(f"{object.cse_object.name}\n")

            out_sects.close()

        if self.get_version() == 85:
            bin_fh = open("unk_chunk.bin", "wb")  # or fail("unk_chunk.bin: !\n");
            # binmode bin_fh;
            bin_fh.write(self.unk_chunk, len(self.unk_chunk))
            bin_fh.close()

        fh = _if.fh
        fh.write("[alife]\nsource_files = <<END\n" + ",\n".join(levels) + "\nEND\n\n")
        if self.get_version() == 85:
            fh.write("[unk]\nbinary_files = unk_chunk.bin\n\n")
        for _if in if_by_level.values():
            _if.close()

    def export_level(self, _if):
        # my self = shift;
        # my (if) = @_;

        id = 0
        if not Path(_if).parent.exists():
            Path(_if).parent.mkdir(parents=True)
        lif = ini_file(_if, "w")  # or fail("if: !\n");
        for object in self.alife_objects:
            if not object:
                continue
            # next unless defined object;
            object.export_ltx(lif, id)
            id += 1

        lif.close()

    def export_af_spawn(self, _if):
        # my self = shift;
        # my (if) = @_;
        if self.get_af():
            fh = open(
                "af_spawn_places.ltx",
                "w",
                encoding="cp1251",
            )  # or fail("af_spawn_places.ltx: !\n");
            id = 0
            for afsp in self.af_spawn_places:
                fh.write(f"[{id}]\n")
                fh.write(
                    f"position = {afsp.position[0]:f},{afsp.position[1]:f},{afsp.position[2]:f}\n",
                )
                fh.write(f"level_vertex_id = {afsp.level_vertex_id}\n")
                fh.write(f"distance = {afsp.distance}\n")
                id += 1
            fh.close()
        else:
            bin_fh = open("section2.bin", "wb")  # or fail("section2.bin: !\n");
            # binmode bin_fh;
            print("exporting raw data...\n")
            bin_fh.write(self.af_spawn_data)
            fh = _if.fh
            fh.write("[section2]\nbinary_files = section2.bin\n\n")

    way_name_exceptions = {
        "kat_teleport_to_dark_city_orientation": "l03u_agr_underground",
        "kat_teleport_to_dark_city_position": "l03u_agr_underground",
        "walk_3": "l05_bar",
        "rad_heli_move": "l10_radar",
        "pri_heli4_go2_path": "l11_pripyat",
        "sar_teleport_0000_exit_look": "l12u_sarcofag",
        "sar_teleport_0000_exit_walk": "l12u_sarcofag",
        "val_ambush_dest_look": "l04_darkvalley",
    }

    def export_way(self, _if):
        # my self = shift;
        # my (if) = @_;

        # init prefixes
        prefixes = self.init_way_prefixes()
        if self.way_objects:
            info_by_level = universal_dict_object()

            for object in self.way_objects:
                level = self.get_level_name(object, prefixes)
                if not level:
                    fail(
                        "unknown level of the way object " + object.name,
                    )  # unless defined level;
                info = info_by_level.get(level)
                if info is None:
                    info = universal_dict_object()
                    if level == r"debug\y_selo":
                        info.lif = ini_file(
                            "way_debug_y_selo.ltx",
                            "w",
                        )  # or fail("way_debug_y_selo.ltx: !\n");
                    else:
                        info.lif = ini_file(
                            f"way_{level}.ltx",
                            "w",
                        )  # or fail("way_level.ltx: !\n");

                    info.way_objects = []
                    info_by_level[level] = info

                info.way_objects.append(object)

            id = 0
            # 		foreach my info (values %info_by_level) {
            for level, info in info_by_level.items():
                print("exporting way objects on level level...\n")
                for object in sorted(info.way_objects, key=lambda o: o.name):
                    object.export(info.lif, id)
                    id += 1

                info.lif.close()

            fh = _if.fh
            fh.write(
                "[way]\nsource_files = <<END\n"
                + ",\n".join(
                    map(lambda s: f"way_{s}.ltx", sorted(info_by_level.keys())),
                )
                + "\nEND\n\n",
            )
        # fh.write("[way]\nsource_files = <<END\n", ",\n".join(map {"way__.ltx"} (sort {a cmp b} keys %info_by_level.keys))), "\nEND\n\n")

    def init_way_prefixes(self):
        # my self = shift;
        prefixes = self.get_prefixes_ini()
        if (prefixes is not None) and "prefixes" in prefixes.sections_hash:
            for key in prefixes.sections_hash["prefixes"].keys():
                # arr = split /,\s*/, prefixes.sections_hash[prefixes][key].split(',')
                arr = [
                    s.strip()
                    for s in split(",", prefixes.sections_hash["prefixes"][key])
                ]
                prefixes.sections_hash["prefixes"][key] = arr

        return prefixes

    def get_level_name(self, object, prefixes):
        # my self = shift;
        # my object = shift;
        # my prefixes = shift;

        default_level = "_level_unknown"
        level = self.graph.level_name(object.points[0].game_vertex_id)
        if level == "_level_unknown":
            for point in object.points:
                l = self.graph.level_name(point.game_vertex_id)
                if l != "_level_unknown":
                    level = l
                    break

            if level == "_level_unknown":
                if prefixes is not None:
                    for key in prefixes.sections_hash["prefixes"].keys():
                        for pref in prefixes.sections_hash["prefixes"][key]:
                            pr = pref + "_"
                            if object.name.startswith(pr):
                                level = key
                                break

                        if level != "_level_unknown":
                            break

            if level == "_level_unknown":
                level = self.way_name_exceptions.get(object.name, default_level)

        return level

    def export_graph(self, _if):
        # my self = shift;
        # my (if) = @_;
        print("exporting graph...\n")
        fn = "section4.bin"
        bin_fh = open(fn, "wb")  # or fail("fn: !\n");
        # binmode bin_fh;
        bin_fh.write(self.graph_data)
        bin_fh.close()
        fh = _if.fh
        fh.write(f"[graph]\nbinary_files = {fn}\n\n")

    # split spawns
    def prepare_graph_points(self):
        # my self = shift;
        graph = self.graph
        print("preparing graph points...\n")
        i = 0
        for vertex in graph.vertices:
            vertex.name = (
                graph.level_by_id[vertex.level_id].level_name + "_graph_point_" + str(i)
            )
            vertex.id = i
            i += 1

        for object in self.alife_objects:
            object.cse_object.flags |= FL_LEVEL_SPAWN
            # ref
            if (object.cse_object).__class__.__name__ != "se_level_changer":
                continue
            graph.vertices[object.cse_object.dest_game_vertex_id].name = (
                object.cse_object.dest_graph_point
            )

        tmp = [
            (i, self.graph.level_name(_object.cse_object.game_vertex_id))
            for (i, _object) in enumerate(self.alife_objects)
        ]
        indexes_by_levels = {}
        for i, level in tmp:
            indexes_by_levels[level] = indexes_by_levels.get(level, []) + [i]

        sorted_levels = sorted(graph.level_by_guid.values())

        for level in sorted_levels:
            level_spawn = all_spawn()
            level_spawn.level_name = level
            level_spawn.config = universal_dict_object()
            level_spawn.config.common = universal_dict_object()
            level_spawn.config.common.src = ""
            level_spawn.config.common.out = level + "/level.spawn"
            level_spawn.set_flag(FL_LEVEL_SPAWN)
            id = 0
            for vertex in graph.vertices:
                if graph.level_by_id[vertex.level_id].level_name == level:
                    object = entity()
                    object.cse_object.flags |= FL_LEVEL_SPAWN
                    self.convert_point(object, vertex, level, id)
                    id += 1
                    level_spawn.alife_objects.append(object)

            self.split_spawns(level_spawn)
            self.level_spawns.append(level_spawn)

        for ls in self.level_spawns:
            for o in ls.alife_objects:
                o.cse_object.game_vertex_id = 0xFFFF

    def convert_point(self, object, vertex, level, id):
        # my self = shift;
        # my () = @_;
        graph = self.graph
        # 	print "	converting vertices of level level...\n";
        object.init_abstract()
        object.cse_object.version = self.get_version()
        object.cse_object.script_version = self.get_script_version()
        object.cse_object = bless(object.cse_object, "cse_alife_graph_point", globals())
        object.init_object()
        object.cse_object.name = vertex.name
        object.cse_object.section_name = "graph_point"
        object.cse_object.position = vertex.level_point
        object.cse_object.direction = [0, 0, 0]
        for i in range(vertex.edge_count):
            edge = graph.edges[int(vertex.edge_index) + i]
            vertex2 = graph.vertices[edge.game_vertex_id]
            if vertex.level_id != vertex2.level_id:
                level2 = graph.level_by_id[vertex2.level_id]
                name2 = level2.level_name
                object.cse_object.connection_point_name = vertex2.name
                object.cse_object.connection_level_name = name2

        object.cse_object["location0"] = vertex.vertex_type[0]
        object.cse_object["location1"] = vertex.vertex_type[1]
        object.cse_object["location2"] = vertex.vertex_type[2]
        object.cse_object["location3"] = vertex.vertex_type[3]

    def read_level_spawns(self):
        # my self = shift;
        print("splitting spawns...\n")
        # prepare arrays with level spawns
        for level in self.graph.level_by_guid.values():
            if level == "_level_unknown":
                continue
            level_spawn = all_spawn()
            level_spawn.level_name = level
            level_spawn.config.common.src = level_spawn.config.common.out = (
                level + "/level.spawn"
            )
            level_spawn.set_flag(FL_LEVEL_SPAWN)
            level_spawn.config.mode = "split"
            level_spawn.read()
            self.split_spawns(level_spawn)
            self.level_spawns.append(level_spawn)

    def split_spawns(self, ls):
        # my self = shift;
        # my (ls) = @_;
        print(f"filling level.spawn with objects ({ls.level_name})...\n")
        tmp = [
            (i, self.graph.level_name(_object.cse_object.game_vertex_id))
            for (i, _object) in enumerate(self.alife_objects)
        ]
        indexes_by_levels = {}
        for i, level in tmp:
            indexes_by_levels[level] = indexes_by_levels.get(level, []) + [i]
        # prepare arrays with level spawns
        for object in self.alife_objects:
            if self.graph.level_name(object.cse_object.game_vertex_id) == ls.level_name:
                if ls.level_name == "_level_unknown":
                    print(
                        f"{object.cse_object.game_vertex_id}, {object.cse_object.name}\n",
                    )
                # 			object.cse_object.game_vertex_id = 0xFFFF;
                object.cse_object.level_vertex_id = 0xFFFFFFFF
                object.cse_object.distance = 0
                object.cse_object.flags |= FL_LEVEL_SPAWN
                ls.alife_objects.append(object)

        # print(f"filled level.spawn with objects ({ls.level_name}). Objects count {len(ls.alife_objects)}\n")

    def write_splitted_spawns(self):
        # my self = shift;
        print("writing level spawns...\n")

        for level_spawn in self.level_spawns:
            print(f"writing {level_spawn.level_name}...")
            level = level_spawn.level_name
            # rename level.'/level.spawn', level.'/level.spawn.bak' or (unlink level.'/level.spawn.bak' and rename level.'/level.spawn', level.'/level.spawn.bak');
            level_spawn.write()

    def split_ways(self) -> None:
        # my self = shift;
        graph = self.graph
        print("splitting ways...\n")
        info_by_level = universal_dict_object()
        prefixes = self.init_way_prefixes()
        for object_ in self.way_objects:
            level = self.get_level_name(object_, prefixes)
            if level is None:
                fail(
                    "unknown level of the way object object.name\n",
                )  # unless defined level;
            info = info_by_level.get(level, None)
            if info is None:
                info = universal_dict_object()
                # rename level.'/level.game', level.'/level.game.bak' or (unlink level.'/level.game.bak' and rename level.'/level.game', level.'/level.game.bak') ;
                if level != "_level_unknown":  # workaround for split mode
                    info.lif = chunked(
                        level + "/level.game",
                        "w",
                    )  # or fail("level/level.game: !\n");
                else:
                    info.lif = chunked(
                        "unrecognized_ways.game",
                        "w",
                    )  # or fail("unrecognized_ways.game: !\n");

                info.way_objects = []
                info_by_level[level] = info

            info.way_objects.append(object_)  # , \object;

        for info in info_by_level.values():
            id_ = 0
            info.lif.w_chunk_open(4096)
            sprted_ways = sorted(info.way_objects, key=lambda way: way.name)
            for object_ in sprted_ways:
                object_.split_ways(info.lif, id_)
                id_ += 1

            info.lif.w_chunk_close()
            info.lif.w_chunk_open(8192)
            info.lif.w_chunk_close()
            info.lif.close()

    # convert
    def prepare_objects(self):
        # my self = shift;
        ini_file = self.config.convert.ini
        if ini_file is None:
            ini_file = "convert.ini"  # if !defined ini_file;
        conv_ini = ini_file(ini_file, "r")  # or fail("ini_file: !\n");
        if conv_ini.value("exclude", "sections") is not None:
            exclude_sects = split(",")
        exclude_classes = convert().get_harm(self.config.convert.new_version)

    # my %sExclude_simple;
    # my %sExclude_regexp;
    # for sect in (exclude_sects):
    # 	if (sect !~ /\*/):
    # 		sExclude_simple[sect] = 1
    # 	else:
    # 		if ( re.match("\*|^\*", sect)):
    # 			sect =~ s/\*//;
    # 			sExclude_regexp[sect] = 1
    # 		else:
    # 			my @sect = split /\*/, sect
    # 			sExclude_regexp{\@sect} = 1
    #
    # my %clExclude;
    # foreach my class (@exclude_classes) {
    # 	clExclude{class} = 1;
    # }
    # my id = 0;
    # foreach my object (@{self.alife_objects}) {
    # 	(push (@{self.harm_objects}, object) and delete(self.alife_objects[id]) and next) if defined clExclude{ref(object.cse_object)};
    # 	(push (@{self.excluded_objects}, object) and delete(self.alife_objects[id]) and next) if defined sExclude_simple{object.cse_object.section_name};
    # 	foreach my section (keys %sExclude_regexp) {
    # 		if (ref(section) eq 'REF') {
    # 			my c = 0;
    # 			foreach (@section) {
    # 				++c if  re.match("_", object.cse_object.section_name);
    # 			}
    # 			(push (@{self.excluded_objects}, object) and delete(self.alife_objects[id]) and last) if c == #{section} + 1;
    # 		} else {
    # 			(push (@{self.excluded_objects}, object) and delete(self.alife_objects[id]) and last) if  re.match("section", object.cse_object.section_name);
    # 		}
    # 	}
    # 	next if !defined self.alife_objects[id];
    # 	my %add;
    # 	my %rep;
    # 	if (defined conv_ini.sections_hash{object.cse_object.section_name}) {
    # 		foreach my param (keys %{conv_ini.sections_hash{object.cse_object.section_name}}) {
    # 			my @temp = split /:\s*/, param;
    # 			add{temp[1]} = conv_ini.sections_hash{object.cse_object.section_name}{param} if temp[0] eq 'add';
    # 			rep{temp[1]} = conv_ini.sections_hash{object.cse_object.section_name}{param} if temp[0] eq 'rep';
    # 		}
    # 		foreach my param (keys %{object.cse_object}) {
    # 			if (defined add{param}) {
    # 				if ( re.match("^\d+", add{param})) {
    # 					object.cse_object.param += add{param};
    # 				} else {
    # 					object.cse_object.param .= add{param};
    # 				}
    # 			}
    # 			if (defined rep{param}) {
    # 				object.cse_object.param = rep{param};
    # 			}
    # 		}
    # 	}
    # }
    # continue {
    # 	id++;
    # }
    # conv_ini.close();

    def print_harm_objects(self):
        # my self = shift;
        (lif) = ini_file("harm_objects.ltx", "w") or fail("harm_objects.ltx: !\n")
        print("exporting harm objects\n")
        id_ = 0
        for object in self.harm_objects:
            object.export_ltx(lif, id_)
            id_ += 1

        lif.close()

    def print_excluded_objects(self):
        # my self = shift;
        (lif) = ini_file("excluded_objects.ltx", "w") or fail(
            "excluded_objects.ltx: !\n",
        )
        print("exporting excluded objects\n")
        id = 0
        for object in self.excluded_objects:
            object.export_ltx(lif, id)
            id += 1

        lif.close()

    # parse
    def parse_way(self, out: str) -> None:
        # my self = shift;
        # my (out) = @_;
        # import
        fn = self.get_src()
        # fn =~ s/alife/way/;
        fn = fn[: -len("/alife/way/")]
        fn = "../" + fn
        fh = ini_file(fn, "r")  # or fail("fn: !\n");
        print("importing way objects from file fn...\n")
        for section in fh.sections_list:
            object_ = level_game()
            object_.importing(fh, section)
            for point in object_.points:
                point.game_vertex_id += self.get_new_gvid() - self.get_old_gvid()

            self.way_objects.append(object_)

        fh.close()
        # export
        # out =~ s/alife/way/;
        out = out[: -len("/alife/way/")]
        fh = ini_file(out, "w")  # or fail("out: !\n");
        print("exporting way objects to file out...\n")
        id_ = 0
        sorted_ways = sorted(self.way_objects, key=lambda way: way.name)
        for object_ in sorted_ways:
            object_.export(fh, id_)
            id_ += 1

        fh.close()

    # other subs
    def check_graph_build(self):
        if self.is_3120():
            return "cop"  # if _[0].is_3120();
        return gg_version().graph_build(self.get_version(), self.get_script_version())

    def check_graph_version(self):
        if self.is_3120():
            return 9  # if _[0].is_3120()
        return gg_version().graph_ver_by_ver(self.get_version())

    def level(self):
        if self.get_flag() & FL_LEVEL_SPAWN:
            return 1

        return 0

    def get_level_id(self, wtf):
        for level in self.sections_list.reverse():
            if wtf >= self.value(level, "gvid0"):
                return self.value(level, "id")

        return None

    def read_service_chunk(self, cf):
        # my self = shift;
        # my (cf) = @_;
        if cf.find_chunk(5):
            print("reading service information...\n")
            (self.idx_file,) = unpack("Z*", cf.r_chunk_data())
            cf.close_found_chunk()

    def write_service_chunk(self, cf: chunked) -> None:
        # my self = shift;
        # my (cf) = @_;

        if self.idx():
            print("writing service information...\n")
            # my idx_name;
            if self.idx() == "":
                idx_name = "spawn_ids.ltx"
            else:
                idx_name = self.idx()

            cf.w_chunk(5, pack("Z*", idx_name))

    def write_unknown_section(self) -> None:
        fh = open("unk_chunk.bin", "w", encoding="cp1251")
        # fh.write(${_[0]}, length(${_[0]}));
        fh.close()
