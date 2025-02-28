import json
import struct
import unittest
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any, ClassVar, TypedDict

from perl_binary_packing import pack, unpack


class ValueWithFormat(TypedDict):
    type: str  # noqaA003,VNE003
    value: Any


class TestPackData(TypedDict):
    used_format: str
    to_pack: list[ValueWithFormat]
    expected_packed: bytes


class TestUnPackData(TypedDict):
    used_format: str
    to_unpack: bytes
    expected_unpacked: list[ValueWithFormat]


class TestFinal(unittest.TestCase):
    json_test_file = "test_data.json"
    _test_packing: ClassVar[list[TestPackData]] = []
    _test_unpacking: ClassVar[list[TestUnPackData]] = []

    @classmethod
    def _binary_hexes_to_bytes(cls, expected_packed_str: list[str]) -> bytes:
        return b"".join(
            [struct.pack("B", int(byte, 16)) for byte in expected_packed_str],
        )

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        with Path(cls.json_test_file).open(encoding="cp1251") as file:
            test_data = json.load(file)

        if "test_pack" in test_data:
            test_packing = test_data["test_pack"]

            cls._test_packing = [
                TestPackData(
                    used_format=test_pack["format"],
                    to_pack=test_pack["to_pack"],
                    expected_packed=cls._binary_hexes_to_bytes(
                        test_pack["expected_packed"],
                    ),
                )
                for test_pack in test_packing
            ]
        if "test_unpack" in test_data:
            test_unpacking = test_data["test_unpack"]

            cls._test_unpacking = [
                TestUnPackData(
                    used_format=test_unpack["format"],
                    to_unpack=cls._binary_hexes_to_bytes(test_unpack["to_unpack"]),
                    expected_unpacked=test_unpack["expected_unpacked"],
                )
                for test_unpack in test_unpacking
            ]

    def _format_bytes(self, _bin: bytes) -> str:
        result = ""
        for byte in _bin:
            result += hex(byte) + " "
        return result

    def test_packing(self) -> None:
        for test_pack in self._test_packing:
            with self.subTest(**test_pack):
                self._subtest_pack(test_pack)

    def _subtest_pack(self, test_pack: TestPackData) -> None:
        _format = test_pack["used_format"]
        to_pack = test_pack["to_pack"]
        expected = test_pack["expected_packed"]
        to_pack = [self._format_value(item) for item in to_pack]
        packed = pack(_format, *to_pack)
        to_pack_view = self._format_array(to_pack)
        test_msg = f'Checking: pack({_format}, {to_pack_view})/ Expected: "{self._format_bytes(expected)}", actual: "{self._format_bytes(packed)}"'
        self.assertEqual(
            expected,
            packed,
            test_msg,
        )

    def test_unpacking(self) -> None:
        for test_unpack in self._test_unpacking:
            with self.subTest(**test_unpack):
                self._subtest_unpack(test_unpack)

    def _format_value(self, expected_object: ValueWithFormat) -> Any:
        _type = expected_object["type"]
        raw_value = expected_object["value"]
        possible_types: dict[str, Callable[[Any], object]] = {
            "str": lambda s: str(s),
            "bytes": lambda s: s.replace("0x00", "\0").encode(),
            "int": lambda s: int(s),
            "float": lambda s: float(s),
        }
        return possible_types[_type](raw_value)

    def _subtest_unpack(self, test_unpack: TestUnPackData) -> None:
        _format = test_unpack["used_format"]
        to_unpack = test_unpack["to_unpack"]
        expected_objects = test_unpack["expected_unpacked"]
        expected_values = [
            self._format_value(expected_object) for expected_object in expected_objects
        ]
        unpacked = list(unpack(_format, to_unpack))
        expected_view = self._format_array(expected_values)
        unpacked_view = self._format_array(unpacked)
        test_msg = f'Checking: pack({_format}, {self._format_bytes(to_unpack)})/ Expected: "{expected_view}", actual: "{unpacked_view}"'
        self.assertListEqual(
            expected_values,
            unpacked,
            test_msg,
        )

    def _format_array(self, arr: Iterable[Any]) -> str:
        return "[" + ", ".join(f'"{s}"' for s in arr) + "]"
