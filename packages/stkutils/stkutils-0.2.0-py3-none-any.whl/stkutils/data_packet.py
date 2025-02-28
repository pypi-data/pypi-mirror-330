# Module for packing and unpacking data
# Update history:
# 	26/08/2012 - fix for new fail() syntax
######################################################
import math
import re

from perl_binary_packing import unpack_with_length

from stkutils.binary_data import pack, unpack
from stkutils.perl_utils import chomp, fail, length, ref, substr, universal_dict_object
from stkutils.stkutils_math import stkutils_math


class data_packet:
    # use strict
    # use IO.File
    # use stkutils.debug qw(fail)
    # use stkutils.ini_file
    # use stkutils.math
    # use POSIX
    FL_IS_25XX = 0x08
    FL_HANDLED = 0x20
    SUCCESS_HANDLE = 2
    template_len = {
        "V": 4,
        "v": 2,
        "C": 1,
        "l": 4,
        "f": 4,
        "vf": 6,
        "v4": 8,
        "a[16]": 16,
        "C8": 8,
        "C4": 4,
        "f2": 8,
        "f3": 12,
        "f4": 16,
        "l3": 12,
        "l4": 16,
        "V2": 8,
        "V3": 12,
        "V4": 16,
        "a[12]": 12,
        "a[8]": 8,
        "a[169]": 169,
        "a[157]": 157,
        "a[153]": 153,
    }
    template_for_scalar = {
        "h8": "C",
        "h16": "v",
        "h32": "V",
        "u8": "C",
        "u16": "v",
        "u32": "V",
        "s8": "C",
        "s16": "v",
        "s32": "l",
        "q8": "C",
        "q16": "v",
        "q16_old": "v",
        "sz": "Z*",
        "f32": "f",
        "guid": "a[16]",
        "ha1": "a[12]",
        "ha2": "a[8]",
        "dumb_1": "a[169]",
        "dumb_2": "a[157]",
        "dumb_3": "a[153]",
    }
    template_for_vector = {
        "l8u8v": "C/C",
        "l8u16v": "C/v",
        "l8u32v": "C/V",
        "l8szv": "C/(Z*)",
        "l8szbv": "C/(Z*C)",
        "l8szu16v": "C/(Z*v)",
        "l8u16u8v": "C/(v*C)",
        "l8u16u16v": "C/(v*v)",
        "l16u16v": "v/v",
        "l32u8v": "V/C",
        "l32u16v": "V/v",
        "l32u32v": "V/V",
        "l32szv": "V/(Z*)",
        "u8v3": "C3",
        "u8v4": "C4",
        "u8v8": "C8",
        "u32v2": "V2",
        "u16v4": "v4",
        "f32v2": "f2",
        "f32v3": "f3",
        "f32v4": "f4",
        "s32v3": "l3",
        "s32v4": "l4",
        "h32v3": "V3",
        "h32v4": "V4",
        "q8v3": "C3",
        "q8v4": "C4",
        "sdir": "vf",
    }

    # function refs

    def sub_hash(self):
        return {
            "convert_q8": self.convert_q8,
            "convert_q16": self.convert_q16,
            "convert_q16_old": self.convert_q16_old,
            "convert_u8": self.convert_u8,
            "convert_u16": self.convert_u16,
            "convert_u16_old": self.convert_u16_old,
        }

    # constructor
    def __init__(self, data=b""):
        self.data = data
        self.init_length = length(self.data)
        self.pos = 0

    def DESTROY(*args, **kwargs):
        pass

    # undef args[0].data

    # unpack
    def unpack(self, template, template_len=None):
        # 	self = shift
        # 	template = shift
        fl = 0

        if "f" in template and "Z" not in template:
            fl = 1

        if self is None:
            fail("packet is not defined")

        if self.data is None:
            fail("there is no data in packet")

        if template is None:
            fail("template is not defined")
        values = None
        if template_len is None:
            unpack_res = unpack_with_length(template, self.data, self.pos)
            values = unpack_res.data
            self.pos += unpack_res.unpacked_bytes_length
            # values = unpack(template + "a*", substr(self.data, self.pos))
            # if not values:
            #     fail("cannot unpack requested data")
            # last_data = values.pop()
            # self.pos = length(self.data) - length(last_data)

        else:
            resid = length(self.data) - self.pos
            if template_len > resid:
                fail("data [resid] is shorter than template [args[2]]")
            unpack_res = unpack_with_length(
                template,
                substr(self.data, self.pos, template_len),
            )
            values = unpack_res.data
            if unpack_res.unpacked_bytes_length != template_len:
                fail("template_len is not equal to unpacked bytes length")
            self.pos += template_len

        if self.data is None:
            fail("data container is empty")
            # print "@values\n"
        if fl == 1:
            values = [
                0 if (self.isinf(val) or self.isnan(val)) else val for val in (values)
            ]
            fl = 0
        return values

    def unpack_properties(self, container, *args, **kwargs):
        if isinstance(args[0], (list, tuple)) and len(args) == 1:
            args = args[0]
        # self = shift
        # container = shift
        for p in args:
            # print "p["name"] = "

            template = self.template_for_scalar.get(p["type"], None)
            if p["type"] == "sz":
                self._unpack_string(container, p)
                continue
            if template is not None:
                self._unpack_scalar(template, container, p)
                if self.is_handled(container):
                    break
                continue
            if p["type"] == "u24":
                self._unpack_u24(container, p)
                continue
            if p["type"] == "shape":
                self._unpack_shape(container, p)
                continue
            if p["type"] == "skeleton":
                self._unpack_skeleton(container, p)
                continue
            if p["type"] == "supplies":
                self._unpack_supplies(container, p)
                continue
            if "afspawns" in p["type"]:
                self._unpack_artefact_spawns(container, p)
                continue
            if p["type"] == "ordaf":
                self._unpack_ordered_artefacts(container, p)
                continue
            if p["type"] == "CTime":
                container[p["name"]] = self.unpack_ctime()
                continue
            if p["type"] == "complex_time":
                container[p["name"]] = self._unpack_complex_time(container, p)
                if self.is_handled(container):
                    break
                continue

            if p["type"] == "npc_info":
                self._unpack_npc_info(container, p)
                continue
            if p["type"] == "sdir":
                self._unpack_sdir(container, p)
                if self.is_handled(container):
                    break
                continue
            # SOC
            if p["type"] == "jobs":
                self._unpack_jobs(container, p)
                continue
            # CS
            if p["type"] == "covers":
                self._unpack_covers(container, p)
                continue
            if p["type"] == "squads":
                self._unpack_squads(container, p)
                continue
            if p["type"] == "sim_squads":
                self._unpack_sim_squads(container, p)
                continue
            if p["type"] == "inited_tasks":
                self._unpack_inited_tasks(container, p)
                continue
            if p["type"] == "inited_find_upgrade_tasks":
                self._unpack_inited_find_upgrade_tasks(container, p)
                continue
            if p["type"] == "rewards":
                self._unpack_rewards(container, p)
                continue
            if p["type"] == "minigames":
                self._unpack_minigames(container, p)
                continue
            # COP
            if p["type"] == "times":
                self._unpack_times(container, p)
                continue
            self._unpack_vector(container, p)
            if self.is_handled(container):
                break

    def _unpack_scalar(self, template, container, p):
        # (self, template, container, p) = args
        if length(self.data) == self.pos or (
            self.template_len.get(template, None) is not None
            and self.resid() < self.template_len[template]
        ):
            self.error_handler(container, template)
        if self.is_handled(container):
            return
        (unpacked_value,) = self.unpack(template, self.template_len[template])
        container[p["name"]] = unpacked_value
        if "q" in p["type"]:
            func = "convert_" + p["type"]
            container[p["name"]] = self.sub_hash()[func](container[p["name"]], -1, 1)

    def _unpack_u24(self, container, p):
        # () = args
        (container[p["name"]],) = unpack("V", pack("CCCC", *self.unpack("C3", 3), 0))

    def _unpack_string(self, container, p):
        # () = args
        (unpacked,) = self.unpack("Z*")
        unpacked = chomp(unpacked)

        (container[p["name"]]) = unpacked
        container[p["name"]] = container[p["name"]].replace("\r", "")

    # chomp container[p["name"]]
    # container[p["name"]] =~ s/\r//g

    def _unpack_vector(self, container, p):
        # () = args
        template = self.template_for_vector[p["type"]]
        if length(self.data) == self.pos or (
            self.template_len.get(template, None) is not None
            and self.resid() < self.template_len[template]
        ):
            self.error_handler(container, template)
        if self.is_handled(container):
            return
        container[p["name"]] = self.unpack(
            template,
            self.template_len.get(template, None),
        )
        if rm := re.match(r"(q\d+)", p["type"]):
            _type = p["type"][rm.regs[0][0] : rm.regs[0][1]]
            # print(f"{_type=}")
            func = "convert_" + _type
            container[p["name"]] = [
                self.sub_hash()[func](tmp, -1, 1) for tmp in container[p["name"]]
            ]

    def _unpack_sdir(self, container, p):
        # () = args
        if length(self.data) == self.pos or self.resid() < 6:
            self.error_handler(container, "vf")
        if self.is_handled(container):
            return
        self._unpack_dir(container, p)
        (s,) = self.unpack("f", 4)
        container[p["name"]] = (item * s for item in container[p["name"]])
        # container[p["name"]][0] *= s
        # container[p["name"]][1] *= s
        # container[p["name"]][2] *= s

    def _unpack_dir(self, container, p):
        # () = args
        (t,) = self.unpack("v", 2)
        # (i, u, v)
        # (x, y, z)
        u = (t >> 7) & 0x3F
        v = t & 0x7F
        if u + v >= 0x7F:
            u = 0x7F - u
            v = 0x7F - v

        i = t & 0x1FFF
        self._prepare_uv_adjustment()
        x = self.uv_adjustment[i] * u
        y = self.uv_adjustment[i] * v
        j = 126 - u - v
        if j == 0:
            z = 0.0000000000001
        else:
            z = self.uv_adjustment[i] * j
        if t & 0x8000:
            x *= -1
        if t & 0x4000:
            y *= -1
        if t & 0x2000:
            z *= -1
        container[p["name"]] = (x, y, z)

    def _prepare_uv_adjustment(self):
        # (i, u, v)
        self.uv_adjustment = [0.0] * (0x2000 + 1)
        for i in range(0x2000 + 1):
            u = i >> 7
            v = i & 0x7F
            if u + v >= 0x7F:
                u = 0x7F - u
                v = 0x7F - v

            self.uv_adjustment[i] = 1.0 / math.sqrt(
                u * u + v * v + (126 - u - v) * (126 - u - v),
            )

    def _unpack_shape(self, container, p):
        # () = args
        (count,) = self.unpack("C", 1)
        if getattr(container, p["name"], None) is None:
            container[p["name"]] = []
        while count > 0:
            count -= 1
            shape = universal_dict_object()
            (shape["type"],) = self.unpack("C", 1)
            if shape["type"] == 0:
                shape["sphere"] = self.unpack("f4", 16)
            elif shape["type"] == 1:
                shape["box"] = self.unpack("f12", 48)
            else:
                fail(f"shape has undefined type ({shape['type']})")

            container[p["name"]].append(shape)

    def _unpack_skeleton(self, container, p):
        # () = args
        container.bones_mask = self.unpack("C8", 8)
        (container.root_bone,) = self.unpack("v", 2)
        container.bbox_min = self.unpack("f3", 12)
        container.bbox_max = self.unpack("f3", 12)
        (count,) = self.unpack("v", 2)
        while count > 0:
            count -= 1
            bone = universal_dict_object()
            bone["ph_position"] = self.unpack("C3", 3)
            # i = 0
            for i in range(len(bone.ph_position)):
                bone.ph_position[i] = self.convert_q8(
                    bone.ph_position[i],
                    container.bbox_min[i],
                    container.bbox_max[i],
                )
            # i++

            bone.ph_rotation = self.unpack("C4", 4)
            for i in range(len(bone.ph_rotation)):
                bone.ph_rotation[i] = self.convert_q8(bone.ph_rotation[i], -1, 1)

            (bone.enabled) = self.unpack("C", 1)
            container.bones.append(bone)

    def _unpack_supplies(self, container, p):
        # () = args
        (count,) = self.unpack("V", 4)
        while count > 0:
            count -= 1
            obj = universal_dict_object()
            (obj.section_name,) = self.unpack("Z*")
            (obj.item_count, obj.min_factor, obj.max_factor) = self.unpack("Vff", 12)
            container[p["name"]].append(obj)

    def _unpack_artefact_spawns(self, container, p):
        # () = args
        (count,) = self.unpack("v", 2)
        while count > 0:
            count -= 1
            obj = universal_dict_object()
            (obj.section_name) = self.unpack("Z*")
            if p["type"] == "afspawns":
                (obj.weight,) = self.unpack("f", 4)
            else:
                (obj.weight,) = self.unpack("V", 4)

            container[p["name"]].append(obj)

    def _unpack_ordered_artefacts(self, container, p):
        # () = args
        (count,) = self.unpack("V", 4)
        while count > 0:
            count -= 1
            obj = universal_dict_object()
            (obj.unknown_string) = self.unpack("Z*")
            (obj.unknown_number) = self.unpack("V", 4)
            (inner_count,) = self.unpack("V", 4)
            while inner_count > 0:
                inner_count -= 1
                afs = universal_dict_object()
                (afs.artefact_name) = self.unpack("Z*")
                (afs.number_1, afs.number_2) = self.unpack("VV", 8)
                obj.af_sects.append(afs)

            container[p["name"]].append(obj)

    def unpack_ctime(self):
        # (self) = args
        time = stkutils_math.create("CTime")
        (year,) = self.unpack("C", 1)
        if year != 0 and year != 255:
            time.set(year, self.unpack("C5v", 7))
        else:
            time.set(year)

        return time

    def _unpack_complex_time(self, container, p):
        # () = args
        if length(self.data) == self.pos or (self.resid() < 1):
            self.error_handler(container, "C")
        if self.is_handled(container):
            return None
        (flag,) = self.unpack("C", 1)
        if flag != 0:
            return self.unpack_ctime()
        return 0

    def _unpack_jobs(self, container, p):
        # () = args
        (count,) = self.unpack("C", 1)
        while count > 0:
            count -= 1
            job = universal_dict_object()
            (job.job_begin, job.job_fill_idle, job.job_idle_after_death_end) = (
                self.unpack("VVV", 12)
            )
            container[p["name"]].append(job)

    def _unpack_npc_info(self, *args):
        # self = shift
        if args[0].version >= 122:
            self._unpack_npc_info_cop(*args)
        elif args[0].version >= 117:
            self._unpack_npc_info_soc(*args)
        else:
            self._unpack_npc_info_old(*args)

    def _unpack_npc_info_old(self, container, p):
        # () = args
        (count,) = self.unpack("C", 1)
        while count > 0:
            count -= 1
            info = universal_dict_object()
            (
                info.o_id,
                info.group,
                info.squad,
                info.move_offline,
                info.switch_offline,
            ) = self.unpack("vCCCC", 6)
            info.stay_end = self.unpack_ctime()
            if container.script_version >= 1 and container.gulagN != 0:
                (info.jobN,) = self.unpack("C", 1)
            container[p["name"]].append(info)

    def _unpack_npc_info_soc(self, container, p):
        # () = args
        (count,) = self.unpack("C", 1)
        while count > 0:
            count -= 1
            info = universal_dict_object()
            (info.o_id, info.o_group, info.o_squad, info.exclusive) = self.unpack(
                "vCCC",
                5,
            )
            info.stay_end = self.unpack_ctime()
            (info.Object_begin_job,) = self.unpack("C", 1)
            if container.script_version > 4:
                (info.Object_didnt_begin_job,) = self.unpack("C", 1)
            (info.jobN) = self.unpack("C", 1)
            container[p["name"]].append(info)

    def _unpack_npc_info_cop(self, container, p):
        # () = args
        (count,) = self.unpack("C", 1)
        while count > 0:
            count -= 1
            info = universal_dict_object()
            (info.id, info.job_prior, info.job_id, info.begin_job, info.need_job) = (
                self.unpack("vCCCZ*")
            )
            container[p["name"]].append(info)

    def _unpack_covers(self, container, p):
        # () = args
        (count,) = self.unpack("C", 1)
        while count > 0:
            count -= 1
            cover = universal_dict_object()
            (cover.npc_id, cover.cover_vertex_id) = self.unpack("vV", 6)
            cover.cover_position = self.unpack("f3", 12)
            cover.look_pos = self.unpack("f3", 12)
            (cover.is_smart_cover) = self.unpack("C", 1)
            container[p["name"]].append(cover)

    def _unpack_squads(self, container, p):
        # () = args
        (count,) = self.unpack("C", 1)
        while count > 0:
            count -= 1

            squad = universal_dict_object()
            (
                squad.squad_name,
                squad.squad_stage,
                squad.squad_prepare_shouted,
                squad.squad_attack_shouted,
                squad.squad_attack_squad,
            ) = self.unpack("Z*Z*CCC")
            squad.squad_inited_defend_time = self._unpack_complex_time()
            squad.squad_start_attack_wait = self._unpack_complex_time()
            squad.squad_last_defence_kill_time = self._unpack_complex_time()
            (squad.squad_power,) = self.unpack("f", 4)
            container[p["name"]].append(squad)

    def _unpack_sim_squads(self, container, p):
        # () = args
        (count,) = self.unpack("v", 2)
        while count > 0:
            count -= 1
            squad = universal_dict_object()
            (squad.squad_id, squad.settings_id, squad.is_scripted) = self.unpack(
                "Z*Z*C",
            )
            self._unpack_sim_squad_generic(container, squad)
            if squad.is_scripted == 1:
                self.set_save_marker(container, "load", 0, "sim_squad_scripted")
                (
                    squad.continue_target,
                    squad.need_free_update,
                    squad.relationship,
                    squad.sympathy,
                ) = self.unpack("CCCC", 4)
                self.set_save_marker(container, "load", 1, "sim_squad_scripted")

            container[p["name"]].append(squad)

    def _unpack_sim_squad_generic(self, container, squad):
        # () = args
        self.set_save_marker(container, "load", 0, "sim_squad_generic")
        (
            squad.smart_id,
            squad.assigned_target_smart_id,
            squad.sim_combat_id,
            squad.delayed_attack_task,
        ) = self.unpack("vvvv", 8)
        squad.random_tasks = self.unpack("C/(vv)")
        (squad.npc_count, squad.squad_power, squad.commander_id) = self.unpack("Cfv", 7)
        squad.squad_npc = self.unpack("C/v")
        (squad.spoted_shouted) = self.unpack("C", 1)
        squad.last_action_timer = self.unpack_ctime()
        (squad.squad_attack_power) = self.unpack("v", 2)
        (flag,) = self.unpack("C", 1)
        if flag == 1:
            (squad._class) = self.unpack("C", 1)
            if squad._class == 1:
                # sim_attack_point
                (squad.dest_smrt_id) = self.unpack("v", 2)
                self.set_save_marker(container, "load", 0, "sim_attack_point")
                (squad.major, squad.target_power_value) = self.unpack("Cv", 3)
                self.set_save_marker(container, "load", 1, "sim_attack_point")
            else:
                # sim_stay_point
                self.set_save_marker(container, "load", 0, "sim_stay_point")
                (squad.stay_defended, squad.continue_point_id) = self.unpack("Cv", 3)
                squad.begin_time = self._unpack_complex_time()
                self.set_save_marker(container, "load", 1, "sim_stay_point")

        (squad.items_spawned) = self.unpack("C", 1)
        squad.bring_item_inited_time = self.unpack_ctime()
        squad.recover_item_inited_time = self.unpack_ctime()
        self.set_save_marker(container, "load", 1, "sim_squad_generic")

    def _unpack_times(self, container, p):
        # () = args
        (count,) = self.unpack("C", 1)
        while count > 0:
            count -= 1
            time = self._unpack_complex_time()
            container[p["name"]].append(time)

    def _unpack_inited_find_upgrade_tasks(self, container, p):
        # () = args
        (count,) = self.unpack("v", 2)
        while count > 0:
            count -= 1
            task = universal_dict_object()
            (task.k,) = self.unpack("v", 2)
            (num,) = self.unpack("v", 2)
            while num > 0:
                count -= 1
                subtask = universal_dict_object()
                (subtask.kk, subtask.entity_id) = self.unpack("Z*v")
                task.subtasks.append(subtask)

            container[p["name"]].append(task)

    def _unpack_rewards(self, container, p):
        # () = args
        (count,) = self.unpack("C", 1)
        while count > 0:
            count -= 1
            comm = universal_dict_object()
            (comm.community) = self.unpack("Z*")
            (num,) = self.unpack("C", 1)
            while num > 0:
                num -= 1
                reward = universal_dict_object()
                (reward.is_money) = self.unpack("C", 1)
                if reward.is_money == 1:
                    (reward.amount) = self.unpack("v", 2)
                else:
                    (reward.item_name) = self.unpack("Z*")

                comm.rewards.append(reward)

            container[p["name"]].append(comm)

    def _unpack_CGeneralTask(self, task, container):
        # () = args
        self.set_save_marker(container, "load", 0, "CGeneralTask")
        (
            task.entity_id,
            task.prior,
            task.status,
            task.actor_helped,
            task.community,
            task.actor_come,
            task.actor_ignore,
        ) = self.unpack("vCCCZ*CC")
        task.inited_time = self.unpack_ctime()
        self.set_save_marker(container, "load", 1, "CGeneralTask")

    def _unpack_CStorylineTask(self, task, container):
        # () = args
        self.set_save_marker(container, "load", 0, "CStorylineTask")
        self._unpack_CGeneralTask(task, container)
        (task.target) = self.unpack("V", 4)
        self.set_save_marker(container, "load", 1, "CStorylineTask")

    def _unpack_CEliminateSmartTask(self, task, container):
        # () = args
        self.set_save_marker(container, "load", 0, "CEliminateSmartTask")
        self._unpack_CGeneralTask(task, container)
        (task.target, task.src_obj, task.faction) = self.unpack("vZ*Z*")
        self.set_save_marker(container, "load", 1, "CEliminateSmartTask")

    def _unpack_CCaptureSmartTask(self, task, container):
        # () = args
        self.set_save_marker(container, "load", 0, "CCaptureSmartTask")
        self._unpack_CGeneralTask(task, container)
        (
            task.target,
            task.state,
            task.counter_attack_community,
            task.counter_squad,
            task.src_obj,
            task.faction,
        ) = self.unpack("vZ*Z*Z*Z*Z*")
        self.set_save_marker(container, "load", 1, "CCaptureSmartTask")

    def _unpack_CDefendSmartTask(self, task, container):
        # () = args
        self.set_save_marker(container, "load", 0, "CDefendSmartTask")
        self._unpack_CGeneralTask(task, container)
        (task.target) = self.unpack("v")
        task.last_called_time = self.unpack_ctime()
        self.set_save_marker(container, "load", 1, "CDefendSmartTask")

    def _unpack_CBringItemTask(self, task, container):
        # () = args
        self.set_save_marker(container, "load", 0, "CBringItemTask")
        self._unpack_CGeneralTask(task, container)
        (task.state, task.ri_counter, task.target, task.squad_id) = self.unpack(
            "Z*CvZ*",
        )
        (num,) = self.unpack("C", 1)
        while num > 0:
            num -= 1
            requested_item = universal_dict_object()
            (requested_item.id) = self.unpack("Z*")
            requested_item.items = self.unpack("v/C")
            task.requested_items.append(requested_item)

        self.set_save_marker(container, "load", 1, "CBringItemTask")

    def _unpack_CRecoverItemTask(self, task, container):
        # () = args
        self.set_save_marker(container, "load", 0, "CRecoverItemTask")
        self._unpack_CGeneralTask(task, container)
        (
            task.state,
            task.squad_id,
            task.target_obj_id,
            task.presence_requested_item,
            task.requested_item,
        ) = self.unpack("CZ*vCZ*")
        self.set_save_marker(container, "load", 1, "CRecoverItemTask")

    def _unpack_CFindUpgradeTask(self, task, container):
        # () = args
        self.set_save_marker(container, "load", 0, "CFindUpgradeTask")
        self._unpack_CGeneralTask(task, container)
        (task.state, task.presence_requested_item, task.requested_item) = self.unpack(
            "Z*CZ*",
        )
        self.set_save_marker(container, "load", 1, "CFindUpgradeTask")

    def _unpack_CHideFromSurgeTask(self, task, container):
        # () = args
        self.set_save_marker(container, "load", 0, "CHideFromSurgeTask")
        self._unpack_CGeneralTask(task, container)
        (task.target, task.wait_time, task.effector_started_time) = self.unpack(
            "vvv",
            12,
        )
        self.set_save_marker(container, "load", 1, "CHideFromSurgeTask")

    def _unpack_CEliminateSquadTask(self, task, container):
        # () = args
        self.set_save_marker(container, "load", 0, "CEliminateSquadTask")
        self._unpack_CGeneralTask(task, container)
        (task.target, task.src_obj) = self.unpack("vZ*")
        self.set_save_marker(container, "load", 1, "CEliminateSquadTask")

    def _unpack_inited_tasks(self, container, p):
        # () = args
        (count,) = self.unpack("v", 2)
        while count > 0:
            count -= 1
            task = universal_dict_object()
            (task.base_id, task.id, task.type) = self.unpack("Z*Z*v")
            if task.type == 0 or task.type == 5:
                self._unpack_CStorylineTask(task, container)
            if task.type == 1:
                self._unpack_CEliminateSmartTask(task, container)
            if task.type == 2:
                self._unpack_CCaptureSmartTask(task, container)
            if task.type == 3 or task.type == 4:
                self._unpack_CDefendSmartTask(task, container)
            if task.type == 6:
                self._unpack_CBringItemTask(task, container)
            if task.type == 7:
                self._unpack_CRecoverItemTask(task, container)
            if task.type == 8:
                self._unpack_CFindUpgradeTask(task, container)
            if task.type == 9:
                self._unpack_CHideFromSurgeTask(task, container)
            if task.type == 10:
                self._unpack_CEliminateSquadTask(task, container)

        container[p["name"]].append(task)

    def _unpack_minigames(self, container, p):
        # () = args
        (count,) = self.unpack("v", 2)
        while count > 0:
            count -= 1
            minigame = universal_dict_object()
            (minigame.key, minigame.profile, minigame.state) = self.unpack("Z*Z*Z*")
            if minigame.profile == "CMGCrowKiller":
                self.set_save_marker(container, "load", 0, "CMGCrowKiller")
                (minigame.param_highscore, minigame.param_timer, minigame.param_win) = (
                    self.unpack("CvC", 4)
                )
                minigame.param_crows_to_kill = self.unpack("C/C")
                (
                    minigame.param_money_multiplier,
                    minigame.param_champion_multiplier,
                    minigame.param_selected,
                    minigame.param_game_type,
                    minigame.high_score,
                    minigame.timer,
                    minigame.time_out,
                    minigame.killed_counter,
                    minigame.win,
                ) = self.unpack("vvCZ*CvvCC")
                self.set_save_marker(container, "load", 1, "CMGCrowKiller")
            elif minigame.profile == "CMGShooting":
                self.set_save_marker(container, "load", 0, "CMGShooting")
                (
                    minigame.param_game_type,
                    minigame.param_wpn_type,
                    minigame.param_stand_way,
                    minigame.param_look_way,
                    minigame.param_stand_way_back,
                    minigame.param_look_way_back,
                    minigame.param_obj_name,
                ) = self.unpack("Z*Z*Z*Z*Z*Z*Z*")
                (minigame.param_is_u16) = self.unpack("C", 1)
                if minigame.param_is_u16 == 0:
                    (minigame.param_win) = self.unpack("C", 1)
                else:
                    (minigame.param_win) = self.unpack("v", 2)

                (minigame.param_distance, minigame.param_ammo) = self.unpack("CC", 2)
                (count2,) = self.unpack("C", 1)
                while count2 > 0:
                    count2 -= 1
                    target = self.unpack("C/(Z*)")
                    minigame.targets.append(target)

                (minigame.param_target_counter) = self.unpack("C", 1)
                minigame.inventory_items = self.unpack("C/v")
                (minigame.prev_time, minigame.type) = self.unpack("VZ*")
                if minigame.type == "training" or minigame.type == "points":
                    self.set_save_marker(container, "load", 0, minigame.type)
                    (
                        minigame.win,
                        minigame.ammo,
                        minigame.cur_target,
                        minigame.points,
                        minigame.ammo_counter,
                    ) = self.unpack("vvZ*vC")
                    self.set_save_marker(container, "load", 1, minigame.type)
                elif minigame.type == "count":
                    self.set_save_marker(container, "load", 0, minigame.type)
                    (minigame.wpn_type, minigame.win, minigame.ammo) = self.unpack(
                        "Z*CC",
                    )
                    (count3,) = self.unpack("C", 1)
                    while count3 > 0:
                        count3 -= 1
                        target = self.unpack("C/(Z*)")
                        minigame.targets.append(target)

                    (
                        minigame.distance,
                        minigame.cur_target,
                        minigame.points,
                        minigame.scored,
                        minigame.ammo_counter,
                    ) = self.unpack("CZ*CCC")
                    self.set_save_marker(container, "load", 1, minigame.type)
                elif minigame.type == "three_hit_training":
                    self.set_save_marker(container, "load", 0, minigame.type)
                    (minigame.wpn_type, minigame.win, minigame.ammo) = self.unpack(
                        "Z*vC",
                    )
                    (count4,) = self.unpack("C", 1)
                    while count4 > 0:
                        count4 -= 1
                        target = self.unpack("C/(Z*)")
                        minigame.targets.append(target)

                    (
                        minigame.distance,
                        minigame.cur_target,
                        minigame.points,
                        minigame.scored,
                        minigame.ammo_counter,
                        minigame.target_counter,
                        minigame.target_hit,
                    ) = self.unpack("CZ*vCCCC")
                    self.set_save_marker(container, "load", 1, minigame.type)
                elif minigame.type == "all_targets":
                    self.set_save_marker(container, "load", 0, minigame.type)
                    (minigame.wpn_type, minigame.win, minigame.ammo) = self.unpack(
                        "Z*vC",
                    )
                    (count,) = self.unpack("C", 1)
                    while count > 0:
                        count -= 1
                        minigame.targets.append(self.unpack("C/(Z*)"))
                        minigame.hitted_targets.append(self.unpack("C/(CZ*)"))

                    (
                        minigame.ammo_counter,
                        minigame.time,
                        minigame.target_counter,
                        minigame.prev_time,
                        minigame.more_targets,
                        minigame.last_target,
                    ) = self.unpack("CvCVCZ*")
                    self.set_save_marker(container, "load", 1, minigame.type)
                elif minigame.type == "count_on_time":
                    self.set_save_marker(container, "load", 0, minigame.type)
                    (minigame.wpn_type, minigame.win, minigame.ammo) = self.unpack(
                        "Z*CC",
                    )
                    (count,) = self.unpack("C", 1)
                    while count > 0:
                        count -= 1
                        minigame.targets.append(self.unpack("C/(Z*)"))

                    (
                        minigame.distance,
                        minigame.cur_target,
                        minigame.points,
                        minigame.scored,
                        minigame.ammo_counter,
                        minigame.time,
                        minigame.prev_time,
                    ) = self.unpack("CZ*CCCCV")
                    self.set_save_marker(container, "load", 1, minigame.type)
                elif minigame.type == "ten_targets":
                    self.set_save_marker(container, "load", 0, minigame.type)
                    (minigame.wpn_type, minigame.win, minigame.ammo) = self.unpack(
                        "Z*CC",
                    )
                    (count,) = self.unpack("C", 1)
                    while count > 0:
                        count -= 1
                        minigame.targets.append(self.unpack("C/(Z*)"))

                    (
                        minigame.distance,
                        minigame.cur_target,
                        minigame.points,
                        minigame.scored,
                        minigame.ammo_counter,
                        minigame.time,
                        minigame.prev_time,
                    ) = self.unpack("CZ*CCCvV")
                    self.set_save_marker(container, "load", 1, minigame.type)
                elif minigame.type == "two_seconds_standing":
                    self.set_save_marker(container, "load", 0, minigame.type)
                    (minigame.wpn_type, minigame.win, minigame.ammo) = self.unpack(
                        "Z*CC",
                    )
                    (count,) = self.unpack("C", 1)
                    while count > 0:
                        count -= 1
                        minigame.targets.append(self.unpack("C/(Z*)"))

                    (
                        minigame.distance,
                        minigame.cur_target,
                        minigame.points,
                        minigame.ammo_counter,
                        minigame.time,
                        minigame.prev_time,
                    ) = self.unpack("CZ*CCCV")
                    self.set_save_marker(container, "load", 1, minigame.type)

                self.set_save_marker(container, "load", 1, "CMGShooting")

            container[p["name"]].append(minigame)

    # pack
    def pack(self, template: str, *args):
        # self = shift
        # template = shift
        if template is None:
            fail("template is not defined")  # if !(defined template)
        if not args:
            fail("data is not defined")  # if !(args)
        # fail("packet is not defined") unless defined self
        # 	print "args\n"
        self.data += pack(template, *args)

    def pack_properties(self, container, *args):
        # self = shift
        # container = shift
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]

        for p in args:
            try:
                self._pack_property(container, p)
            except Exception as e:
                raise ValueError(f"Error pack {p=}") from e

    def _pack_property(self, container, p):
        # print "p["name"] = "
        template = self.template_for_scalar.get(p["type"], None)
        if template:
            self._pack_scalar(template, container, p)
        # defined template				and do { continue}
        elif p["type"] == "u24":
            self._pack_u24(container, p)
        elif p["type"].startswith("l"):
            self._pack_complex(container, p)
        elif p["type"] == "shape":
            self._pack_shape(container, p)
        elif p["type"] == "skeleton":
            self._pack_skeleton(container, p)
        elif p["type"] == "supplies":
            self._pack_supplies(container, p)
        elif p["type"].startswith("afspawns"):
            self._pack_artefact_spawns(container, p)
        elif p["type"] == "ordaf":
            self._pack_ordered_artefacts(container, p)
        elif p["type"] == "CTime":
            self._pack_ctime(container[p["name"]])
        elif p["type"] == "complex_time":
            self._pack_complex_time(container[p["name"]])
        elif p["type"] == "npc_info":
            self._pack_npc_info(container, p)
        elif p["type"] == "sdir":
            self._pack_sdir(container, p)
        # SOC
        elif p["type"] == "jobs":
            self._pack_jobs(container, p)
        # CS
        elif p["type"] == "covers":
            self._pack_covers(container, p)
        elif p["type"] == "squads":
            self._pack_squads(container, p)
        elif p["type"] == "sim_squads":
            self._pack_sim_squads(container, p)
        elif p["type"] == "inited_tasks":
            self._pack_inited_tasks(container, p)
        elif p["type"] == "inited_find_upgrade_tasks":
            self._pack_inited_find_upgrade_tasks(container, p)
        elif p["type"] == "rewards":
            self._pack_rewards(container, p)
        elif p["type"] == "minigames":
            self._pack_minigames(container, p)
        # COP
        elif p["type"] == "times":
            self._pack_times(container, p)
        else:
            self._pack_vector(container, p)

    def _pack_scalar(self, template, container, p):
        # () = args
        if p["type"].startswith("q"):  # re.match("q(.*)", #)):
            func = "convert_u" + p["type"][1:]
            converted = self.sub_hash()[func](container[p["name"]], -1, 1)
            if abs(converted - int(converted)) < 1e-4:
                converted = int(converted)
            else:
                raise ValueError(f"int({converted}) != {converted}")
            container[p["name"]] = converted

        self.pack(template, container[p["name"]])

    def _pack_u24(self, container, p):
        # () = args
        self.pack("CCC", unpack("CCCC", pack("V", container[p["name"]])))

    def _pack_complex(*args, **kwargs):
        (self, container, p) = args
        n: int = len(container[p["name"]])
        if p["type"] == "l8u8v":
            self.pack(f"CC{n}", n, *container[p["name"]])
        elif p["type"] == "l8u16v":
            self.pack(f"Cv{n}", n, *container[p["name"]])
        elif p["type"] == "l8u32v":
            self.pack(f"CV{n}", n, *container[p["name"]])
        elif p["type"] == "l8szv":
            self.pack(f"C(Z*){n}", n, *container[p["name"]])
        elif p["type"] == "l8szbv":
            n = n // 2
            self.pack(f"C(Z*C){n}", n, *container[p["name"]])
        elif p["type"] == "l8szu16v":
            n = n // 2
            self.pack(f"C(Z*v){n}", n, *container[p["name"]])
        elif p["type"] == "l8u16u8v":
            n = n // 2
            self.pack(f"C(v*C){n}", n, *container[p["name"]])
        elif p["type"] == "l8u16u16v":
            n = n // 2
            self.pack(f"C(v*v){n}", n, *container[p["name"]])
        elif p["type"] == "l16u16v":
            self.pack(f"vv{n}", n, *container[p["name"]])
        elif p["type"] == "l32u8v":
            self.pack(f"VC{n}", n, *container[p["name"]])
        elif p["type"] == "l32u16v":
            self.pack(f"Vv{n}", n, *container[p["name"]])
        elif p["type"] == "l32u32v":
            self.pack(f"VV{n}", n, *container[p["name"]])
        elif p["type"] == "l32szv":
            self.pack(f"V(Z*){n}", n, *container[p["name"]])

    def _pack_vector(*args, **kwargs):
        (self, container, p) = args
        if rm := re.match(r"^q(?P<count>\d+)", p["type"]):
            func = "convert_u" + rm.group("count")
            for i in range(len(container[p["name"]])):
                converted = self.sub_hash()[func](container[p["name"]][i], -1, 1)
                if abs(converted - int(converted)) < 1e-4:
                    converted = int(converted)
                else:
                    raise ValueError(f"int({converted}) != {converted}")
                container[p["name"]][i] = converted

        self.pack(self.template_for_vector[p["type"]], *container[p["name"]])

    def _pack_sdir(*args, **kwargs):
        (self, container, p) = args
        (x, y, z) = container[p["name"]]
        (s) = math.sqrt(x * x + y * y + z * z)
        if s > 0.0000001:
            container[p["name"]][0] /= s
            container[p["name"]][1] /= s
            container[p["name"]][2] /= s
            self._pack_dir(container, p)
        else:
            s = 0.0
            container[p["name"]][0] = 0
            container[p["name"]][1] = 0
            container[p["name"]][2] = 0
            self.pack("v", 0)

        self.pack("f", s)

    def _pack_dir(*args, **kwargs):
        (self, container, p) = args
        (x, y, z) = container[p["name"]]
        # (i, u, v)
        t = 0
        if x < 0:
            t = 0x8000
            x = -x

        if y < 0:
            t |= 0x4000
            y = -y

        if z < 0:
            t |= 0x2000
            z = -z

        i = (x + y + z) / 126
        u = round(x / i)
        v = round(y / i)
        if u >= 64:
            v = 127 - v
            u = 127 - u

        t |= v
        t |= u << 7
        self.pack("v", t)

    def _pack_shape(self, container, p):
        # () = args
        self.pack("C", len(container[p["name"]]))
        for shape in container[p["name"]]:
            self.pack("C", shape.type)
            if shape.type == 0:
                self.pack("f4", *shape.sphere)
            elif shape.type == 1:
                self.pack("f12", *shape.box)

    def _pack_skeleton(self, container, p):
        # () = args
        self.pack(
            "C8vf3f3v",
            container.bones_mask,
            container.root_bone,
            container.bbox_min,
            container.bbox_max,
            len(container.bones),
        )
        for bone in container.bones:

            for i in range(len(bone.ph_position)):
                bone.ph_position[i] = self.convert_u8(
                    bone.ph_position[i],
                    container.bbox_min[i],
                    container.bbox_max[i],
                )

            self.pack("C3", bone.ph_position)
            for i in range(len(bone.ph_rotation)):
                bone.ph_rotation[i] = self.convert_u8(bone.ph_rotation[i], -1, 1)

            self.pack("C4", bone.ph_rotation)
            self.pack("C", bone.enabled)

    def _pack_supplies(*args, **kwargs):
        (self, container, p) = args
        self.pack("V", len(container[p["name"]]))
        for sect in container[p["name"]]:
            self.pack(
                "Z*Vff",
                sect.section_name,
                sect.item_count,
                sect.min_factor,
                sect.max_factor,
            )

    def _pack_artefact_spawns(*args, **kwargs):
        (self, container, p) = args
        self.pack("v", len(container[p["name"]]))
        if p["type"] == "afspawns":
            for sect in container[p["name"]]:
                self.pack("Z*f", sect.section_name, sect.weight)

        else:
            for sect in container[p["name"]]:
                self.pack("Z*V", sect.section_name, sect.weight)

    def _pack_ordered_artefacts(*args, **kwargs):
        (self, container, p) = args
        self.pack("V", len(container[p["name"]]))
        for sect in container[p["name"]]:
            self.pack(
                "Z*VV",
                sect.unknown_string,
                sect.unknown_number,
                len(sect.af_sects),
            )
            for obj in sect.af_sects:
                self.pack("Z*VV", obj.artefact_name, obj.number_1, obj.number_2)

    def _pack_ctime(*args, **kwargs):
        (self, time) = args
        date = []
        if time != 0:
            date = time.get_all()
        else:
            date = [2000]

        date[0] -= 2000
        if date[0] == 0 or date[0] == 255:
            self.pack("C", date[0])
        else:
            self.pack("C6v", date)

    def _pack_complex_time(*args, **kwargs):
        (self, time) = args
        flag = 0
        if time != 0:
            flag = 1
        self.pack("C", flag)
        if flag == 1:
            self._pack_ctime(time)

    def _pack_jobs(*args, **kwargs):
        (self, container, p) = args
        self.pack("C", len(container[p["name"]]))
        for job in container[p["name"]]:
            self.pack(
                "VVV",
                job.job_begin,
                job.job_fill_idle,
                job.job_idle_after_death_end,
            )

    def _pack_npc_info(self, *args, **kwargs):

        if args[0].version >= 122:
            self._pack_npc_info_cop(*args)
        elif args[0].version >= 117:
            self._pack_npc_info_soc(*args)
        else:
            self._pack_npc_info_old(*args)

    def _pack_npc_info_old(*args, **kwargs):
        (self, container, p) = args
        self.pack("C", len(container[p["name"]]))
        for info in container[p["name"]]:
            self.pack(
                "vCCCC",
                info.o_id,
                info.group,
                info.squad,
                info.move_offline,
                info.switch_offline,
            )
            self._pack_ctime(info.stay_end)
            if container.script_version >= 1 and container.gulagN != 0:
                self.pack("C", info.jobN)

    def _pack_npc_info_soc(*args, **kwargs):
        (self, container, p) = args
        self.pack("C", len(container[p["name"]]))
        for info in container[p["name"]]:
            self.pack("vCCC", info.o_id, info.o_group, info.o_squad, info.exclusive)
            self._pack_ctime(info.stay_end)
            self.pack("C", info.Object_begin_job)
            if container.script_version > 4:
                self.pack("C", info.Object_didnt_begin_job)
            self.pack("C", info.jobN)

    def _pack_npc_info_cop(*args, **kwargs):
        (self, container, p) = args
        self.pack("C", len(container[p["name"]]))
        for info in container[p["name"]]:
            self.pack(
                "vCCCZ*",
                info.id,
                info.job_prior,
                info.job_id,
                info.begin_job,
                info.need_job,
            )

    def _pack_covers(*args, **kwargs):
        (self, container, p) = args
        self.pack("C", len(container[p["name"]]))
        for cover in container[p["name"]]:
            self.pack(
                "vVf3f3C",
                cover.npc_id,
                cover.cover_vertex_id,
                cover.cover_position,
                cover.look_pos,
                cover.is_smart_cover,
            )

    def _pack_squads(*args, **kwargs):
        (self, container, p) = args
        self.pack("C", len(container[p["name"]]))
        for squad in container[p["name"]]:
            self.pack(
                "Z*Z*CCC",
                squad.squad_name,
                squad.squad_stage,
                squad.squad_prepare_shouted,
                squad.squad_attack_shouted,
                squad.squad_attack_squad,
            )
            self._pack_complex_time(squad.squad_inited_defend_time)
            self._pack_complex_time(squad.squad_start_attack_wait)
            self._pack_complex_time(squad.squad_last_defence_kill_time)
            self.pack("f", squad.squad_power)

    def _pack_sim_squads(*args, **kwargs):
        (self, container, p) = args
        self.pack("v", len(container[p["name"]]))
        for squad in container[p["name"]]:
            self.pack("Z*Z*C", squad.squad_id, squad.settings_id, squad.is_scripted)
            self._pack_sim_squad_generic(container, squad)
            if squad.is_scripted == 1:
                self.set_save_marker(container, "save", 0, "sim_squad_scripted")
                self.pack(
                    "CCCC",
                    squad.continue_target,
                    squad.need_free_update,
                    squad.relationship,
                    squad.sympathy,
                )
                self.set_save_marker(container, "save", 1, "sim_squad_scripted")

    def _pack_sim_squad_generic(*args, **kwargs):
        (self, container, squad) = args
        self.set_save_marker(container, "save", 0, "sim_squad_generic")
        self.pack(
            "vvvv",
            squad.smart_id,
            squad.assigned_target_smart_id,
            squad.sim_combat_id,
            squad.delayed_attack_task,
        )
        n = len(squad.random_tasks) + 1
        n = n / 2
        self.pack("C(vv)n", n, squad.random_tasks)
        self.pack("Cfv", squad.npc_count, squad.squad_power, squad.commander_id)
        n = len(squad.squad_npc)
        self.pack("C(v)n", n, squad.squad_npc)
        self.pack("C", squad.spoted_shouted)
        self._pack_ctime(squad.last_action_timer)
        self.pack("v", squad.squad_attack_power)
        if squad._class is not None:
            self.pack("C", 1)
            self.pack("C", squad._class)
            if squad._class == 1:
                # sim_attack_point
                self.pack("v", squad.dest_smrt_id)
                self.set_save_marker(container, "save", 0, "sim_attack_point")
                self.pack("Cv", squad.major, squad.target_power_value)
                self.set_save_marker(container, "save", 1, "sim_attack_point")
            else:
                self.set_save_marker(container, "save", 0, "sim_stay_point")
                self.pack("Cv", squad.stay_defended, squad.continue_point_id)
                self._pack_complex_time(squad.begin_time)
                self.set_save_marker(container, "save", 1, "sim_stay_point")

        else:
            self.pack("C", 0)

        self.pack("C", squad.items_spawned)
        self._pack_ctime(squad.bring_item_inited_time)
        self._pack_ctime(squad.recover_item_inited_time)
        self.set_save_marker(container, "save", 1, "sim_squad_generic")

    def _pack_times(*args, **kwargs):
        (self, container, p) = args
        self.pack("C", len(container[p["name"]]))
        for _ in container[p["name"]]:
            self._pack_complex_time(_)

    def _pack_inited_find_upgrade_tasks(*args, **kwargs):
        (self, container, p) = args
        self.pack("v", len(container[p["name"]]))
        for _ in container[p["name"]]:
            self.unpack("vv", _.k, len(_.subtasks))
            for subtask in _.subtasks:
                self.unpack("Z*v", subtask.kk, subtask.entity_id)

    def _pack_rewards(*args, **kwargs):
        (self, container, p) = args
        self.pack("C", len(container[p["name"]]))
        for _ in container[p["name"]]:
            self.pack("Z*C", _.community, len(_.rewards))
            for reward in _.rewards:
                self.pack("C", reward.is_money)
                if reward.is_money == 1:
                    self.pack("v", reward.amount)
                else:
                    self.pack("Z*", reward.item_name)

    def _pack_CGeneralTask(*args, **kwargs):
        (self, task, container) = args
        self.set_save_marker(container, "save", 0, "CGeneralTask")
        self.pack(
            "vCCCZ*CC",
            task.entity_id,
            task.prior,
            task.status,
            task.actor_helped,
            task.community,
            task.actor_come,
            task.actor_ignore,
        )
        self._pack_ctime(task.inited_time)
        self.set_save_marker(container, "save", 1, "CGeneralTask")

    def _pack_CStorylineTask(*args, **kwargs):
        (self, task, container) = args
        self.set_save_marker(container, "save", 0, "CStorylineTask")
        self._pack_CGeneralTask(task, container)
        self.pack("V", task.target)
        self.set_save_marker(container, "save", 1, "CStorylineTask")

    def _pack_CEliminateSmartTask(*args, **kwargs):
        (self, task, container) = args
        self.set_save_marker(container, "save", 0, "CEliminateSmartTask")
        self._pack_CGeneralTask(task, container)
        self.pack("vZ*Z*", task.target, task.src_obj, task.faction)
        self.set_save_marker(container, "save", 1, "CEliminateSmartTask")

    def _pack_CCaptureSmartTask(*args, **kwargs):
        (self, task, container) = args
        self.set_save_marker(container, "save", 0, "CCaptureSmartTask")
        self._pack_CGeneralTask(task, container)
        self.pack(
            "vZ*Z*Z*Z*Z*",
            task.target,
            task.state,
            task.counter_attack_community,
            task.counter_squad,
            task.src_obj,
            task.faction,
        )
        self.set_save_marker(container, "save", 1, "CCaptureSmartTask")

    def _pack_CDefendSmartTask(*args, **kwargs):
        (self, task, container) = args
        self.set_save_marker(container, "save", 0, "CDefendSmartTask")
        self._pack_CGeneralTask(task, container)
        self.pack("v", task.target)
        self.pack_ctime(task.last_called_time)
        self.set_save_marker(container, "save", 1, "CDefendSmartTask")

    def _pack_CBringItemTask(*args, **kwargs):
        (self, task, container) = args
        self.set_save_marker(container, "save", 0, "CBringItemTask")
        self._pack_CGeneralTask(task, container)
        self.pack(
            "Z*CvZ*C",
            task.state,
            task.ri_counter,
            task.target,
            task.squad_id,
            len(task.requested_items),
        )
        for _ in task.requested_items:
            self.pack("Z*", _.id)
            n = len(_.items)
            self.pack("v(C)n", _.items)

        self.set_save_marker(container, "save", 1, "CBringItemTask")

    def _pack_CRecoverItemTask(*args, **kwargs):
        (self, task, container) = args
        self.set_save_marker(container, "save", 0, "CRecoverItemTask")
        self._pack_CGeneralTask(task, container)
        self.pack(
            "CZ*vCZ*",
            task.state,
            task.squad_id,
            task.target_obj_id,
            task.presence_requested_item,
            task.requested_item,
        )
        self.set_save_marker(container, "save", 1, "CRecoverItemTask")

    def _pack_CFindUpgradeTask(*args, **kwargs):
        (self, task, container) = args
        self.set_save_marker(container, "save", 0, "CFindUpgradeTask")
        self._pack_CGeneralTask(task, container)
        self.pack(
            "Z*CZ*",
            task.state,
            task.presence_requested_item,
            task.requested_item,
        )
        self.set_save_marker(container, "save", 1, "CFindUpgradeTask")

    def _pack_CHideFromSurgeTask(*args, **kwargs):
        (self, task, container) = args
        self.set_save_marker(container, "save", 0, "CHideFromSurgeTask")
        self._pack_CGeneralTask(task, container)
        self.pack("vvv", task.target, task.wait_time, task.effector_started_time)
        self.set_save_marker(container, "save", 1, "CHideFromSurgeTask")

    def _pack_CEliminateSquadTask(*args, **kwargs):
        (self, task, container) = args
        self.set_save_marker(container, "save", 0, "CEliminateSquadTask")
        self._pack_CGeneralTask(task, container)
        self.pack("vZ*", task.target, task.src_obj)
        self.set_save_marker(container, "save", 1, "CEliminateSquadTask")

    def _pack_inited_tasks(*args, **kwargs):
        (self, container, p) = args
        (count) = self.pack("v", len(container[p["name"]]))
        for _ in container[p["name"]]:
            self.pack("Z*Z*v", _.base_id, _.id, _.type)

            if _.type == 0 or _.type == 5:
                self._pack_CStorylineTask(_, container)
            elif _.type == 1:
                self._pack_CEliminateSmartTask(_, container)
            elif _.type == 2:
                self._pack_CCaptureSmartTask(_, container)
            elif _.type == 3 or _.type == 4:
                self._pack_CDefendSmartTask(_, container)
            elif _.type == 6:
                self._pack_CBringItemTask(_, container)
            elif _.type == 7:
                self._pack_CRecoverItemTask(_, container)
            elif _.type == 8:
                self._pack_CFindUpgradeTask(_, container)
            elif _.type == 9:
                self._pack_CHideFromSurgeTask(_, container)
            elif _.type == 10:
                self._pack_CEliminateSquadTask(_, container)
        # else:
        # 	raise NotImplementedError()

    def _pack_minigames(*args, **kwargs):
        (self, container, p) = args
        self.pack("v", len(container[p["name"]]))
        for _ in container[p["name"]]:
            self.pack("Z*Z*Z*", _.key, _.profile, _.state)
            if _.profile == "CMGCrowKiller":
                self.set_save_marker(container, "save", 0, "CMGCrowKiller")
                self.pack("CvC", _.param_highscore, _.param_timer, _.param_win)
                n = len(_.param_crows_to_kill)
                self.pack("C(C)n", n, _.param_crows_to_kill)
                self.pack(
                    "vvCZ*CvvCC",
                    _.param_money_multiplier,
                    _.param_champion_multiplier,
                    _.param_selected,
                    _.param_game_type,
                    _.high_score,
                    _.timer,
                    _.time_out,
                    _.killed_counter,
                    _.win,
                )
                self.set_save_marker(container, "save", 1, "CMGCrowKiller")
            elif _.profile == "CMGShooting":
                self.set_save_marker(container, "save", 0, "CMGShooting")
                self.pack(
                    "Z*Z*Z*Z*Z*Z*Z*",
                    _.param_game_type,
                    _.param_wpn_type,
                    _.param_stand_way,
                    _.param_look_way,
                    _.param_stand_way_back,
                    _.param_look_way_back,
                    _.param_obj_name,
                )
                self.pack("C", _.param_is_u16)
                if _.param_is_u16 == 0:
                    self.pack("C", _.param_win)
                else:
                    self.pack("v", _.param_win)

                self.pack("CCC", _.param_distance, _.param_ammo, len(_.targets))
                for target in _.targets:
                    n = len(target)
                    self.pack("C(Z*)n", n, target)

                self.pack("C", _.param_target_counter)
                n = len(_.inventory_items)
                self.pack("C(v)n", n, _.inventory_items)
                self.pack("VZ*", _.prev_time, _.type)
                if _.type == "training" or _.type == "points":
                    self.set_save_marker(container, "save", 0, _.type)
                    self.pack(
                        "vvZ*vC",
                        _.win,
                        _.ammo,
                        _.cur_target,
                        _.points,
                        _.ammo_counter,
                    )
                    self.set_save_marker(container, "save", 1, _.type)
                elif _.type == "count":
                    self.set_save_marker(container, "save", 0, _.type)
                    self.pack("Z*CCC", _.wpn_type, _.win, _.ammo, len(_.targets))
                    for target in _.targets:
                        n = len(target)
                        self.pack("C(Z*)n", n, target)

                    self.pack(
                        "CZ*CCC",
                        _.distance,
                        _.cur_target,
                        _.points,
                        _.scored,
                        _.ammo_counter,
                    )
                    self.set_save_marker(container, "save", 1, _.type)
                elif _.type == "three_hit_training":
                    self.set_save_marker(container, "save", 0, _.type)
                    self.pack("Z*vCC", _.wpn_type, _.win, _.ammo, len(_.targets))
                    for target in _.targets:
                        n = len(target)
                        self.pack("C(Z*)n", n, target)

                    self.pack(
                        "CZ*vCCCC",
                        _.distance,
                        _.cur_target,
                        _.points,
                        _.scored,
                        _.ammo_counter,
                        _.target_counter,
                        _.target_hit,
                    )
                    self.set_save_marker(container, "save", 1, _.type)
                elif _.type == "all_targets":
                    self.set_save_marker(container, "save", 0, _.type)
                    self.pack("Z*vCC", _.wpn_type, _.win, _.ammo, len(_.targets))
                    for target in _.targets:
                        n = len(target)
                        self.pack("C(Z*)n", n, target)

                    for hitted_target in _.hitted_targets:
                        n = len(hitted_target)
                        self.pack("C(Z*)n", n, hitted_target)

                    self.pack(
                        "CvCVCZ*",
                        _.ammo_counter,
                        _.time,
                        _.target_counter,
                        _.prev_time,
                        _.more_targets,
                        _.last_target,
                    )
                    self.set_save_marker(container, "save", 1, _.type)
                elif _.type == "count_on_time":
                    self.set_save_marker(container, "save", 0, _.type)
                    self.pack("Z*vCC", _.wpn_type, _.win, _.ammo, len(_.targets))
                    for target in _.targets:
                        n = len(target)
                        self.pack("C(Z*)n", n, target)

                    self.pack(
                        "CZ*CCCCV",
                        _.distance,
                        _.cur_target,
                        _.points,
                        _.scored,
                        _.ammo_counter,
                        _.time,
                        _.prev_time,
                    )
                    self.set_save_marker(container, "save", 1, _.type)
                elif _.type == "ten_targets":
                    self.set_save_marker(container, "save", 0, _.type)
                    self.pack("Z*vCC", _.wpn_type, _.win, _.ammo, len(_.targets))
                    for target in _.targets:
                        n = len(target)
                        self.pack("C(Z*)n", n, target)

                    self.pack(
                        "CZ*CCCvV",
                        _.distance,
                        _.cur_target,
                        _.points,
                        _.scored,
                        _.ammo_counter,
                        _.time,
                        _.prev_time,
                    )
                    self.set_save_marker(container, "save", 1, _.type)
                elif _.type == "two_seconds_standing":
                    self.set_save_marker(container, "save", 0, _.type)
                    self.pack("Z*vCC", _.wpn_type, _.win, _.ammo, len(_.targets))
                    for target in _.targets:
                        n = len(target)
                        self.pack("C(Z*)n", n, target)

                    self.pack(
                        "CZ*CCCV",
                        _.distance,
                        _.cur_target,
                        _.points,
                        _.ammo_counter,
                        _.time,
                        _.prev_time,
                    )
                    self.set_save_marker(container, "save", 1, _.type)

                self.set_save_marker(container, "save", 1, "CMGShooting")

    # various
    def length(self):
        return length(self.data)

    def resid(self):
        return self.length() - self.pos

    def r_tell(self):
        return self.init_length - self.resid()

    def w_tell(self):
        return length(self.data)

    def raw(*args, **kwargs):
        if len(args) == 1:
            out = substr(args[0].data, args[0].pos, args[1])
            args[0].pos += args[1]
            return out
        if len(args) == 2:
            substr(args[0].data, args[0].pos, args[1], args[2])

    # def data (*args, **kwargs):
    # 	if len(args) == 0:
    # 		return args[0].data #if #_ == 0
    # 	args[0].data = args[1]

    # def pos (*args, **kwargs):
    # 	return args[0].pos if #_ == 0
    # 	args[0].pos = args[1]

    def isinf(self, num):
        return math.isinf(num)

    def isnan(self, num):
        return math.isnan(num)

    # if (! defined(args[0] <=> 9**9**9)):
    # 	return 1
    #
    # return 0

    def set_save_marker(packet, object, mode, check, name):
        # packet = shift
        # object = shift
        # mode = shift
        # check = shift
        # name = shift
        if check:
            if object.markers[name] is None:
                raise ValueError
            # die unless defined()
            if mode == "save":
                diff = packet.w_tell() - object.markers[name]
                assert diff > 0
                packet.pack("v", diff)
            else:
                diff = packet.r_tell() - object.markers[name]
                assert diff > 0
                (diff1,) = packet.unpack("v", 2)
                assert diff == diff1

        else:
            if object.markers is None:
                object.markers = universal_dict_object()
            if mode == "save":
                object.markers[name] = packet.w_tell()
            else:
                object.markers[name] = packet.r_tell()

    def convert_q8(self, u, min, max):
        # (u, min, max) = args
        q = u / 255.0 * (max - min) + min
        return q

    def convert_u8(self, q, min, max):
        # (q, min, max) = args
        u = (q - min) * 255.0 / (max - min)
        return u

    def convert_q16(self, u, a, b):
        # (u) = args
        q = (u / 43.69) - 500.0
        return q

    def convert_u16(self, q, a, b):
        # (q) = args
        u = round((q + 500.0) * 43.69)
        return u

    def convert_q16_old(self, u, a, b):
        # (u) = args
        q = (u / 32.77) - 1000.0
        return q

    def convert_u16_old(self, q, a, b):
        # (q) = args
        u = round((q + 1000.0) * 32.77)
        return u

    def error_handler(self, container, template):

        print("handling error with container.section_name, template template\n")
        print(f" {container.section_name=},{template=}")

        if (
            (template == "C")
            and (ref(container) == "se_zone_anom")
            and container.version == 118
            and container.script_version == 6
        ):
            print("unpacking spawn of Narodnaya Solyanka, huh? OK...\n")
            # bless container, 'cse_alife_anomalous_zone'
            if container.ini is not None:
                container.ini.sections_hash["sections"][
                    "'container.section_name'"
                ] = "cse_alife_anomalous_zone"
            container.flags |= self.FL_HANDLED

        # future fix
        elif (
            (template == "C")
            and (ref(container) == "se_zone_visual")
            and container.version == 118
            and container.script_version == 6
        ):
            print("unpacking spawn of some mod, huh? OK...\n")
            # bless container, 'cse_alife_zone_visual'
            if container.ini is not None:
                container.ini.sections_hash["sections"][
                    "'container.section_name'"
                ] = "cse_alife_zone_visual"  # if defined container.ini
            container.flags |= self.FL_HANDLED

        elif (
            (template == "f")
            and (ref(container) == "cse_alife_anomalous_zone")
            and container.version == 118
            and container.script_version == 6
        ):
            print("unpacking spawn of some mod, huh? OK...\n")
            # bless container, 'cse_alife_custom_zone'
            if container.ini is not None:
                container.ini.sections_hash["sections"][
                    "'container.section_name'"
                ] = "cse_alife_custom_zone"  # if defined container.ini
            container.flags |= self.FL_HANDLED
        # last

        # builds 25xx fix
        elif (
            re.match("cse_alife_item_weapon_", ref(container))
            and container.version == 118
            and container.script_version == 5
        ):
            if ref(container) == "cse_alife_item_weapon_shotgun":
                # bless container, 'cse_alife_item_weapon_magazined'
                ...
            else:
                # bless container, 'cse_alife_item_weapon'
                ...

            self.fix_25xx(container)
        # last

        elif (
            re.match("stalker|monster|actor", ref(container))
            and container.version == 118
            and container.script_version == 5
        ):
            self.fix_25xx(container)
        # last
        else:
            fail("unhandled exception\n")

    # }

    def round(*args, **kwargs):
        temp = "%.2f" % args[0]
        int = int(temp)
        if (temp - int) > 0.5000:
            return math.ceil(temp)
        return math.floor(temp)

    def fix_25xx(self, *args, **kwargs):
        args[1].flags |= self.FL_IS_25XX
        args[0].pos = 2
        args[1].update_read(args[0])
        args[1].flags |= self.FL_HANDLED
        if re.match("stalker|monster", ref(args[1])):
            args[0].pos = 42
        for section in args[1].ini.sections_hash["sections"].keys():
            if re.match(
                "cse_alife_item_weapon_magazined",
                args[1].ini.sections_hash["sections"][section],
            ):
                args[1].ini.sections_hash["sections"][section] = "cse_alife_item_weapon"
            elif (
                args[1].ini.sections_hash["sections"][section]
                == "cse_alife_item_weapon_shotgun"
            ):
                args[1].ini.sections_hash["sections"][
                    section
                ] = "cse_alife_item_weapon_magazined"

    def is_handled(self, *args, **kwargs):
        return (
            hasattr(args[0], "is_handled")
            and (args[0].is_handled is not None)
            and args[0].is_handled()
        )
