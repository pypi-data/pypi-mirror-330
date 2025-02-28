import os
import re
import subprocess
from pathlib import Path
from unittest import TestCase

from stkutils import perl_utils
from stkutils.conf import BaseConfig, CommonOptions
from stkutils.core import main
from stkutils.ini_file import ini_file
from tests.ltx_parser import LtxBlock, LtxParser

DATA_DIR = "data"


class BaseCompareTest(TestCase):
    perl_dir = "perl"
    pthon_dir = "python"
    data_dir = "data"
    results_dir = "results"
    current_dir: str
    # maxDiff = None

    def get_python_results_path(self) -> Path:
        root = Path(__file__).parent.parent
        return (
            root / self.data_dir / self.results_dir / self.current_dir / self.pthon_dir
        )

    def get_perl_results_path(self) -> Path:
        root = Path(__file__).parent.parent
        return (
            root / self.data_dir / self.results_dir / self.current_dir / self.perl_dir
        )

    def _compare_files(self):
        perl_path = self.get_perl_results_path() / "all_cs"
        python_path = self.get_python_results_path() / "all_cs"
        perl_files = {path.name for path in perl_path.iterdir()}
        python_files = {path.name for path in python_path.iterdir()}

        self.assertSetEqual(perl_files, python_files)

        for filename in sorted(perl_files):
            with self.subTest(filename):
                python_file = python_path / filename
                perl_file = perl_path / filename
                self.assertFileEquals(python_file, perl_file)

    def assertFileEquals(self, python_file: Path, perl_file: Path) -> None:
        self.assertTrue(python_file.is_file())
        self.assertTrue(perl_file.is_file())
        if python_file.suffix == ".ltx":
            self.assertLtxEqual(python_file, perl_file)
        elif python_file.suffix in {".sections", ".log"}:
            self.assertTextFilesEqual(python_file, perl_file)
        elif python_file.suffix in {".bin", ".spawn", ".game"}:
            self.assertBinEqual(python_file, perl_file)
        else:
            raise ValueError(f"Unknown extension {python_file.suffix}")

    def assertLtxEqual(self, python_file: Path, perl_file: Path) -> None:
        python_parser = LtxParser(python_file)
        perl_parser = LtxParser(perl_file)
        python_blocks = python_parser.get_parsed_blocks()
        perl_blocks = perl_parser.get_parsed_blocks()

        python_blocks_keys = set(python_blocks.keys())
        perl_blocks_keys = set(perl_blocks.keys())
        self.assertSetEqual(python_blocks_keys, perl_blocks_keys)

        for block_name in sorted(python_blocks_keys):
            python_block = python_blocks[block_name]
            perl_block = perl_blocks[block_name]
            with self.subTest(file=python_file.name, block=block_name):
                self._assertLtxBlockEquals(python_block, perl_block)

    def _assertLtxBlockEquals(
        self,
        python_block: LtxBlock,
        perl_block: LtxBlock,
    ) -> None:
        coordinates_delta = 5e-5
        big_number = 1e10
        float_re = r"([+-]?\d(\.\d+)?e(-|\+)?\d+)|([+-]?\d+(\.\d+)?)"
        float_prop_regex = re.compile(rf"\s*(?P<value>{float_re})")
        point_with_weight_re = re.compile(rf"p(?P<point>\d+)\((?P<weight>{float_re})\)")
        if isinstance(python_block, list) and isinstance(perl_block, list):
            self.assertListEqual(python_block, perl_block)
        elif isinstance(python_block, dict) and isinstance(perl_block, dict):
            python_block_keys = set(python_block.keys())
            perl_block_keys = set(perl_block.keys())
            self.assertSetEqual(python_block_keys, perl_block_keys)
            for key in python_block_keys:
                python_value = python_block[key]
                perl_value = perl_block[key]
                if python_value is None or perl_value is None:
                    self.assertEqual(python_value, perl_value)

                elif all(
                    float_prop_regex.match(part) for part in perl_value.split(",")
                ) and all(
                    float_prop_regex.match(part) for part in python_value.split(",")
                ):
                    for perl_match, py_math in zip(
                        (
                            float_prop_regex.match(perl_part)
                            for perl_part in perl_value.split(",")
                        ),
                        (
                            float_prop_regex.match(python_part)
                            for python_part in python_value.split(",")
                        ),
                        strict=False,
                    ):
                        python_parsed_value = float(py_math.group("value"))
                        perl_parsed_value = float(perl_match.group("value"))
                        if (
                            abs(python_parsed_value) > big_number
                            or abs(perl_parsed_value) > big_number
                        ):
                            abs_diff = abs(
                                python_parsed_value - perl_parsed_value,
                            ) / min(abs(python_parsed_value), abs(perl_parsed_value))
                            self.assertAlmostEqual(
                                abs_diff,
                                0,
                                delta=coordinates_delta,
                                msg=key,
                            )
                        else:
                            self.assertAlmostEqual(
                                python_parsed_value,
                                perl_parsed_value,
                                delta=coordinates_delta,
                                msg=key,
                            )

                elif all(
                    point_with_weight_re.match(part) for part in perl_value.split(",")
                ) and all(
                    point_with_weight_re.match(part) for part in python_value.split(",")
                ):
                    for perl_match, py_math in zip(
                        (
                            point_with_weight_re.match(perl_part)
                            for perl_part in perl_value.split(",")
                        ),
                        (
                            point_with_weight_re.match(python_part)
                            for python_part in python_value.split(",")
                        ),
                        strict=False,
                    ):
                        self.assertEqual(
                            py_math.group("point"),
                            perl_match.group("point"),
                            msg=key,
                        )
                        self.assertAlmostEqual(
                            float(py_math.group("weight")),
                            float(perl_match.group("weight")),
                            delta=coordinates_delta,
                            msg=key,
                        )

                else:
                    self.assertEqual(python_value.strip(), perl_value.strip(), msg=key)
        else:
            raise TypeError(f"Couldnt compare {python_block=}, {perl_block=}")

    def assertTextFilesEqual(self, python_file: Path, perl_file: Path) -> None:
        with open(python_file, encoding="cp1251") as python_file_content:
            with open(perl_file, encoding="cp1251") as perl_file_content:
                for python_file_line, perl_file_line in zip(
                    python_file_content.readlines(),
                    perl_file_content.readlines(),
                    strict=True,
                ):
                    if python_file_line == perl_file_line:
                        continue
                    self.assertEqual(python_file_line, perl_file)

    def assertBinEqual(self, python_file_path: Path, perl_file_path: Path) -> None:
        with open(python_file_path, "rb") as python_file:
            py_file_content = python_file.read()
        with open(perl_file_path, "rb") as perl_file:
            perl_file_content = perl_file.read()

        self.assertEqual(py_file_content, perl_file_content)

        with self.subTest("length", file=python_file.name):
            self.assertEqual(len(py_file_content), len(perl_file_content))

        different_chars_count = sum(
            0 if py_ch == perl_ch else 1
            for (py_ch, perl_ch) in zip(
                py_file_content,
                perl_file_content,
                strict=False,
            )
        )

        with self.subTest("diff_chars_count", file=python_file.name):
            total_len = len(perl_file_content)
            if total_len > 0:
                change_perc = round(different_chars_count / total_len, 4)
                self.assertEqual(
                    different_chars_count,
                    0,
                    msg=f"Total length {total_len:_}, changes={different_chars_count:_}, perc={change_perc}",
                )

        CHUNK_SIZE = 500_000
        max_len = max(len(py_file_content), len(perl_file_content))
        chunks_count = max_len // CHUNK_SIZE
        if max_len % CHUNK_SIZE != 0:
            chunks_count += 1
        for chunk_num in range(chunks_count):

            py_chunk = py_file_content[
                chunk_num * CHUNK_SIZE : CHUNK_SIZE * (chunk_num + 1)
            ]
            perl_chunk = perl_file_content[
                chunk_num * CHUNK_SIZE : CHUNK_SIZE * (chunk_num + 1)
            ]

            with self.subTest("total", chunk_index=chunk_num, file=python_file.name):
                self.assertListEqual(list(py_chunk), list(perl_chunk))

            with self.subTest("diff", chunk_index=chunk_num, file=python_file.name):
                different_chars_count = sum(
                    0 if py_ch == perl_ch else 1
                    for (py_ch, perl_ch) in zip(py_chunk, perl_chunk, strict=False)
                )
                total_len = CHUNK_SIZE
                change_perc = round(different_chars_count / total_len, 4)
                self.assertLess(
                    different_chars_count,
                    2 * CHUNK_SIZE / 100,
                    msg=f"Total length {total_len:_}, changes={different_chars_count:_}, perc={change_perc}",
                )

        self.assertEqual(py_file_content, perl_file_content)

    def _get_ini_if_file_exists(self, filename: str) -> ini_file | None:
        return ini_file(filename, "r") if Path(filename).exists() else None

    def _decompile_files(self):
        config = BaseConfig()
        config.mode = "decompile"
        config.common = CommonOptions()
        config.common.src = str(
            Path("data") / "sources" / self.current_dir / "spawns" / "all.spawn",
        )
        config.common.out = str(
            Path("data") / "results" / self.current_dir / "python" / "all_cs",
        )
        config.common.sort = "complex"
        config.common.graph_dir = str(Path("data") / "sources" / self.current_dir)
        config.common.af = None
        config.common.way = False
        config.common.scan_dir = None
        config.common.level_spawn = None
        config.common.nofatal = False
        config.common.af = None

        config.compile = perl_utils.universal_dict_object()
        config.compile.flags = None
        config.compile.idx_file = None
        # 	# split options
        config.split = perl_utils.universal_dict_object()
        config.split.use_graph = False
        config.parse = perl_utils.universal_dict_object()
        config.parse.old_gvid = None
        config.parse.new_gvid = None

        config.common.sections_ini = (
            config.with_scan() if self._get_ini_if_file_exists("sections.ini") else None
        )
        config.common.user_ini = self._get_ini_if_file_exists("user_sections.ini")
        config.common.prefixes_ini = self._get_ini_if_file_exists("way_prefixes.ini")

        m = main(config)
        m.main()

        decompile_perl_result = subprocess.run(
            [
                "perl",
                "universal_acdc.pl",
                "-d",
                str(
                    Path("data")
                    / "sources"
                    / self.current_dir
                    / "spawns"
                    / "all.spawn",
                ),
                "-out",
                str(Path("data") / "results" / self.current_dir / "perl" / "all_cs"),
                "-sort",
                "complex",
                "-g",
                str(Path("data") / "sources" / self.current_dir),
            ],
            check=False,
        )
        self.assertEqual(decompile_perl_result.returncode, 0)


class ShadowOfChernobylCompareTest(BaseCompareTest):
    current_dir = "shadow_of_chernobyl_Steam"

    def test(self) -> None:
        self._decompile_files()
        self._compare_files()


class ClearSkyCompareTest(BaseCompareTest):
    current_dir = "clear_sky"

    def test(self) -> None:
        self._decompile_files()
        self._compare_files()


class CallOfPripyatCompareTest(BaseCompareTest):
    current_dir = "call_of_pripyat"

    def test(self) -> None:
        self._decompile_files()
        self._compare_files()


class TestSplitShoC(BaseCompareTest):
    current_dir = "shadow_of_chernobyl_Steam"

    def _split_files(self):
        config = BaseConfig()
        config.mode = "split"
        config.common = CommonOptions()
        config.common.src = str(
            Path("data") / "sources" / self.current_dir / "spawns" / "all.spawn",
        )
        config.common.out = str(
            Path("data") / "results" / self.current_dir / "python" / "spawns",
        )
        config.common.sort = "complex"
        config.common.graph_dir = str(Path("data") / "sources" / self.current_dir)
        config.common.af = None
        config.common.way = True
        config.common.scan_dir = None
        config.common.level_spawn = None
        config.common.nofatal = False
        config.common.af = None

        config.compile = perl_utils.universal_dict_object()
        config.compile.flags = None
        config.compile.idx_file = None
        # 	# split options
        config.split = perl_utils.universal_dict_object()
        config.split.use_graph = True
        config.parse = perl_utils.universal_dict_object()
        config.parse.old_gvid = None
        config.parse.new_gvid = None

        config.common.sections_ini = (
            config.with_scan() if self._get_ini_if_file_exists("sections.ini") else None
        )
        config.common.user_ini = self._get_ini_if_file_exists("user_sections.ini")
        config.common.prefixes_ini = self._get_ini_if_file_exists("way_prefixes.ini")

        m = main(config)
        m.main()

        decompile_perl_result = subprocess.run(
            [
                "perl",
                "universal_acdc.pl",
                "-split",
                str(
                    Path("data")
                    / "sources"
                    / self.current_dir
                    / "spawns"
                    / "all.spawn",
                ),
                "-way",
                "-out",
                str(Path("data") / "results" / self.current_dir / "perl" / "spawns"),
                "-g",
                str(Path("data") / "sources" / self.current_dir),
                "-use_graph",
            ],
            check=False,
        )
        self.assertEqual(decompile_perl_result.returncode, 0)

    def test(self) -> None:
        self._split_files()
        self._compare_files()

    def _compare_files(self):
        perl_path = self.get_perl_results_path() / "spawns"
        python_path = self.get_python_results_path() / "spawns"
        perl_subdirs = {path.name for path in perl_path.iterdir()}
        python_subdirs = {path.name for path in python_path.iterdir()}

        self.assertSetEqual(perl_subdirs, python_subdirs)

        for filename in sorted(perl_subdirs):
            with self.subTest(filename):
                if (python_path / filename).is_dir():
                    python_file = python_path / filename / "level.spawn"
                    perl_file = perl_path / filename / "level.spawn"
                    self.assertFileEquals(python_file, perl_file)
                else:
                    self.assertFileEquals(python_path / filename, perl_path / filename)


class BaseAFCompareTest(BaseCompareTest):
    def _decompile_files(self):
        config = BaseConfig()
        config.mode = "decompile"
        config.common = CommonOptions()
        config.common.src = str(
            Path("data") / "sources" / self.current_dir / "spawns" / "all.spawn",
        )
        config.common.out = str(
            Path("data") / "results" / self.current_dir / "python" / "all_cs",
        )
        config.common.sort = "complex"
        config.common.graph_dir = str(Path("data") / "sources" / self.current_dir)
        config.common.af = None
        config.common.way = False
        config.common.scan_dir = None
        config.common.level_spawn = None
        config.common.nofatal = False
        config.common.af = True

        config.compile = perl_utils.universal_dict_object()
        config.compile.flags = None
        config.compile.idx_file = None
        # 	# split options
        config.split = perl_utils.universal_dict_object()
        config.split.use_graph = False
        config.parse = perl_utils.universal_dict_object()
        config.parse.old_gvid = None
        config.parse.new_gvid = None

        config.common.sections_ini = (
            config.with_scan() if self._get_ini_if_file_exists("sections.ini") else None
        )
        config.common.user_ini = self._get_ini_if_file_exists("user_sections.ini")
        config.common.prefixes_ini = self._get_ini_if_file_exists("way_prefixes.ini")

        m = main(config)
        m.main()

        decompile_perl_result = subprocess.run(
            [
                "perl",
                "universal_acdc.pl",
                "-d",
                str(
                    Path("data")
                    / "sources"
                    / self.current_dir
                    / "spawns"
                    / "all.spawn",
                ),
                "-out",
                str(Path("data") / "results" / self.current_dir / "perl" / "all_cs"),
                "-sort",
                "complex",
                "-g",
                str(Path("data") / "sources" / self.current_dir),
                "--af",
            ],
            check=False,
        )
        self.assertEqual(decompile_perl_result.returncode, 0)


class ShadowOfChernobylAFCompareTest(BaseAFCompareTest):
    current_dir = "shadow_of_chernobyl_Steam"

    def test(self) -> None:
        self._decompile_files()
        self._compare_files()


class ClearSkyAFCompareTest(BaseAFCompareTest):
    current_dir = "clear_sky"

    def test(self) -> None:
        self._decompile_files()
        self._compare_files()


class CallOfPripyatAFCompareTest(BaseAFCompareTest):
    current_dir = "call_of_pripyat"

    def test(self) -> None:
        self._decompile_files()
        self._compare_files()


class BaseCompileCompareTest(BaseCompareTest):
    pass


class ShadowOfChernobylCompileCompareTest1(BaseCompileCompareTest):
    current_dir = "shadow_of_chernobyl_Steam"

    def _compile_files(self):
        config = BaseConfig()
        config.mode = "compile"
        config.common = CommonOptions()
        config.common.out = str(
            Path("data")
            / "results"
            / self.current_dir
            / "python"
            / "spawns"
            / "all.spawn",
        )
        config.common.src = str(
            Path("data") / "results" / self.current_dir / "perl" / "all_cs",
        )
        config.common.sort = "complex"
        config.common.graph_dir = None  # f"data\\sources\\{self.current_dir}"
        config.common.af = None
        config.common.way = False
        config.common.scan_dir = None
        config.common.level_spawn = None
        config.common.nofatal = False
        config.common.af = True

        config.compile = perl_utils.universal_dict_object()
        config.compile.flags = None
        config.compile.idx_file = None
        # 	# split options
        config.split = perl_utils.universal_dict_object()
        config.split.use_graph = False
        config.parse = perl_utils.universal_dict_object()
        config.parse.old_gvid = None
        config.parse.new_gvid = None

        config.common.sections_ini = (
            config.with_scan() if self._get_ini_if_file_exists("sections.ini") else None
        )
        config.common.user_ini = self._get_ini_if_file_exists("user_sections.ini")
        config.common.prefixes_ini = self._get_ini_if_file_exists("way_prefixes.ini")

        m = main(config)
        m.main()

        decompile_perl_result = subprocess.run(
            [
                "perl",
                "universal_acdc.pl",
                "-compile",
                str(Path("data") / "results" / self.current_dir / "perl" / "all_cs"),
                "-out",
                str(
                    Path("data")
                    / "results"
                    / self.current_dir
                    / "perl"
                    / "spawns"
                    / "all.spawn",
                ),
                "-sort",
                "complex",
                # "-g",
                # f"data\\sources\\{self.current_dir}",
                "--af",
            ],
            check=False,
        )
        self.assertEqual(decompile_perl_result.returncode, 0)

    def test_compile(self):
        self._compile_files()
        self.assertFileEquals(
            Path("data")
            / "results"
            / self.current_dir
            / "python"
            / "spawns"
            / "all.spawn",
            Path("data")
            / "results"
            / self.current_dir
            / "perl"
            / "spawns"
            / "all.spawn",
        )


class ShadowOfChernobylCompileCompareTest2(BaseCompileCompareTest):
    current_dir = "shadow_of_chernobyl_Steam"

    def _compile_files(self):
        config = BaseConfig()
        config.mode = "compile"
        config.common = CommonOptions()
        config.common.out = str(
            Path("data")
            / "results"
            / self.current_dir
            / "python"
            / "spawns"
            / "all.spawn",
        )
        config.common.src = str(
            Path("data") / "results" / self.current_dir / "python" / "all_cs",
        )
        config.common.sort = "complex"
        config.common.graph_dir = None  # f"data\\sources\\{self.current_dir}"
        config.common.af = None
        config.common.way = False
        config.common.scan_dir = None
        config.common.level_spawn = None
        config.common.nofatal = False
        config.common.af = True

        config.compile = perl_utils.universal_dict_object()
        config.compile.flags = None
        config.compile.idx_file = None
        # 	# split options
        config.split = perl_utils.universal_dict_object()
        config.split.use_graph = False
        config.parse = perl_utils.universal_dict_object()
        config.parse.old_gvid = None
        config.parse.new_gvid = None

        config.common.sections_ini = (
            config.with_scan() if self._get_ini_if_file_exists("sections.ini") else None
        )
        config.common.user_ini = self._get_ini_if_file_exists("user_sections.ini")
        config.common.prefixes_ini = self._get_ini_if_file_exists("way_prefixes.ini")

        m = main(config)
        m.main()

        decompile_perl_result = subprocess.run(
            [
                "perl",
                "universal_acdc.pl",
                "-compile",
                str(Path("data") / "results" / self.current_dir / "python" / "all_cs"),
                "-out",
                str(
                    Path("data")
                    / "results"
                    / self.current_dir
                    / "perl"
                    / "spawns"
                    / "all.spawn",
                ),
                "-sort",
                "complex",
                # "-g",
                # f"data\\sources\\{self.current_dir}",
                "--af",
            ],
            check=False,
        )
        self.assertEqual(decompile_perl_result.returncode, 0)

    def test_compile(self):
        self._compile_files()
        self.assertFileEquals(
            Path("data")
            / "results"
            / self.current_dir
            / "python"
            / "spawns"
            / "all.spawn",
            Path("data")
            / "results"
            / self.current_dir
            / "perl"
            / "spawns"
            / "all.spawn",
        )


class TestCompareResultsCompareEscapeEscape(BaseCompileCompareTest):
    current_dir = "shadow_of_chernobyl_Steam"

    def _compile_files(self):
        config = BaseConfig()
        config.mode = "compare"
        config.common = CommonOptions()
        config.common.out = str(
            Path("data")
            / "results"
            / self.current_dir
            / "python"
            / "compare"
            / "compare_l01_escape_l01_escape.ltx",
        )
        config.common.src = (
            str(
                Path("data")
                / "sources"
                / self.current_dir
                / "all_cs"
                / "alife_l01_escape.ltx",
            )
            + ","
            + str(
                Path("data")
                / "sources"
                / self.current_dir
                / "all_cs"
                / "alife_l01_escape.ltx",
            )
        )
        config.common.sort = None
        config.common.graph_dir = None  # f"data\\sources\\{self.current_dir}"
        config.common.af = None
        config.common.way = False
        config.common.scan_dir = None
        config.common.level_spawn = None
        config.common.nofatal = False
        config.common.af = True

        config.compile = perl_utils.universal_dict_object()
        config.compile.flags = None
        config.compile.idx_file = None
        # 	# split options
        config.split = perl_utils.universal_dict_object()
        config.split.use_graph = False
        config.parse = perl_utils.universal_dict_object()
        config.parse.old_gvid = None
        config.parse.new_gvid = None

        config.common.sections_ini = (
            config.with_scan() if self._get_ini_if_file_exists("sections.ini") else None
        )
        config.common.user_ini = self._get_ini_if_file_exists("user_sections.ini")
        config.common.prefixes_ini = self._get_ini_if_file_exists("way_prefixes.ini")

        m = main(config)
        m.main()

        decompile_perl_result = subprocess.run(
            [
                "perl",
                "universal_acdc.pl",
                "-compare",
                str(
                    Path("data")
                    / "sources"
                    / self.current_dir
                    / "all_cs"
                    / "alife_l01_escape.ltx",
                )
                + ","
                + str(
                    Path("data")
                    / "sources"
                    / self.current_dir
                    / "all_cs"
                    / "alife_l01_escape.ltx",
                ),
            ],
            check=False,
        )
        self.assertEqual(decompile_perl_result.returncode, 0)

    def test_compare(self):
        self._compile_files()
        self.assertFileEquals(
            Path("data")
            / "results"
            / self.current_dir
            / "python"
            / "compare"
            / "compare_l01_escape_l01_escape.ltx",
            Path("data")
            / "sources"
            / self.current_dir
            / "all_cs"
            / "alife_l01_escape_compared.ltx",
        )

    def tearDown(self) -> None:
        if (
            Path("data")
            / "sources"
            / self.current_dir
            / "all_cs"
            / "alife_l01_escape_compared.ltx"
        ).exists():
            os.remove(
                Path("data")
                / "sources"
                / self.current_dir
                / "all_cs"
                / "alife_l01_escape_compared.ltx",
            )


class TestCompareResultsCompareChaes1Chaes2(BaseCompileCompareTest):
    current_dir = "shadow_of_chernobyl_Steam"

    def _compile_files(self):
        config = BaseConfig()
        config.mode = "compare"
        config.common = CommonOptions()
        config.common.out = str(
            Path("data")
            / "results"
            / self.current_dir
            / "python"
            / "compare"
            / "compare_chaes1_chaes2.ltx",
        )
        config.common.src = (
            str(
                Path("data")
                / "sources"
                / self.current_dir
                / "all_cs"
                / "alife_l12_stancia.ltx",
            )
            + ","
            + str(
                Path("data")
                / "sources"
                / self.current_dir
                / "all_cs"
                / "alife_l12_stancia_2.ltx",
            )
        )
        config.common.sort = None
        config.common.graph_dir = None  # f"data\\sources\\{self.current_dir}"
        config.common.af = None
        config.common.way = False
        config.common.scan_dir = None
        config.common.level_spawn = None
        config.common.nofatal = False
        config.common.af = True

        config.compile = perl_utils.universal_dict_object()
        config.compile.flags = None
        config.compile.idx_file = None
        # 	# split options
        config.split = perl_utils.universal_dict_object()
        config.split.use_graph = False
        config.parse = perl_utils.universal_dict_object()
        config.parse.old_gvid = None
        config.parse.new_gvid = None

        config.common.sections_ini = (
            config.with_scan() if self._get_ini_if_file_exists("sections.ini") else None
        )
        config.common.user_ini = self._get_ini_if_file_exists("user_sections.ini")
        config.common.prefixes_ini = self._get_ini_if_file_exists("way_prefixes.ini")

        m = main(config)
        m.main()

        decompile_perl_result = subprocess.run(
            [
                "perl",
                "universal_acdc.pl",
                "-compare",
                str(
                    Path("data")
                    / "sources"
                    / self.current_dir
                    / "all_cs"
                    / "alife_l12_stancia.ltx",
                )
                + ","
                + str(
                    Path("data")
                    / "sources"
                    / self.current_dir
                    / "all_cs"
                    / "alife_l12_stancia_2.ltx",
                ),
            ],
            check=False,
        )
        self.assertEqual(decompile_perl_result.returncode, 0)

    def test_compare(self):
        self._compile_files()
        self.assertFileEquals(
            Path("data")
            / "results"
            / self.current_dir
            / "python"
            / "compare"
            / "compare_chaes1_chaes2.ltx",
            Path("data")
            / "sources"
            / self.current_dir
            / "all_cs"
            / "alife_l12_stancia_compared.ltx",
        )

    def tearDown(self) -> None:
        if (
            Path("data")
            / "sources"
            / self.current_dir
            / "all_cs"
            / "alife_l12_stancia_compared.ltx"
        ).exists():
            os.remove(
                Path("data")
                / "sources"
                / self.current_dir
                / "all_cs"
                / "alife_l12_stancia_compared.ltx",
            )
