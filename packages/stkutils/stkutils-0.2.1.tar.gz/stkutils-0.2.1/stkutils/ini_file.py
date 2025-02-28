# Module for importing and exporting variables and data structures
# Update history^
# 	26/08/2012 - fix for new fail() syntax
# 	09/08/2012 - implementing import/export for some clear sky se_actor properties
######################################################
import math
import re

from stkutils.binary_data import pack, unpack
from stkutils.perl_utils import chomp, defined, fail, join, split, universal_dict_object
from stkutils.stkutils_math import CTime


class ini_file:

    def __init__(self, fn, mode):

        fh = open(fn, mode, encoding="cp1251")  # or return undef;

        # my self = universal_dict_object();
        self.fh = fh
        self.sections_list = []
        self.sections_hash = universal_dict_object()
        # bless(self, $class);

        if mode == "w":
            return

        section = None
        skip_section = 0
        section_header = re.compile(r"^\[(?P<section>.*)\]\s*:*\s*(?P<flag>\w.*)?$")
        section_value = re.compile(r"^\s*(?P<name>[^=]*?)\s*=\s*(?P<value>.*?)$")
        while line := fh.readline():
            # for line in fh.readlines():
            # $_ =~ qr/^\s*;/ and continue;
            # line = fh.readline()

            if rm := re.match(section_header, line):
                rm1 = rm.group("section")
                rm2 = rm.group("flag")
                if rm2 is not None and not is_flag_defined(rm2):
                    skip_section = 1
                    continue

                section = rm1

                if self.sections_hash.get(section, None) is not None:
                    fail("duplicate section " + section + " found while reading " + fn)
                self.sections_list.append(section)
                tmp = universal_dict_object()
                # 			tie %tmp, "Tie::IxHash";
                self.sections_hash[section] = tmp
                skip_section = 0
                continue
            if rm := re.match(section_value, line):
                rm1 = rm.group("name")
                rm2 = rm.group("value")
                (name, value) = (rm1, rm2)
                # костыль ебучий. Почему-то название одной секции с perl содержит \r
                if section == "gar_smart_garage_guard_3_look" and name == "p0:name":
                    value += "\r"
                if rm := re.match(r"^<<(.*)\s*$", value):
                    rm1 = rm[0]
                    rm2 = rm[1]
                    terminator = rm2
                    value = ""
                    while fh:
                        line = fh.readline()
                        # chomp;

                        if re.match(rf"^\s*{terminator}\s*$", line):
                            break
                        value += line
                        # value += "\n" + line
                    # }
                    if line is None:
                        raise ValueError
                    # die unless defined $_;
                    # substr ($value, 0, 1) = '';
                    # value[0] = ""
                    value = chomp(value)
                if skip_section == 1:
                    continue
                if section is None:
                    fail(
                        "undefined section found while reading " + fn,
                    )  # unless defined section;
                if (name != "custom_data") and re.match(r"^(.+)(?=\s*;+?)", value):
                    value = rm1

                self.sections_hash[section][name] = value

    # return self

    def close(self):
        # my self = shift;
        self.fh.close()
        self.fh = None

    format_for_number = {
        "h32": "%#x",
        "h16": "%#x",
        "h8": "%#x",
        "u32": "%u",
        "u16": "%u",
        "u8": "%u",
        "q8": "%.8g",
        "q16": "%.8g",
        "q16_old": "%.8g",
        "s32": "%d",
        "s16": "%d",
        "s8": "%d",
        "f32": "%.8g",
    }

    # export functions
    def export_properties(self, comment, container, *args):
        # # my self = shift;
        # my $comment = shift;
        # my container = shift;
        if len(args) == 1 and isinstance(args[0], tuple):
            args = args[0]
        # print container.name."\n";
        fh = self.fh
        if comment is not None:
            fh.write(f"\n; {comment} properties\n")
        for p in args:
            # 	print "$p['name'], $p.type\n";
            format = self.format_for_number.get(p["type"])
            if format is not None:
                self._export_scalar(fh, format, container, p)
                continue
            if p["type"] == "sz":
                self._export_string(fh, container, p)
                continue
            if p["type"] == "shape":
                self._export_shape(fh, container, p)
                continue
            if p["type"] == "skeleton":
                self._export_skeleton(fh, container, p)
                continue
            if p["type"] == "supplies":
                self._export_supplies(fh, container, p)
                continue
            if re.match("afspawns", p["type"]):
                self._export_artefact_spawns(fh, container, p)
                continue
            if p["type"] == "ordaf":
                self._export_ordered_artefacts(fh, container, p)
                continue
            if p["type"] == "CTime":
                self._export_ctime(fh, p["name"], container[p["name"]])
                continue
            if p["type"] == "complex_time":
                self._export_ctime(fh, p["name"], container[p["name"]])
                continue
            if p["type"] == "npc_info":
                self._export_npc_info(fh, container, p)
                continue
            # SOC
            if p["type"] == "jobs":
                self._export_jobs(fh, container, p)
                continue
            # CS
            if p["type"] == "covers":
                self._export_covers(fh, container, p)
                continue
            if p["type"] == "squads":
                self._export_squads(fh, container, p)
                continue
            if p["type"] == "sim_squads":
                self._export_sim_squads(fh, container, p)
                continue
            if p["type"] == "inited_tasks":
                self._export_inited_tasks(fh, container, p)
                continue
            if p["type"] == "inited_find_upgrade_tasks":
                self._export_inited_find_upgrade_tasks(fh, container, p)
                continue
            if p["type"] == "rewards":
                self._export_rewards(fh, container, p)
                continue
            if p["type"] == "minigames":
                self._export_minigames(fh, container, p)
                continue
            # COP
            if p["type"] == "times":
                self._export_times(fh, container, p)
                continue
            self._export_vector(fh, container, p)

    def _export_scalar(self, fh, format, container, p):

        if container.get(p["name"]) is None:
            fail(f'undefined field {p["name"]} for entity {container.name}')
        if p["default"] is not None and container[p["name"]] == p["default"]:
            return
        if (
            p["default"] is not None
            and abs(container[p["name"]] - p["default"]) < 0.001
            and (p["type"] == "f32" or p["type"] == "q8")
        ):
            return
        formatted_num = self.format_num(format, container[p["name"]])
        fh.write(f"{p['name']} = {formatted_num}\n")

    def format_num(self, _format, num: int | float) -> str:
        if _format == "%#x" and num == 0:
            return "0"
        python_format = _format.replace("%", ":").replace("u", "d")
        return ("{" + python_format + "}").format(num)

    def _export_string(self, fh, container, p):
        # my (fh, container, $p) = args;
        if defined(p.get("default")) and container[p["name"]] == p["default"]:
            return
        value = container[p["name"]]
        if "\n" in value:
            value = value.replace(
                "\r\n",
                "\n",
            )  # WTF? Приводит к двойным переносам строк
            fh.write(f"{p['name']} = <<END\n{value}\nEND\n")
        else:
            fh.write(f"{p['name']} = {value}\n")

    def _export_vector(self, fh, container, p):
        # my () = args;
        if re.match("dumb", p["type"]):
            fh.write(f"{p['name']} = " + unpack("H*", container[p["name"]])[0] + "\n")
        else:
            if p["default"] and self.comp_arrays(container, p):
                return
            maybe_format_values = [
                (self._format_float(f) if isinstance(f, float) else f)
                for f in container[p["name"]]
            ]
            fh.write(f"{p['name']} = " + join(", ", maybe_format_values) + "\n")

    def _format_float(self, f: float) -> str:
        if math.isnan(f):
            return str(f)
        if abs(int(f) - f) < 1e-12:
            return str(int(f))
        return str(round(f, 13))

    def _export_shape(self, fh, container, p):
        # my () = args;

        count = len(container[p["name"]])
        fh.write(p["name"] + " = " + str(count) + "\n")
        # my $i = 0;
        for i, shape in enumerate(container[p["name"]]):
            id = f"shape_{i}"
            if shape["type"] == 0:
                fh.write(f"{id}:type = sphere\n")
                fh.write(
                    f"{id}:offset = " + join(",", shape["sphere"][0 : 2 + 1]) + "\n",
                )
                fh.write(f"{id}:radius = {shape.sphere[3]}\n")
            elif shape["type"] == 1:
                fh.write(f"{id}:type = box\n")
                fh.write(f"{id}:axis_x = " + join(",", shape["box"][0 : 2 + 1]) + "\n")
                fh.write(f"{id}:axis_y = " + join(",", shape["box"][3 : 5 + 1]) + "\n")
                fh.write(f"{id}:axis_z = " + join(",", shape["box"][6 : 8 + 1]) + "\n")
                fh.write(f"{id}:offset = " + join(",", shape["box"][9 : 11 + 1]) + "\n")

    def _export_skeleton(self, fh, container, p):
        # my () = args;

        fh.write("bones_mask = " + join(",", container.bones_mask) + "\n")
        fh.write("root_bone = container.root_bone\n")
        fh.write("bbox_min = " + join(",", container.bbox_min) + "\n")
        fh.write("bbox_max = " + join(",", container.bbox_max) + "\n")
        count = len(container.bones)
        fh.write(f"bones_count = {count}\n")

        for i, bone in enumerate(container.bones):
            id = f"bone_{i}"
            fh.write(f"{id}:ph_position = " + join(",", bone.ph_position) + "\n")
            fh.write(f"{id}:ph_rotation = " + join(",", bone.ph_rotation) + "\n")
            fh.write(f"{id}:enabled = {bone.enabled}\n\n")

    def _export_supplies(self, fh, container, p):
        # my () = args;

        count = len(container[p["name"]])
        fh.write(p["name"] + " = " + str(count) + "\n")

        # return if $count == 0;
        # my $i = 0;
        for i, sect in enumerate(container[p["name"]]):
            id = f"sup_{i}"
            fh.write(f"{id}:section_name = {sect.section_name}\n")
            fh.write(f"{id}:item_count = {sect.item_count}\n")
            fh.write(f"{id}:min_factor = {sect.min_factor}\n")
            fh.write(f"{id}:max_factor = {sect.max_factor}\n")
            fh.write("\n")

    # $i++;

    # }

    def _export_artefact_spawns(self, fh, container, p):
        # my () = args;

        count = len(container[p["name"]])
        fh.write(p["name"] + " = " + str(count) + "\n")
        # return if $count == 0;
        # my $i = 0;
        for i, sect in enumerate(container[p["name"]]):
            id = f"art_{i}"
            fh.write(f"{id}:section_name = {sect.section_name}\n")
            fh.write(f"{id}:weight = {sect.weight}\n")
            fh.write("\n")

    # $i++;

    def _export_ordered_artefacts(self, fh, container, p):
        # my () = args;

        # my $i = 0;
        # my $k = 0;
        count = len(container[p["name"]])
        fh.write(p["name"] + " = " + str(count) + "\n")
        # return if $count == 0;
        for i, sect in enumerate(container[p["name"]]):
            id = f"unknown_section_{i}"
            fh.write(f"{id}:unknown_string = {sect.name}\n")
            fh.write(f"{id}:unknown_number = {sect.number}\n")
            count = len(sect.af_sects)
            fh.write(f"{id}:artefact_sections = " + str(count) + "\n")
            # $k = 0;
            for k, af in enumerate(sect.af_sects):
                af_id = f"artefact_section_{i}"
                fh.write(f"{id}:{af_id}:artefact_name = {af.af_section}\n")
                fh.write(f"{id}:{af_id}:number_1 = {af.unk_num1}\n")
                fh.write(f"{id}:{af_id}:number_2 = {af.unk_num2}\n")

    def _export_ctime(self, fh, name, time):
        # my () = args;
        # 	print $time."\n";
        if time == 0:
            return
        time = time.get_all()
        if time[0] != 2000:
            if time[0] != 2255:
                fh.write(f"{name} = ", join(":", time), "\n")
            else:
                fh.write(f"{name} = 255\n")

    def _export_jobs(self, fh, container, p):
        # my () = args;

        count = len(container[p["name"]])
        fh.write(p["name"] + " = " + str(count) + "\n")
        # return if $count == 0;
        # my $i = 0;
        for i, job in enumerate(container[p["name"]]):
            id = f"job_{i}"
            fh.write(f"{id}:job_begin = {job.job_begin}\n")
            fh.write(f"{id}:job_fill_idle = {job.job_fill_idle}\n")
            fh.write(
                f"{id}:job_idle_after_death_end = {job.job_idle_after_death_end}\n\n",
            )

    def _export_npc_info(self, *args, **kwargs):
        if args[1].version >= 122:
            self._export_npc_info_cop(*args)
        elif args[1].version >= 117:
            self._export_npc_info_soc(*args)
        else:
            self._export_npc_info_old(*args)

    def _export_npc_info_old(self, fh, container, p):
        # my (fh, container, $p) = args;

        count = len(container[p["name"]])
        fh.write(p["name"] + " = " + str(count) + "\n")
        # return if $count == 0;
        # my $i = 0;
        for i, info in enumerate(container[p["name"]]):
            id = f"info_{i}"
            fh.write(f"{id}:o_id = {info.o_id}\n")
            fh.write(f"{id}:group = {info.group}\n")
            fh.write(f"{id}:squad = {info.squad}\n")
            fh.write(f"{id}:move_offline = {info.move_offline}\n")
            fh.write(f"{id}:switch_offline = {info.switch_offline}\n")
            self._export_ctime(fh, f"{id}:stay_end", info["stay_end"])
            fh.write(
                (
                    f"{id}:jobN = {info.jobN}\n"
                    if container.script_version >= 1 and container.gulagN != 0
                    else ""
                ),
            )
            fh.write("\n")

    # $i++;

    def _export_npc_info_soc(self, fh, container, p):
        # my (fh, container, $p) = args;

        count = len(container[p["name"]])
        fh.write(p["name"] + " = " + str(count) + "\n")
        # return if $count == 0;
        # my $i = 0;
        for i, info in enumerate(container[p["name"]]):
            id = f"info_{i}"
            fh.write(f"{id}:o_id = {info.o_id}\n")
            fh.write(f"{id}:o_group = {info.o_group}\n")
            fh.write(f"{id}:o_squad = {info.o_squad}\n")
            fh.write(f"{id}:exclusive = {info.exclusive}\n")
            self._export_ctime(fh, f"{id}:stay_end", info["stay_end"])
            fh.write(f"{id}:Object_begin_job = {info.Object_begin_job}\n")
            fh.write(
                (
                    f"{id}:Object_didnt_begin_job = {info.Object_didnt_begin_job}\n"
                    if container.script_version > 4
                    else ""
                ),
            )
            fh.write(f"{id}:jobN = {info.jobN}\n\n")

    # $i++;

    def _export_npc_info_cop(self, fh, container, p):
        # my () = args;

        count = len(container[p["name"]])
        fh.write(p["name"] + " = " + str(count) + "\n")
        # return if $count == 0;
        # my $i = 0;
        for i, info in enumerate(container[p["name"]]):
            id = f"info_{i}"
            fh.write(f"{id}:id = {info.id}\n")
            fh.write(f"{id}:job_prior = {info.job_prior}\n")
            fh.write(f"{id}:job_id = {info.job_id}\n")
            fh.write(f"{id}:begin_job = {info.begin_job}\n")
            fh.write(f"{id}:need_job = {info.need_job}\n\n")

    def _export_covers(self, fh, container, p):
        # my () = args;

        count = len(container[p["name"]])
        fh.write(p["name"] + " = " + str(count) + "\n")
        # return if $count == 0;
        # my $i = 0;
        for i, cover in enumerate(container[p["name"]]):
            id = f"cover_{i}"
            fh.write(f"{id}:npc_id = {cover.npc_id}\n")
            fh.write(f"{id}:cover_vertex_id = {cover.cover_vertex_id}\n")
            fh.write(
                f"{id}:cover_position = ".join(",", (cover["cover_position"])) + "\n",
            )
            fh.write(f"{id}:look_pos = ".join(",", (cover.look_pos)) + "\n")
            fh.write(f"{id}:is_smart_cover = {cover.is_smart_cover}\n\n")

    # $i++;

    def _export_squads(self, fh, container, p):
        # my () = args;

        count = len(container[p["name"]])
        fh.write("\n; squads\n")
        fh.write(p["name"] + " = " + str(count) + "\n")
        # return if $count == 0;
        # my $i = 0;
        for i, squad in enumerate(container[p["name"]]):
            id = f"squad_{i}"
            fh.write(f"{id}:squad_name = {squad.squad_name}\n")
            fh.write(f"{id}:squad_stage = {squad.squad_stage}\n")
            fh.write(f"{id}:squad_prepare_shouted = {squad.squad_prepare_shouted}\n")
            fh.write(f"{id}:squad_attack_shouted = {squad.squad_attack_shouted}\n")
            fh.write(f"{id}:squad_attack_squad = {squad.squad_attack_squad}\n")
            self._export_ctime(
                fh,
                f"{id}:squad_inited_defend_time",
                squad.squad_inited_defend_time,
            )
            self._export_ctime(
                fh,
                f"{id}:squad_start_attack_wait",
                squad.squad_start_attack_wait,
            )
            self._export_ctime(
                fh,
                f"{id}:squad_last_defence_kill_time",
                squad.squad_last_defence_kill_time,
            )
            fh.write(f"{id}:squad_power = {squad.squad_power}\n\n")

    def _export_times(self, fh, container, p):
        # my () = args;

        count = len(container[p["name"]])
        fh.write(p["name"] + " = " + str(count) + "\n")

        for i, time in enumerate(container[p["name"]]):
            id = f"time_{i}"
            self._export_ctime(fh, f"{id}", time)

    def _export_sim_squads(self, fh, container, p):
        # my () = args;

        count = len(container[p["name"]])
        fh.write(p["name"] + " = " + str(count) + "\n")
        # return if $count == 0;
        # my $i = 0;
        for i, squad in enumerate(container[p["name"]]):
            id = f"sim_squad_{i}"
            fh.write(f"{id}:squad_id = {squad.squad_id}\n")
            fh.write(f"{id}:settings_id = {squad.settings_id}\n")
            fh.write(f"{id}:is_scripted = {squad.is_scripted}\n")
            if squad.is_scripted == 1:
                self._export_sim_squad_generic(fh, squad, id)
                fh.write(f"{id}:continue_target = ${squad.continue_target}\n")
                fh.write(f"{id}:need_free_update = ${squad.need_free_update}\n")
                fh.write(f"{id}:relationship = {squad.relationship}\n")
                fh.write(f"{id}:sympathy = {squad.sympathy}\n")

            fh.write("\n")

    def _export_sim_squad_generic(self, fh, squad, id):

        fh.write(f"{id}:smart_id = {squad.smart_id}\n")
        fh.write(f"{id}:assigned_target_smart_id = ${squad.assigned_target_smart_id}\n")
        fh.write(f"{id}:sim_combat_id = ${squad.sim_combat_id}\n")
        fh.write(f"{id}:delayed_attack_task = {squad.delayed_attack_task}\n")
        fh.write(f"{id}:random_tasks = ".join(",", (squad.random_tasks)) + "\n")
        fh.write(f"{id}:npc_count = {squad.npc_count}\n")
        fh.write(f"{id}:squad_power = ${squad.squad_power}\n")
        fh.write(f"{id}:commander_id = ${squad.commander_id}\n")
        fh.write(f"{id}:squad_npc = ".join(",", (squad.squad_npc)) + "\n")
        fh.write(f"{id}:spoted_shouted = {squad.spoted_shouted}\n")
        fh.write(f"{id}:squad_power = ${squad.squad_powe}r\n")
        self._export_ctime(fh, f"{id}:last_action_timer", squad.last_action_timer)
        fh.write(f"{id}:squad_attack_power = ${squad.squad_attack_power}\n")
        fh.write(f"{id}:class = ${squad['class']}\n")
        if squad["class"] is not None:
            if squad["class"] == 1:
                # sim_attack_point
                fh.write(f"{id}:dest_smrt_id = {squad.dest_smrt_id}\n")
                fh.write(f"{id}:major = ${squad.major}\n")
                fh.write(f"{id}:target_power_value = ${squad.target_power_value}\n")
            else:
                # sim_stay_point
                fh.write(f"{id}:stay_defended = {squad.stay_defended}\n")
                fh.write(f"{id}:continue_point_id = ${squad.continue_point_id}\n")
                self._export_ctime(fh, f"{id}:begin_time", squad.begin_time)

        fh.write(f"{id}:items_spawned = {squad.items_spawned}\n")
        self._export_ctime(
            fh,
            f"{id}:bring_item_inited_time",
            squad.bring_item_inited_time,
        )
        self._export_ctime(
            fh,
            f"{id}:recover_item_inited_time",
            squad.recover_item_inited_time,
        )

    def _export_inited_tasks(self, fh, container, p):

        count = len(container[p["name"]])
        fh.write("\n; inited tasks\n")
        fh.write(p["name"] + " = " + str(count) + "\n")
        # return if $count == 0;
        # my $i = 0;
        for i, task in enumerate(container[p["name"]]):
            id = f"task_{i}"
            fh.write(f"{id}:base_id = {task.base_id}\n")
            fh.write(f"{id}:id = {task.id}\n")
            fh.write(f"{id}:type = {task.type}\n")

            if task.type == 0 or task.type == 5:
                self._export_CStorylineTask(fh, task, id)
            elif task.type == 1:
                self._export_CEliminateSmartTask(fh, task, id)
            elif task.type == 2:
                self._export_CCaptureSmartTask(fh, task, id)
            elif task.type == 3 or task.type == 4:
                self._export_CDefendSmartTask(fh, task, id)
            elif task.type == 6:
                self._export_CBringItemTask(fh, task, id)
            elif task.type == 7:
                self._export_CRecoverItemTask(fh, task, id)
            elif task.type == 8:
                self._export_CFindUpgradeTask(fh, task, id)
            elif task.type == 9:
                self._export_CHideFromSurgeTask(fh, task, id)
            elif task.type == 10:
                self._export_CEliminateSquadTask(fh, task, id)

            fh.write("\n")

    def _export_CGeneralTask(self, fh, task, id):

        fh.write(f"{id}:entity_id = {task.entity_id}\n")
        fh.write(f"{id}:prior = {task.prior}\n")
        fh.write(f"{id}:status = {task.status}\n")
        fh.write(f"{id}:actor_helped = {task.actor_helped}\n")
        fh.write(f"{id}:community = {task.community}\n")
        fh.write(f"{id}:actor_come = {task.actor_come}\n")
        fh.write(f"{id}:actor_ignore = {task.actor_ignore}\n")
        self._export_ctime(fh, f"{id}:inited_time", task.inited_time)

    def _export_CStorylineTask(self, fh, task, id):
        self._export_CGeneralTask(fh, task, id)
        fh.write(f"{id}:target = {task.target}\n")

    def _export_CEliminateSmartTask(self, fh, task, id):
        self._export_CGeneralTask(fh, task, id)
        fh.write(f"{id}:target = {task.target}\n")
        fh.write(f"{id}:src_obj = {task.src_obj}\n")
        fh.write(f"{id}:faction = {task.faction}\n")

    def _export_CCaptureSmartTask(self, fh, task, id):
        self._export_CGeneralTask(fh, task, id)
        fh.write(f"{id}:target = {task.target}\n")
        fh.write(f"{id}:state = {task.state}\n")
        fh.write(f"{id}:counter_attack_community = {task.counter_attack_community}\n")
        fh.write(f"{id}:counter_squad = {task.counter_squad}\n")
        fh.write(f"{id}:src_obj = {task.src_obj}\n")
        fh.write(f"{id}:faction = {task.faction}\n")

    def _export_CDefendSmartTask(self, fh, task, id):

        self._export_CGeneralTask(fh, task, id)
        fh.write(f"{id}:target = {task.target}\n")
        self._export_ctime(fh, f"{id}:last_called_time", task.last_called_time)

    def _export_CBringItemTask(self, fh, task, id):
        self._export_CGeneralTask(fh, task, id)
        fh.write(f"{id}:state = {task.state}\n")
        fh.write(f"{id}:ri_counter = {task.ri_counter}\n")
        fh.write(f"{id}:target = {task.target}\n")
        fh.write(f"{id}:squad_id = {task.squad_id}\n")
        fh.write(f"{id}:requested_items = " + str(len(task.requested_items)) + "\n")

        for j, item in enumerate(task.requested_items):
            fh.write(f"{id}:item_id_{j} = {item.id}\n")
            fh.write(f"{id}:items_{j} = " + join(",", len(item.requested_items)) + "\n")

    def _export_CRecoverItemTask(self, fh, task, id):
        self._export_CGeneralTask(fh, task, id)
        fh.write(f"{id}:state = {task.state}\n")
        fh.write(f"{id}:squad_id = {task.squad_id}\n")
        fh.write(f"{id}:target_obj_id = {task.target_obj_id}\n")
        fh.write(f"{id}:presence_requested_item = {task.presence_requested_item}\n")
        fh.write(f"{id}:requested_item = {task.requested_item}\n")

    def _export_CFindUpgradeTask(self, fh, task, id):
        self._export_CGeneralTask(fh, task, id)
        fh.write(f"{id}:state = {task.state}\n")
        fh.write(f"{id}:presence_requested_item = {task.presence_requested_item}\n")
        fh.write(f"{id}:requested_item = {task.requested_item}\n")

    def _export_CHideFromSurgeTask(self, fh, task, id):
        self._export_CGeneralTask(fh, task, id)
        fh.write(f"{id}:target = {task.target}\n")
        fh.write(f"{id}:wait_time = {task.wait_time}\n")
        fh.write(f"{id}:effector_started_time = {task.effector_started_time}\n")

    def _export_CEliminateSquadTask(self, fh, task, id):
        self._export_CGeneralTask(fh, task, id)
        fh.write(f"{id}:target = {task.target}\n")
        fh.write(f"{id}:src_obj = {task.src_obj}\n")

    def _export_inited_find_upgrade_tasks(self, fh, container, p):

        count = len(container[p["name"]])
        fh.write("\n; inited 'find upgrade' tasks\n")
        fh.write(p["name"] + " = " + str(count) + "\n")
        for i, task in enumerate(container[p["name"]]):
            id = f"upgrade_task_{i}"
            fh.write(f"{id}:k = {task.k}\n")
            fh.write(f"{id}:subtasks = " + str(len(task.subtasks)) + "\n")

            for j, subtask in enumerate(task.subtasks):
                fh.write(f"{id}:kk_{j} = {subtask.kk}\n")
                fh.write(f"{id}:entity_id_{j} = {subtask.entity_id}\n")

    def _export_rewards(self, fh, container, p):
        count = len(container[p["name"]])
        fh.write("\n; rewards\n")
        fh.write(p["name"] + " = " + str(count) + "\n")

        for i, comm in enumerate(container[p["name"]]):
            id = f"community_{i}"
            fh.write(f"{id}:community_name = {comm.community}\n")
            fh.write(f"{id}:rewards = " + str(len(comm.rewards)) + "\n")
            for j, reward in enumerate(comm.rewards):
                if reward.is_money == 1:
                    fh.write(f"{id}:reward_{j}:money_amount = {reward.amount}\n")
                else:
                    fh.write(f"{id}:reward_{j}:item_name = {reward.item_name}\n")

        fh.write("\n")

    def _export_minigames(self, fh, container, p):
        count = len(container[p["name"]])
        fh.write("\n; minigames\n")
        fh.write(p["name"] + " = " + str(count) + "\n")
        for i, minigame in enumerate(container[p["name"]]):
            id = f"minigame_{i}"
            fh.write(f"{id}:key = {minigame.key}\n")
            fh.write(f"{id}:profile = {minigame.profile}\n")
            fh.write(f"{id}:state = {minigame.state}\n")
            if minigame.profile == "CMGCrowKiller":
                fh.write(f"{id}:param_highscore = {minigame.param_highscore}\n")
                fh.write(f"{id}:param_timer = {minigame.param_timer}\n")
                fh.write(f"{id}:param_win = {minigame.param_win}\n")
                fh.write(
                    f"{id}:param_crows_to_kill = ".join(
                        ",",
                        (minigame.param_crows_to_kill),
                    )
                    + "\n",
                )
                fh.write(
                    f"{id}:param_money_multiplier = {minigame.param_money_multiplier}\n",
                )
                fh.write(
                    f"{id}:param_champion_multiplier = {minigame.param_champion_multiplier}\n",
                )
                fh.write(f"{id}:param_selected = {minigame.param_selected}\n")
                fh.write(f"{id}:param_game_type = {minigame.param_game_type}\n")
                fh.write(f"{id}:high_score = {minigame.high_score}\n")
                fh.write(f"{id}:timer = {minigame.timer}\n")
                fh.write(f"{id}:time_out = {minigame.time_out}\n")
                fh.write(f"{id}:killed_counter = {minigame.killed_counter}\n")
                fh.write(f"{id}:win = {minigame.win}\n")
            elif minigame.profile == "CMGShooting":
                fh.write(f"{id}:param_game_type = {minigame.param_game_type}\n")
                fh.write(f"{id}:param_wpn_type = {minigame.param_wpn_type}\n")
                fh.write(f"{id}:param_stand_way = {minigame.param_stand_way}\n")
                fh.write(f"{id}:param_look_way = {minigame.param_look_way}\n")
                fh.write(
                    f"{id}:param_stand_way_back = {minigame.param_stand_way_back}\n",
                )
                fh.write(f"{id}:param_look_way_back = {minigame.param_look_way_back}\n")
                fh.write(f"{id}:param_obj_name = {minigame.param_obj_name}\n")
                fh.write(f"{id}:param_is_u16 = {minigame.param_is_u16}\n")
                if minigame.param_is_u16 == 0:
                    fh.write(f"{id}:param_win = {minigame.param_win}\n")
                else:
                    fh.write(f"{id}:param_win = {minigame.param_win}\n")

                fh.write(f"{id}:param_distance = {minigame.param_distance}\n")
                fh.write(f"{id}:param_ammo = {minigame.param_ammo}\n")
                fh.write(f"{id}:targets = " + str(len(minigame.targets)) + "\n")

                for j, target in enumerate(minigame.targets):
                    fh.write(f"{id}:target_{j} = " + join(",", target) + "\n")

                fh.write(
                    f"{id}:param_target_counter = {minigame.param_target_counter}\n",
                )
                fh.write(
                    f"{id}:inventory_items = ".join(",", (minigame.inventory_items))
                    + "\n",
                )
                fh.write(f"{id}:prev_time = {minigame.prev_time}\n")
                fh.write(f"{id}:type = {minigame.type}\n")

                if minigame.type == "training" or minigame.type == "points":
                    fh.write(f"{id}:win = {minigame.win}\n")
                    fh.write(f"{id}:ammo = {minigame.ammo}\n")
                    fh.write(f"{id}:cur_target = {minigame.cur_target}\n")
                    fh.write(f"{id}:points = {minigame.points}\n")
                    fh.write(f"{id}:ammo_counter = {minigame.ammo_counter}\n")
                elif minigame.type == "count":
                    fh.write(f"{id}:wpn_type = {minigame.wpn_type}\n")
                    fh.write(f"{id}:win = {minigame.win}\n")
                    fh.write(f"{id}:ammo = {minigame.ammo}\n")
                    fh.write(f"{id}:targets = " + str(len(minigame.targets)) + "\n")

                    for j, target in enumerate(minigame.targets):
                        fh.write(f"{id}:target_{j} = " + join(",", target) + "\n")

                    fh.write(f"{id}:distance = {minigame.distance}\n")
                    fh.write(f"{id}:cur_target = {minigame.cur_target}\n")
                    fh.write(f"{id}:points = {minigame.points}\n")
                    fh.write(f"{id}:scored = {minigame.scored}\n")
                    fh.write(f"{id}:ammo_counter = {minigame.ammo_counter}\n")
                elif minigame.type == "three_hit_training":
                    fh.write(f"{id}:wpn_type = {minigame.wpn_type}\n")
                    fh.write(f"{id}:win = {minigame.win}\n")
                    fh.write(f"{id}:ammo = {minigame.ammo}\n")
                    fh.write(f"{id}:targets = " + str(len(minigame.targets)) + "\n")

                    for j, target in enumerate(minigame.targets):
                        fh.write(f"{id}:target_{j} = " + join(",", target) + "\n")

                    fh.write(f"{id}:distance = {minigame.distance}\n")
                    fh.write(f"{id}:cur_target = {minigame.cur_target}\n")
                    fh.write(f"{id}:points = {minigame.points}\n")
                    fh.write(f"{id}:scored = {minigame.scored}\n")
                    fh.write(f"{id}:ammo_counter = {minigame.ammo_counter}\n")
                    fh.write(f"{id}:target_counter = {minigame.target_counter}\n")
                    fh.write(f"{id}:target_hit = {minigame.target_hit}\n")
                elif minigame.type == "all_targets":
                    fh.write(f"{id}:wpn_type = {minigame.wpn_type}\n")
                    fh.write(f"{id}:win = {minigame.win}\n")
                    fh.write(f"{id}:ammo = {minigame.ammo}\n")
                    fh.write(f"{id}:targets = " + str(len(minigame.targets)) + "\n")
                    fh.write(
                        f"{id}:hitted_targets = "
                        + str(len(minigame.hitted_targets))
                        + "\n",
                    )

                    for j, target in enumerate(minigame.targets):
                        fh.write(f"{id}:target_{j} = " + join(",", target) + "\n")

                    for j, target in enumerate(minigame.hitted_targets):
                        fh.write(
                            f"{id}:hitted_target_{j} = " + join(",", target) + "\n",
                        )

                    fh.write(f"{id}:ammo_counter = {minigame.ammo_counter}\n")
                    fh.write(f"{id}:time = {minigame.time}\n")
                    fh.write(f"{id}:target_counter = {minigame.target_counter}\n")
                    fh.write(f"{id}:prev_time = {minigame.prev_time}\n")
                    fh.write(f"{id}:more_targets = {minigame.more_targets}\n")
                    fh.write(f"{id}:last_target = {minigame.last_target}\n")
                elif minigame.type == "count_on_time":
                    fh.write(f"{id}:wpn_type = {minigame.wpn_type}\n")
                    fh.write(f"{id}:win = {minigame.win}\n")
                    fh.write(f"{id}:ammo = {minigame.ammo}\n")
                    fh.write(f"{id}:targets = " + str(len(minigame.targets)) + "\n")

                    for j, target in enumerate(minigame.targets):
                        fh.write(f"{id}:target_{j} = " + join(",", target) + "\n")

                    fh.write(f"{id}:distance = {minigame.distance}\n")
                    fh.write(f"{id}:cur_target = {minigame.cur_target}\n")
                    fh.write(f"{id}:points = {minigame.points}\n")
                    fh.write(f"{id}:ammo_counter = {minigame.ammo_counter}\n")
                    fh.write(f"{id}:time = {minigame.time}\n")
                    fh.write(f"{id}:prev_time = {minigame.prev_time}\n")
                elif minigame.type == "ten_targets":
                    fh.write(f"{id}:wpn_type = {minigame.wpn_type}\n")
                    fh.write(f"{id}:win = {minigame.win}\n")
                    fh.write(f"{id}:ammo = {minigame.ammo}\n")
                    fh.write(f"{id}:targets = " + str(len(minigame.targets)) + "\n")

                    for j, target in enumerate(minigame.targets):
                        fh.write(f"{id}:target_{j} = " + join(",", target) + "\n")

                    fh.write(f"{id}:distance = {minigame.distance}\n")
                    fh.write(f"{id}:cur_target = {minigame.cur_target}\n")
                    fh.write(f"{id}:points = {minigame.points}\n")
                    fh.write(f"{id}:scored = {minigame.scored}\n")
                    fh.write(f"{id}:ammo_counter = {minigame.ammo_counter}\n")
                    fh.write(f"{id}:time = {minigame.time}\n")
                    fh.write(f"{id}:prev_time = {minigame.prev_time}\n")
                elif minigame.type == "two_seconds_standing":
                    fh.write(f"{id}:wpn_type = {minigame.wpn_type}\n")
                    fh.write(f"{id}:win = {minigame.win}\n")
                    fh.write(f"{id}:ammo = {minigame.ammo}\n")
                    fh.write(f"{id}:targets = " + str(len(minigame.targets)) + "\n")
                    for j, target in enumerate(minigame.targets):
                        fh.write(f"{id}:target_{j} = " + join(",", target) + "\n")

                    fh.write(f"{id}:distance = {minigame.distance}\n")
                    fh.write(f"{id}:cur_target = {minigame.cur_target}\n")
                    fh.write(f"{id}:points = {minigame.points}\n")
                    fh.write(f"{id}:ammo_counter = {minigame.ammo_counter}\n")
                    fh.write(f"{id}:time = {minigame.time}\n")
                    fh.write(f"{id}:prev_time = {minigame.prev_time}\n")

            fh.write("\n")

    # import functions
    def import_properties(self, section, container, *props):
        if len(props) == 1 and isinstance(props[0], tuple):
            props = props[0]
        if self.sections_hash[section] is None:
            fail("section is undefined")
        # 	print "[section]\n";
        for p in props:
            # 	print "$p['name'] = ";
            value = self.value(section, p["name"])
            format = self.format_for_number.get(p["type"])
            if format is not None:
                self._import_scalar(value, container, p)
            elif p["type"] == "sz":
                self._import_string(value, container, p)
            elif p["type"] == "shape":
                self._import_shape(section, value, container, p)
            elif p["type"] == "skeleton":
                self._import_skeleton(section, value, container, p)
            elif p["type"] == "supplies":
                self._import_supplies(section, value, container, p)
            elif re.match("afspawns", p["type"]):
                self._import_artefact_spawns(section, value, container, p)
            elif p["type"] == "ordaf":
                self._import_ordered_artefacts(section, value, container, p)
            elif p["type"] == "CTime" or p["type"] == "complex_time":
                container[p["name"]] = self._import_ctime(value)
            elif p["type"] == "npc_info":
                value = int(value)
                self._import_npc_info(section, value, container, p)
            # SOC
            elif p["type"] == "jobs":
                self._import_jobs(section, value, container, p)
            # CS
            elif p["type"] == "covers":
                self._import_covers(section, value, container, p)
            elif p["type"] == "squads":
                self._import_squads(section, value, container, p)
            elif p["type"] == "sim_squads":
                self._import_sim_squads(section, value, container, p)
            elif p["type"] == "inited_tasks":
                self._import_inited_tasks(section, value, container, p)
            elif p["type"] == "inited_find_upgrade_tasks":
                self._import_inited_find_upgrade_tasks(section, value, container, p)
            elif p["type"] == "rewards":
                self._import_rewards(section, value, container, p)
            elif p["type"] == "minigames":
                self._import_minigames(section, value, container, p)
            # COP
            elif p["type"] == "times":
                value = int(value)
                self._import_times(section, value, container, p)
            else:
                self._import_vector(value, container, p)

    def _import_scalar(self, value, container, p):

        if value is not None:
            if re.match(r"^\s*0x", value):
                value = int(value, base=16)
            else:
                value = float(value) if ("." in value or "e" in value) else int(value)
            container[p["name"]] = value
        else:
            container[p["name"]] = p["default"]

    def _import_string(self, value, container, p):
        # my () = args;
        container[p["name"]] = value if (value is not None) else p["default"]

    def _import_vector(self, value, container, p):

        if re.match("dumb", p["type"]):
            container[p["name"]] = pack("H*", value)
        else:
            container[p["name"]] = re.split(r",\s*", value) if value else p["default"]
            if "f" in p["type"] or p["type"] == "sdir":
                container[p["name"]] = [float(val) for val in container[p["name"]]]
            elif "u" in p["type"] or "q" in p["type"]:
                container[p["name"]] = [int(val) for val in container[p["name"]]]

    def _import_shape(self, section, value, container, p):
        if value is None:
            fail(f"{p['name']} is undefined")  # unless defined $value;
        container[p["name"]] = []
        for i in range(int(value)):
            id = f"shape_{i}"
            shape = universal_dict_object()
            _type = self.value(section, f"{id}:type") or fail("no type in section\n")
            offset = self.value(section, f"{id}:offset")
            if _type == "sphere":
                radius = self.value(section, f"{id}:radius") or fail(
                    "no radius in section\n",
                )
                shape.type = 0
                shape.sphere = [float(f) for f in (*split(",", offset), radius)]
            elif _type == "box":
                shape.type = 1
                axis_x = self.value(section, f"{id}:axis_x") or fail(
                    "no axis_x in section\n",
                )
                axis_y = self.value(section, f"{id}:axis_y") or fail(
                    "no axis_y in section\n",
                )
                axis_z = self.value(section, f"{id}:axis_z") or fail(
                    "no axis_z in section\n",
                )
                shape.box = []
                shape.box.extend(map(float, split(",", axis_x)))
                shape.box.extend(map(float, split(",", axis_y)))
                shape.box.extend(map(float, split(",", axis_z)))
                shape.box.extend(map(float, split(",", offset)))
            else:
                fail("unknown shape type in section\n")

            container[p["name"]].append(shape)

    def _import_skeleton(self, section, value, container, p):

        container.bones_mas = split(r"/,\s*/", self.value(section, "bones_mask"))
        container.root_bone = self.value(section, "root_bone")
        container.bbox_min = split(r"/,\s*/", self.value(section, "bbox_min"))
        container.bbox_max = split(r"/,\s*/", self.value(section, "bbox_max"))
        count = self.value(section, "bones_count")
        for i in range(count):
            bone = universal_dict_object()
            (bone.ph_position) = split(
                r"/,\s*/",
                self.value(section, f"bone_{i}:ph_position"),
            )
            (bone.ph_rotation) = split(
                r"/,\s*/",
                self.value(section, f"bone_{i}:ph_rotation"),
            )
            bone.enabled = self.value(section, f"bone_{i}:enabled")
            container.bones.append(bone)

    def _import_supplies(self, section, value, container, p):
        if value is None or value == 0:
            return
        for i in range(value):
            item = universal_dict_object()
            item.section_name = self.value(section, f"sup_{i}:section_name")
            item.item_count = self.value(section, f"sup_{i}:item_count")
            item.min_factor = self.value(section, f"sup_{i}:min_factor")
            item.max_factor = self.value(section, f"sup_{i}:max_factor")
            (container[p["name"]]).append(item)

    def _import_artefact_spawns(self, section, value, container, p):
        if value is None or value == 0:
            return
        for i in range(value):
            item = universal_dict_object()
            item.section_name = self.value(section, f"art_{i}:section_name")
            item.weight = self.value(section, f"art_{i}:weight")
            (container[p["name"]]).append(item)

    def _import_ordered_artefacts(self, section, value, container, p):
        if value is None or value == 0:
            return
        for i in range(value):
            id = f"unknown_section_{i}"
            item = universal_dict_object()
            item.unknown_string = self.value(section, f"{id}:unknown_string")
            item.unknown_number = self.value(section, f"{id}:unknown_number")
            count = self.value(section, f"{id}:artefact_sections")
            for j in range(value):
                art = universal_dict_object()
                sID = f"{id}:artefact_section_{j}"
                art.artefact_name = self.value(section, f"{sID}:artefact_name")
                art.number_1 = self.value(section, f"{sID}:number_1")
                art.number_2 = self.value(section, f"{sID}:number_2")
                item.af_sects.append(art)

            (container[p["name"]]).append(item)

    def _import_ctime(self, value):
        if value is None:
            return 0
        time = split(r"/:\s*/", value)
        if time[0] != 255:
            time[0] -= 2000
        # _time = math.create('CTime')
        _time = CTime()
        _time.set(time)
        return _time

    def _import_jobs(self, section, value, container, p):
        if value is None or value == 0:
            return
        for i in range(value):
            job = universal_dict_object()
            job.job_begin = self.value(section, f"job_{i}:job_begin")
            job.job_fill_idle = self.value(section, f"job_{i}:job_fill_idle")
            job.job_idle_after_death_end = self.value(
                section,
                f"job_{i}:job_idle_after_death_end",
            )
            container[p["name"]].append(job)

    def _import_npc_info(self, section, value, container, p):
        if container.version >= 122:
            self._import_npc_info_cop(section, value, container, p)
        elif container.version >= 117:
            self._import_npc_info_soc(section, value, container, p)
        else:
            self._import_npc_info_old(section, value, container, p)

    def _import_npc_info_old(self, section, value, container, p):
        if value is None or value == 0:
            return
        for i in range(value):
            info = universal_dict_object()
            info.o_id = self.value(section, f"info_{i}:o_id")
            info.group = self.value(section, f"info_{i}:group")
            info.squad = self.value(section, f"info_{i}:squad")
            info.move_offline = self.value(section, f"info_{i}:move_offline")
            info.switch_offline = self.value(section, f"info_{i}:switch_offline")
            info.stay_end = self._import_ctime(
                self.value(section, f"info_{i}:stay_end"),
            )
            if container.script_version >= 1 and container.gulagN != 0:
                info.jobN = self.value(section, f"info_{i}:Object_didnt_begin_job")
            container[p["name"]].append(info)

    def _import_npc_info_soc(self, section, value, container, p):
        if value is None or value == 0:
            return
        for i in range(value):
            info = universal_dict_object()
            info.o_id = self.value(section, f"info_{i}:o_id")
            info.o_group = self.value(section, f"info_{i}:o_group")
            info.o_squad = self.value(section, f"info_{i}:o_squad")
            info.exclusive = self.value(section, f"info_{i}:exclusive")
            info.stay_end = self._import_ctime(
                self.value(section, f"info_{i}:stay_end"),
            )
            info.Object_begin_job = self.value(section, f"info_{i}:Object_begin_job")
            if container.script_version > 4:
                info.Object_didnt_begin_job = self.value(
                    section,
                    f"info_{i}:Object_didnt_begin_job",
                )
            info.jobN = self.value(section, f"info_{i}:jobN")
            container[p["name"]].append(info)

    def _import_npc_info_cop(self, section, value, container, p):
        if value is None or value == 0:
            return
        for i in range(value):
            info = universal_dict_object()
            info.id = self.value(section, f"info_{i}:id")
            info.job_prior = self.value(section, f"info_{i}:job_prior")
            info.job_id = self.value(section, f"info_{i}:job_id")
            info.begin_job = self.value(section, f"info_{i}:begin_job")
            info.need_job = self.value(section, f"info_{i}:need_job")
            container[p["name"]].append(info)

    def _import_covers(self, section, value, container, p):
        if value is None or value == 0:
            return
        for i in range(value):
            cover = universal_dict_object()
            cover.npc_id = self.value(section, f"cover_{i}:npc_id")
            cover.cover_vertex_id = self.value(section, f"cover_{i}:cover_vertex_id")
            (cover.cover_position) = split(
                r"/,\s*/",
                self.value(section, f"cover_{i}:cover_position"),
            )
            (cover.look_pos) = split(
                r"/,\s*/",
                self.value(section, f"cover_{i}:look_pos"),
            )
            cover.is_smart_cover = self.value(section, f"cover_{i}:is_smart_cover")
            container[p["name"]].append(cover)

    def _import_squads(self, section, value, container, p):
        if value is None or value == 0:
            return
        for i in range(value):
            squad = universal_dict_object()
            squad.squad_name = self.value(section, f"squad_{i}:squad_name")
            squad.squad_stage = self.value(section, f"squad_{i}:squad_stage")
            squad.squad_prepare_shouted = self.value(
                section,
                f"squad_{i}:squad_prepare_shouted",
            )
            squad.squad_attack_shouted = self.value(
                section,
                f"squad_{i}:squad_attack_shouted",
            )
            squad.squad_attack_squad = self.value(
                section,
                f"squad_{i}:squad_attack_squad",
            )
            squad.squad_inited_defend_time = self._import_ctime(
                self.value(section, f"squad_{i}:squad_inited_defend_time"),
            )
            squad.squad_start_attack_wait = self._import_ctime(
                self.value(section, f"squad_{i}:squad_start_attack_wait"),
            )
            squad.squad_last_defence_kill_time = self._import_ctime(
                self.value(section, f"squad_{i}:squad_last_defence_kill_time"),
            )
            squad.squad_power = self.value(section, f"squad_{i}:squad_power")
            container[p["name"]].append(squad)

    def _import_times(self, section, value, container, p):
        if value is None or value == 0:
            return
        for i in range(value):
            time = self._import_ctime(self.value(section, f"time_{i}"))
            container[p["name"]].append(time)

    def _import_sim_squads(self, section, value, container, p):
        if value is None or value == 0:
            return
        for i in range(value):
            squad = universal_dict_object()
            squad.squad_id = self.value(section, f"sim_squad_{i}:squad_id")
            squad.settings_id = self.value(section, f"sim_squad_{i}:settings_id")
            squad.is_scripted = self.value(section, f"sim_squad_{i}:is_scripted")
            if squad.is_scripted == 1:
                self._import_sim_squad_generic(section, squad, i)
                squad.continue_target = self.value(
                    section,
                    f"sim_squad_{i}:continue_target",
                )
                squad.need_free_update = self.value(
                    section,
                    f"sim_squad_{i}:need_free_update",
                )
                squad.relationship = self.value(section, f"sim_squad_{i}:relationship")
                squad.sympathy = self.value(section, f"sim_squad_{i}:sympathy")

            container[p["name"]].append(squad)

    def _import_sim_squad_generic(self, section, squad, i):

        squad.smart_id = self.value(section, f"sim_squad_{i}:smart_id")
        squad.assigned_target_smart_id = self.value(
            section,
            f"sim_squad_{i}:assigned_target_smart_id",
        )
        squad.sim_combat_id = self.value(section, f"sim_squad_{i}:sim_combat_id")
        squad.delayed_attack_task = self.value(
            section,
            f"sim_squad_{i}:delayed_attack_task",
        )
        (squad.random_tasks) = split(
            "/,/",
            self.value(section, f"sim_squad_{i}:random_tasks"),
        )
        squad.npc_count = self.value(section, f"sim_squad_{i}:npc_count")
        squad.squad_power = self.value(section, f"sim_squad_{i}:squad_power")
        squad.commander_id = self.value(section, f"sim_squad_{i}:commander_id")
        (squad.squad_npc) = split(
            "/,/",
            self.value(section, f"sim_squad_{i}:squad_npc"),
        )
        squad.spoted_shouted = self.value(section, f"sim_squad_{i}:spoted_shouted")
        squad.squad_power = self.value(section, f"sim_squad_{i}:squad_power")
        squad.last_action_timer = self._import_ctime(
            self.value(section, f"sim_squad_{i}:last_action_timer"),
        )
        squad.squad_attack_power = self.value(
            section,
            f"sim_squad_{i}:squad_attack_power",
        )
        squad["class"] = self.value(section, f"sim_squad_{i}:class")
        if squad["class"] is not None:
            if squad["class"] == 1:
                # sim_attack_point
                squad.dest_smrt_id = self.value(section, f"sim_squad_{i}:dest_smrt_id")
                squad.major = self.value(section, f"sim_squad_{i}:major")
                squad.target_power_value = self.value(
                    section,
                    f"sim_squad_{i}:target_power_value",
                )
            else:
                # sim_stay_point
                squad.stay_defended = self.value(
                    section,
                    f"sim_squad_{i}:stay_defended",
                )
                squad.continue_point_id = self.value(
                    section,
                    f"sim_squad_{i}:continue_point_id",
                )
                squad.begin_time = self._import_ctime(
                    self.value(section, f"sim_squad_{i}:begin_time"),
                )

        squad.items_spawned = self.value(section, f"sim_squad_{i}:items_spawned")
        squad.bring_item_inited_time = self._import_ctime(
            self.value(section, f"sim_squad_{i}:bring_item_inited_time"),
        )
        squad.recover_item_inited_time = self._import_ctime(
            self.value(section, f"sim_squad_{i}:recover_item_inited_time"),
        )

    def _import_inited_tasks(self, section, value, container, p):
        if value is None or value == 0:
            return
        for i in range(value):
            task = universal_dict_object()
            task.base_id = self.value(section, f"task_{i}:base_id")
            task.id = self.value(section, f"task_{i}:id")
            task.type = self.value(section, f"task_{i}:type")

            if task.type == 0 or task.type == 5:
                self._import_CStorylineTask(task, section, i)
            elif task.type == 1:
                self._import_CEliminateSmartTask(task, section, i)
            elif task.type == 2:
                self._import_CCaptureSmartTask(task, section, i)
            elif task.type == 3 or task.type == 4:
                self._import_CDefendSmartTask(task, section, i)
            elif task.type == 6:
                self._import_CBringItemTask(task, section, i)
            elif task.type == 7:
                self._import_CRecoverItemTask(task, section, i)
            elif task.type == 8:
                self._import_CFindUpgradeTask(task, section, i)
            elif task.type == 9:
                self._import_CHideFromSurgeTask(task, section, i)
            elif task.type == 10:
                self._import_CEliminateSquadTask(task, section, i)

            container[p["name"]].append(task)

    def _import_CGeneralTask(self, task, section, i):
        task.entity_id = self.value(section, f"task_{i}:entity_id")
        task.prior = self.value(section, f"task_{i}:prior")
        task.status = self.value(section, f"task_{i}:status")
        task.actor_helped = self.value(section, f"task_{i}:actor_helped")
        task.community = self.value(section, f"task_{i}:community")
        task.actor_come = self.value(section, f"task_{i}:actor_come")
        task.actor_ignore = self.value(section, f"task_{i}:actor_ignore")
        task.inited_time = self._import_ctime(
            self.value(section, f"task_{i}:inited_time"),
        )

    def _import_CStorylineTask(self, task, section, i):
        self._import_CGeneralTask(task, section, i)
        task.target = self.value(section, f"task_{i}:target")

    def _import_CEliminateSmartTask(self, task, section, i):
        self._import_CGeneralTask(task, section, i)
        task.target = self.value(section, f"task_{i}:target")
        task.src_obj = self.value(section, f"task_{i}:src_obj")
        task.faction = self.value(section, f"task_{i}:faction")

    def _import_CCaptureSmartTask(self, task, section, i):
        self._import_CGeneralTask(task, section, i)
        task.target = self.value(section, f"task_{i}:target")
        task.state = self.value(section, f"task_{i}:state")
        task.counter_attack_community = self.value(
            section,
            f"task_{i}:counter_attack_community",
        )
        task.counter_squad = self.value(section, f"task_{i}:counter_squad")
        task.src_obj = self.value(section, f"task_{i}:src_obj")
        task.faction = self.value(section, f"task_{i}:faction")

    def _import_CDefendSmartTask(self, task, section, i):
        self._import_CGeneralTask(task, section, i)
        task.target = self.value(section, f"task_{i}:target")
        task.last_called_time = self._import_ctime(
            self.value(section, f"task_{i}:last_called_time"),
        )

    def _import_CBringItemTask(self, task, section, i):
        self._import_CGeneralTask(task, section, i)
        task.target = self.value(section, f"task_{i}:target")
        task.state = self.value(section, f"task_{i}:state")
        task.ri_counter = self.value(section, f"task_{i}:ri_counter")
        task.squad_id = self.value(section, f"task_{i}:squad_id")
        count = self.value(section, f"task_{i}:requested_items")
        for j in range(count):
            item = universal_dict_object()
            item.id = self.value(section, f"task_{i}:item_id_{j}")
            (item.requested_items) = split(
                "/,/",
                self.value(section, f"task_{i}:items_{j}"),
            )
            task.requested_items.append(item)

    def _import_CRecoverItemTask(self, task, section, i):
        self._import_CGeneralTask(task, section, i)
        task.state = self.value(section, f"task_{i}:state")
        task.squad_id = self.value(section, f"task_{i}:squad_id")
        task.target_obj_id = self.value(section, f"task_{i}:target_obj_id")
        task.presence_requested_item = self.value(
            section,
            f"task_{i}:presence_requested_item",
        )
        task.requested_item = self.value(section, f"task_{i}:requested_item")

    def _import_CFindUpgradeTask(self, task, section, i):
        self._import_CGeneralTask(task, section, i)
        task.state = self.value(section, f"task_{i}:state")
        task.presence_requested_item = self.value(
            section,
            f"task_{i}:presence_requested_item",
        )
        task.requested_item = self.value(section, f"task_{i}:requested_item")

    def _import_CHideFromSurgeTask(self, task, section, i):
        self._import_CGeneralTask(task, section, i)
        task.target = self.value(section, f"task_{i}:target")
        task.wait_time = self.value(section, f"task_{i}:wait_time")
        task.effector_started_time = self.value(
            section,
            f"task_{i}:effector_started_time",
        )

    def _import_CEliminateSquadTask(self, task, section, i):
        self._import_CGeneralTask(task, section, i)
        task.target = self.value(section, f"task_{i}:target")
        task.src_obj = self.value(section, f"task_{i}:src_obj")

    def _import_inited_find_upgrade_tasks(self, section, value, container, p):

        if value is None or value == 0:
            return
        for i in range(value):
            task = universal_dict_object()
            task.k = self.value(section, f"task_{i}:k")
            count = self.value(section, f"task_{i}:subtasks")
            for j in range(count):
                subtask = universal_dict_object()
                subtask.k = self.value(section, f"task_{i}:kk_{j}")
                subtask.entity_id = self.value(section, f"task_{i}:entity_id_{j}")
                task.subtasks.append(subtask)

            container[p["name"]].append(task)

    def _import_rewards(self, section, value, container, p):

        if value is None or value == 0:
            return
        for i in range(value):
            comm = universal_dict_object()
            comm.community = self.value(section, f"community_{i}:community_name")
            count = self.value(section, f"community_{i}:rewards")
            for j in range(count):
                reward = universal_dict_object()
                if (
                    self.value(section, f"community_{i}:reward_{j}:money_amount")
                    is not None
                ):
                    reward.amount = self.value(
                        section,
                        f"community_{i}:reward_{j}:money_amount",
                    )
                else:
                    reward.item_name = self.value(
                        section,
                        f"community_{i}:reward_{j}:item_name",
                    )
                comm.rewards.append(reward)
            container[p["name"]].append(comm)

    def _import_minigames(self, section, value, container, p):

        if value is None or value == 0:
            return
        for i in range(value):
            minigame = universal_dict_object()
            minigame.key = self.value(section, f"minigame_{i}:key")
            minigame.profile = self.value(section, f"minigame_{i}:profile")
            minigame.state = self.value(section, f"minigame_{i}:state")
            if minigame.profile == "CMGCrowKiller":
                minigame.param_highscore = self.value(
                    section,
                    f"minigame_{i}:param_highscore",
                )
                minigame.param_timer = self.value(section, f"minigame_{i}:param_timer")
                minigame.param_win = self.value(section, f"minigame_{i}:param_win")
                (minigame.param_crows_to_kill) = split(
                    "/,/",
                    self.value(section, f"minigame_{i}:param_crows_to_kill"),
                )
                minigame.param_money_multiplier = self.value(
                    section,
                    f"minigame_{i}:param_money_multiplier",
                )
                minigame.param_champion_multiplier = self.value(
                    section,
                    f"minigame_{i}:param_champion_multiplier",
                )
                minigame.param_selected = self.value(
                    section,
                    f"minigame_{i}:param_selected",
                )
                minigame.param_game_type = self.value(
                    section,
                    f"minigame_{i}:param_game_type",
                )
                minigame.high_score = self.value(section, f"minigame_{i}:high_score")
                minigame.timer = self.value(section, f"minigame_{i}:timer")
                minigame.time_out = self.value(section, f"minigame_{i}:time_out")
                minigame.killed_counter = self.value(
                    section,
                    f"minigame_{i}:killed_counter",
                )
                minigame.win = self.value(section, f"minigame_{i}:win")
            elif minigame.profile == "CMGShooting":
                minigame.param_game_type = self.value(
                    section,
                    f"minigame_{i}:param_game_type",
                )
                minigame.param_wpn_type = self.value(
                    section,
                    f"minigame_{i}:param_wpn_type",
                )
                minigame.param_stand_way = self.value(
                    section,
                    f"minigame_{i}:param_stand_way",
                )
                minigame.param_look_way = self.value(
                    section,
                    f"minigame_{i}:param_look_way",
                )
                minigame.param_stand_way_back = self.value(
                    section,
                    f"minigame_{i}:param_stand_way_back",
                )
                minigame.param_look_way_back = self.value(
                    section,
                    f"minigame_{i}:param_look_way_back",
                )
                minigame.param_obj_name = self.value(
                    section,
                    f"minigame_{i}:param_obj_name",
                )
                minigame.param_is_u16 = self.value(
                    section,
                    f"minigame_{i}:param_is_u16",
                )
                minigame.param_win = self.value(section, f"minigame_{i}:param_win")
                minigame.param_distance = self.value(
                    section,
                    f"minigame_{i}:param_distance",
                )
                minigame.param_ammo = self.value(section, f"minigame_{i}:param_ammo")
                count = self.value(section, f"minigame_{i}:targets")
                for j in range(count):
                    minigame.targets.append(
                        split("/,/", self.value(section, f"minigame_{i}:target_{j}")),
                    )

                minigame.param_target_counter = self.value(
                    section,
                    f"minigame_{i}:param_target_counter",
                )
                (minigame.inventory_items) = split(
                    "/,/",
                    self.value(section, f"minigame_{i}:inventory_items"),
                )
                minigame.prev_time = self.value(section, f"minigame_{i}:prev_time")
                minigame.type = self.value(section, f"minigame_{i}:type")
                if minigame.type == "training" or minigame.type == "points":
                    minigame.win = self.value(section, f"minigame_{i}:win")
                    minigame.ammo = self.value(section, f"minigame_{i}:ammo")
                    minigame.cur_target = self.value(
                        section,
                        f"minigame_{i}:cur_target",
                    )
                    minigame.points = self.value(section, f"minigame_{i}:points")
                    minigame.ammo_counter = self.value(
                        section,
                        f"minigame_{i}:ammo_counter",
                    )
                    minigame.param_obj_name = self.value(
                        section,
                        f"minigame_{i}:param_obj_name",
                    )
                elif minigame.type == "count":
                    minigame.wpn_type = self.value(section, f"minigame_{i}:wpn_type")
                    minigame.win = self.value(section, f"minigame_{i}:win")
                    minigame.ammo = self.value(section, f"minigame_{i}:ammo")
                    count = self.value(section, f"minigame_{i}:targets")
                    for j in range(count):
                        minigame.targets.append(
                            split(
                                "/,/",
                                self.value(section, f"minigame_{i}:target_{j}"),
                            ),
                        )

                    minigame.distance = self.value(section, f"minigame_{i}:distance")
                    minigame.cur_target = self.value(
                        section,
                        f"minigame_{i}:cur_target",
                    )
                    minigame.points = self.value(section, f"minigame_{i}:points")
                    minigame.scored = self.value(section, f"minigame_{i}:scored")
                    minigame.ammo_counter = self.value(
                        section,
                        f"minigame_{i}:ammo_counter",
                    )
                elif minigame.type == "three_hit_training":
                    minigame.wpn_type = self.value(section, f"minigame_{i}:wpn_type")
                    minigame.win = self.value(section, f"minigame_{i}:win")
                    minigame.ammo = self.value(section, f"minigame_{i}:ammo")
                    count = self.value(section, f"minigame_{i}:targets")
                    for j in range(count):
                        minigame.targets.append(
                            split(
                                "/,/",
                                self.value(section, f"minigame_{i}:target_{j}"),
                            ),
                        )

                    minigame.distance = self.value(section, f"minigame_{i}:distance")
                    minigame.cur_target = self.value(
                        section,
                        f"minigame_{i}:cur_target",
                    )
                    minigame.points = self.value(section, f"minigame_{i}:points")
                    minigame.scored = self.value(section, f"minigame_{i}:scored")
                    minigame.ammo_counter = self.value(
                        section,
                        f"minigame_{i}:ammo_counter",
                    )
                    minigame.target_counter = self.value(
                        section,
                        f"minigame_{i}:target_counter",
                    )
                    minigame.target_hit = self.value(
                        section,
                        f"minigame_{i}:target_hit",
                    )
                elif minigame.type == "all_targets":
                    minigame.wpn_type = self.value(section, f"minigame_{i}:wpn_type")
                    minigame.win = self.value(section, f"minigame_{i}:win")
                    minigame.ammo = self.value(section, f"minigame_{i}:ammo")
                    count = self.value(section, f"minigame_{i}:targets")
                    for j in range(count):
                        minigame.targets.append(
                            split(
                                "/,/",
                                self.value(section, f"minigame_{i}:target_{j}"),
                            ),
                        )

                    count = self.value(section, f"minigame_{i}:hitted_targets")
                    for j in range(count):
                        minigame.hitted_targets.append(
                            split(
                                "/,/",
                                self.value(section, f"minigame_{i}:hitted_target_{j}"),
                            ),
                        )

                    minigame.ammo_counter = self.value(
                        section,
                        f"minigame_{i}:ammo_counter",
                    )
                    minigame.time = self.value(section, f"minigame_{i}:time")
                    minigame.target_counter = self.value(
                        section,
                        f"minigame_{i}:target_counter",
                    )
                    minigame.prev_time = self.value(section, f"minigame_{i}:prev_time")
                    minigame.more_targets = self.value(
                        section,
                        f"minigame_{i}:more_targets",
                    )
                    minigame.last_target = self.value(
                        section,
                        f"minigame_{i}:last_target",
                    )
                elif minigame.type == "count_on_time":
                    minigame.wpn_type = self.value(section, f"minigame_{i}:wpn_type")
                    minigame.win = self.value(section, f"minigame_{i}:win")
                    minigame.ammo = self.value(section, f"minigame_{i}:ammo")
                    count = self.value(section, f"minigame_{i}:targets")
                    for j in range(count):
                        minigame.targets.append(
                            split(
                                "/,/",
                                self.value(section, f"minigame_{i}:target_{j}"),
                            ),
                        )

                    minigame.distance = self.value(section, f"minigame_{i}:distance")
                    minigame.cur_target = self.value(
                        section,
                        f"minigame_{i}:cur_target",
                    )
                    minigame.points = self.value(section, f"minigame_{i}:points")
                    minigame.ammo_counter = self.value(
                        section,
                        f"minigame_{i}:ammo_counter",
                    )
                    minigame.time = self.value(section, f"minigame_{i}:time")
                    minigame.prev_time = self.value(section, f"minigame_{i}:prev_time")
                elif minigame.type == "ten_targets":
                    minigame.wpn_type = self.value(section, f"minigame_{i}:wpn_type")
                    minigame.win = self.value(section, f"minigame_{i}:win")
                    minigame.ammo = self.value(section, f"minigame_{i}:ammo")
                    count = self.value(section, f"minigame_{i}:targets")
                    for j in range(count):
                        minigame.targets.append(
                            split(
                                "/,/",
                                self.value(section, f"minigame_{i}:target_{j}"),
                            ),
                        )

                    minigame.distance = self.value(section, f"minigame_{i}:distance")
                    minigame.cur_target = self.value(
                        section,
                        f"minigame_{i}:cur_target",
                    )
                    minigame.points = self.value(section, f"minigame_{i}:points")
                    minigame.scored = self.value(section, f"minigame_{i}:scored")
                    minigame.ammo_counter = self.value(
                        section,
                        f"minigame_{i}:ammo_counter",
                    )
                    minigame.time = self.value(section, f"minigame_{i}:time")
                    minigame.prev_time = self.value(section, f"minigame_{i}:prev_time")
                elif minigame.type == "two_seconds_standing":
                    minigame.wpn_type = self.value(section, f"minigame_{i}:wpn_type")
                    minigame.win = self.value(section, f"minigame_{i}:win")
                    minigame.ammo = self.value(section, f"minigame_{i}:ammo")
                    count = self.value(section, f"minigame_{i}:targets")
                    for j in range(count):
                        minigame.targets.append(
                            split(
                                "/,/",
                                self.value(section, f"minigame_{i}:target_{j}"),
                            ),
                        )

                    minigame.distance = self.value(section, f"minigame_{i}:distance")
                    minigame.cur_target = self.value(
                        section,
                        f"minigame_{i}:cur_target",
                    )
                    minigame.points = self.value(section, f"minigame_{i}:points")
                    minigame.ammo_counter = self.value(
                        section,
                        f"minigame_{i}:ammo_counter",
                    )
                    minigame.time = self.value(section, f"minigame_{i}:time")
                    minigame.prev_time = self.value(section, f"minigame_{i}:prev_time")

            container[p["name"]].append(minigame)

    # various
    def comp_arrays(self, container, prop):
        eps = 0.0001
        if len(container[prop["name"]]) != len(prop["default"]):
            return 0
        if any(map(math.isnan, container[prop["name"]])):
            return 1
        zipped = zip(container[prop["name"]], prop["default"], strict=False)
        diff = lambda t: abs(t[0] - t[1])
        diffs = map(diff, zipped)
        return all(map(lambda a: a < eps, diffs))

    # (i, j) = (0, 0);
    # for (len(container[prop['name']])) {
    # 	$j++;
    # 	$i++ if abs($_ - $prop.default[$i]) < eps;
    # 	return 0 if $i != $j;

    # return 1;

    def value(self, section, name):
        if self.sections_hash.get(section) is None:
            fail("section is undefined")
        return self.sections_hash.get(section).get(name)

    def section_exists(self, key):
        return self.sections_hash[key] is not None

    def line_count(self, section):
        # my self = shift;
        # my (section) = args;
        if self.sections_hash[section] is None:
            fail("section is undefined")  # unless defined
        return len(self.sections_hash[section])

    # my $count = 0;
    # foreach (keys %{self.sections_hash[section]}) {
    # 	$count++;
    # }
    # return count;

    def section_safe(self, section):
        if self.sections_hash[section] is None:
            fail("section is undefined")  # unless defined self.sections_hash[section];
        return self.sections_hash[section]

    def section(self, arg):
        return self.sections_hash.get(arg)
