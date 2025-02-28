import dataclasses
import struct
from typing import Any, Generic, TypeVar

T = TypeVar("T")


# Сопоставление форматов
# перла https://perldoc.perl.org/functions/pack
# и питона https://docs.python.org/3/library/struct.html


@dataclasses.dataclass
class UnpackResult(Generic[T]):
    data: T
    unpacked_bytes_length: int


@dataclasses.dataclass
class PackResult:
    packed: bytes
    packed_items_count: int


class ByteNybbles:
    _byte: int
    _low_nybble: int
    _high_nybble: int

    def __init__(self, byte: int):
        self._byte = byte
        low_nybble = byte & 0x0F
        high_nybble = (byte & 0xF0) >> 4
        self._low_nybble = low_nybble
        self._high_nybble = high_nybble

    @property
    def high_nybble(self) -> str:
        return f"{self._high_nybble:x}"

    @property
    def low_nybble(self) -> str:
        return f"{self._low_nybble:x}"


class BaseBinaryFormat(Generic[T]):
    def pack(self, values: tuple[Any, ...]) -> PackResult:
        value: T | None = values[0] if values else None
        if value is None or self._value_is_empty(value):
            packed = self._pack_none()
            return PackResult(packed, 0)
        packed = self._pack(value)
        return PackResult(packed, 1)

    def _value_is_empty(self, value: T | None) -> bool:
        return value is None

    def _pack(self, value: T) -> bytes:
        raise NotImplementedError

    def unpack(self, data: bytes, pos: int = 0) -> UnpackResult[T]:
        raise NotImplementedError

    def get_bytes_length(self) -> int:
        raise NotImplementedError

    def _pack_none(self) -> bytes:
        return b"\0"


class PythonSupportedFormat(BaseBinaryFormat[T]):
    _python_format: str

    def _get_format(self) -> str:
        return self._python_format

    def _pack(self, value: T) -> bytes:
        return struct.pack(self._get_format(), value)

    def unpack(self, data: bytes, pos: int = 0) -> UnpackResult[T]:
        size = self.get_bytes_length()
        part = data[pos : pos + size]
        packed_data = struct.unpack(self._get_format(), part)[0]
        return UnpackResult(packed_data, size)

    def get_bytes_length(self) -> int:
        return struct.calcsize(self._get_format())


# region binary


class HexStringLowNybbleFirst(PythonSupportedFormat[str]):
    # h
    _python_format = "s"

    def _pack(self, value: str) -> bytes:
        low_nybble = int(value[0], base=16)
        byte = low_nybble
        return bytes([byte])


class HexStringHighNybbleFirst(PythonSupportedFormat[str]):
    # H
    _python_format = "s"

    def _pack(self, value: str) -> bytes:
        high_nybble = int(value[0], base=16)
        byte = high_nybble << 4
        return bytes([byte])


# endregion binary


# region strings
class NullPaddedChar(PythonSupportedFormat[bytes]):
    # a
    _python_format = "s"


class SpacePaddedChar(PythonSupportedFormat[bytes]):
    # A
    _python_format = "s"

    def _pack_none(self) -> bytes:
        return b" "

    def _value_is_empty(self, value: T | None) -> bool:
        return value is None or value == b""


class AsciiNullPaddedChar(PythonSupportedFormat[bytes]):
    # Z
    _python_format = "s"

    def _pack(self, value: T) -> bytes:
        return b"\0"


# endregion strings


# region integers
class SignedChar(PythonSupportedFormat[int]):
    # c
    _python_format = "=b"


class UnSignedChar(PythonSupportedFormat[int]):
    # C
    _python_format = "=B"


class SignedShort(PythonSupportedFormat[int]):
    # s
    _python_format = "=h"


class UnSignedShort(PythonSupportedFormat[int]):
    # S
    _python_format = "=H"


class SignedLong(PythonSupportedFormat[int]):
    # l
    _python_format = "=l"


class UnSignedLong(PythonSupportedFormat[int]):
    # L
    _python_format = "=L"


class SignedLongLong(PythonSupportedFormat[int]):
    # q
    _python_format = "=q"


class UnSignedLongLong(PythonSupportedFormat[int]):
    # Q
    _python_format = "=Q"


class SignedInteger(PythonSupportedFormat[int]):
    # i
    _python_format = "=i"


class UnSignedInteger(PythonSupportedFormat[int]):
    # I
    _python_format = "=I"


class NetWorkUnSignedShort(PythonSupportedFormat[int]):
    # n
    _python_format = "!H"


class VAXUnSignedShort(PythonSupportedFormat[int]):
    # v
    _python_format = "<H"


class NetWorkUnSignedLong(PythonSupportedFormat[int]):
    # N
    _python_format = "!L"


class VAXUnSignedLong(PythonSupportedFormat[int]):
    # V
    _python_format = "<L"


# endregion integers


# region floats


class Float(PythonSupportedFormat[float]):
    # f
    _python_format = "f"


class Double(PythonSupportedFormat[float]):
    """Perl не совсем соответствует IEEE754, а python реализует его. Проблема.."""

    # d
    _python_format = "d"


# endregion floats


class FixedLenArray(BaseBinaryFormat[list[T]], Generic[T]):
    # вида FORMAT[COUNT]
    def __init__(self, inner_format: BaseBinaryFormat[T], count: int):
        self._count = count
        self._item_format = inner_format

    def _pack(self, value: list[T]) -> bytes:
        packed = b""
        for item in value:
            packed += self._item_format._pack(item)
        return packed

    def unpack(self, data: bytes, pos: int = 0) -> UnpackResult[list[T]]:
        result = []
        total_bytes = 0
        current_pos = pos
        for _ in range(self._count):
            item_result = self._item_format.unpack(data, current_pos)
            result.append(item_result.data)
            total_bytes += item_result.unpacked_bytes_length
            current_pos += item_result.unpacked_bytes_length
        return UnpackResult(result, total_bytes)

    def get_bytes_length(self) -> int:
        return self._item_format.get_bytes_length() * self._count


class DynamicLenArray(BaseBinaryFormat[list[T]], Generic[T]):
    # LENGTH_TYPE/ITEM_TYPE
    def __init__(
        self,
        inner_format: BaseBinaryFormat[T],
        count_format: BaseBinaryFormat[int],
    ):
        self._count_format = count_format
        self._item_format = inner_format

    def pack(self, values: tuple[Any, ...]) -> PackResult:
        if not values:
            packed = self._pack_none()
            return PackResult(packed, 0)
        packed = b""
        packed += self._count_format._pack(len(values))
        for item in values:
            packed += self._item_format._pack(item)
        return PackResult(packed, len(values))

    def unpack(self, data: bytes, pos: int = 0) -> UnpackResult[list[T]]:
        result: list[T] = []
        total_bytes = 0
        count_unpack_result = self._count_format.unpack(data, pos)
        count = count_unpack_result.data

        total_bytes += count_unpack_result.unpacked_bytes_length
        current_pos = pos + count_unpack_result.unpacked_bytes_length
        for _ in range(count):
            unpacked = self._item_format.unpack(data, current_pos)
            bytes_len = unpacked.unpacked_bytes_length
            if isinstance(unpacked.data, (list, tuple)):
                result.extend(unpacked.data)
            else:
                result.append(unpacked.data)
            total_bytes += bytes_len
            current_pos += bytes_len
        return UnpackResult(result, total_bytes)

    def get_bytes_length(self) -> int:
        msg = "Нельзя определить не распаковав данные"
        raise NotImplementedError(msg)


class UnlimitedLenArray(BaseBinaryFormat[list[T]], Generic[T]):
    # ITEM_TYPE*
    def __init__(self, inner_format: BaseBinaryFormat[T]):
        self._item_format = inner_format

    def _pack(self, value: list[T]) -> bytes:
        packed = b""
        for item in value:
            packed += self._item_format._pack(item)
        return packed

    def unpack(self, data: bytes, pos: int = 0) -> UnpackResult[list[T]]:
        result = []
        total_bytes = 0
        current_pos = pos
        while current_pos < len(data):
            unpack_res = self._item_format.unpack(data, current_pos)
            unpacked_item = unpack_res.data
            bytes_len = unpack_res.unpacked_bytes_length
            result.append(unpacked_item)
            total_bytes += bytes_len
            current_pos += bytes_len
        return UnpackResult(result, total_bytes)

    def get_bytes_length(self) -> int:
        msg = "Нельзя определить не распаковав данные"
        raise NotImplementedError(msg)

    def _pack_none(self) -> bytes:
        return b""


class FixedLenNullPaddedStr(PythonSupportedFormat[bytes]):
    # 10a
    _python_format = "s"

    def __init__(self, count: int):
        self._count = count

    def _get_format(self) -> str:
        return f"{self._count}{self._python_format}"


class FixedLenSpacePaddedStr(PythonSupportedFormat[bytes]):
    # 10A
    _python_format = "s"

    def __init__(self, count: int):
        self._count = count

    def _get_format(self) -> str:
        return f"{self._count}{self._python_format}"


class AsciiNullPaddedStr(PythonSupportedFormat[bytes]):
    # 10Z
    _python_format = "s"

    def __init__(self, count: int):
        self._count = count

    def _get_format(self) -> str:
        return f"{self._count - 1}{self._python_format}"

    def _pack(self, value: bytes) -> bytes:
        return super()._pack(value) + b"\0"


class UnlimitedAsciiString(BaseBinaryFormat[bytes]):
    _inner_format = UnlimitedLenArray[int](UnSignedChar())

    def _pack(self, value: bytes) -> bytes:
        return self._inner_format._pack(list(value))

    def unpack(self, data: bytes, pos: int = 0) -> UnpackResult[bytes]:
        result: UnpackResult[list[int]] = self._inner_format.unpack(data, pos)

        return UnpackResult(bytes(result.data), result.unpacked_bytes_length)

    def _pack_none(self) -> bytes:
        return b""


class UnlimitedAsciiZString(BaseBinaryFormat[str]):
    # Z*
    _inner_format = UnlimitedLenArray[int](UnSignedChar())

    def _pack(self, value: str) -> bytes:
        bytes_str = list(value.encode("cp1251"))
        return self._inner_format._pack(bytes_str) + b"\0"

    def _pack_none(self) -> bytes:
        return b"\0"

    def unpack(self, data: bytes, pos: int = 0) -> UnpackResult[str]:
        if data is None:
            return UnpackResult("\0", 0)
        items_data = data
        end_pos = items_data.find(b"\0", pos)
        if end_pos == -1:
            end_pos = len(items_data)
        result = items_data[pos:end_pos]
        total_bytes = end_pos - pos + 1

        return UnpackResult(bytes(result).decode("cp1251"), total_bytes)


class FirstLowNibbleUnlimitedArray(BaseBinaryFormat[str]):
    # h*

    def _pack(self, value: str) -> bytes:
        result = []
        for i, nybble_str in enumerate(value):
            nybble_num = int(nybble_str)
            is_high = i % 2 == 1
            if is_high:
                nybble_num <<= 4
            if i % 2 == 0:
                result.append(nybble_num)
            else:
                result[-1] += nybble_num
        return bytes(result)

    def _pack_none(self) -> bytes:
        return b"\0"

    def unpack(self, data: bytes, pos: int = 0) -> UnpackResult[str]:
        result = ""
        chunk = data[pos:]
        for byte in chunk:
            nybbles = ByteNybbles(byte)
            current = f"{nybbles.low_nybble}{nybbles.high_nybble}"
            result += current
        return UnpackResult(result, len(chunk))

    def get_bytes_length(self) -> int:
        msg = "Нельзя определить не распаковав данные"
        raise NotImplementedError(msg)


class FirstHighNibbleUnlimitedArray(BaseBinaryFormat[str]):
    # H*

    def _pack(self, value: str) -> bytes:
        result = []
        for i, nybble_str in enumerate(value):
            nybble_num = int(nybble_str, base=16)
            is_high = i % 2 == 0
            if is_high:
                nybble_num <<= 4
            if i % 2 == 0:
                result.append(nybble_num)
            else:
                result[-1] += nybble_num
        return bytes(result)

    def _pack_none(self) -> bytes:
        return b"\0"

    def unpack(self, data: bytes, pos: int = 0) -> UnpackResult[str]:
        result = ""
        chunk = data[pos:]
        for byte in chunk:
            nybbles = ByteNybbles(byte)
            current = f"{nybbles.high_nybble}{nybbles.low_nybble}"
            result += current
        return UnpackResult(result, len(chunk))

    def get_bytes_length(self) -> int:
        msg = "Нельзя определить не распаковав данные"
        raise NotImplementedError(msg)


class FirstLowNibbleCountedArray(BaseBinaryFormat[str]):
    # h5

    def __init__(self, count: int) -> None:
        self._count = count

    def _pack(self, value: str) -> bytes:
        result = []
        for i, nybble_str in enumerate(value):
            if i >= self._count:
                break
            nybble_num = int(nybble_str)
            is_high = i % 2 == 1
            if is_high:
                nybble_num <<= 4
            if i % 2 == 0:
                result.append(nybble_num)
            else:
                result[-1] += nybble_num
        return bytes(result)

    def _pack_none(self) -> bytes:
        return b"\0"

    def unpack(self, data: bytes, pos: int = 0) -> UnpackResult[str]:
        result = ""
        for nybble_index in range(self._count):
            byte_index = nybble_index // 2 + pos
            if byte_index >= len(data):
                break
            byte = data[byte_index]
            nybbles = ByteNybbles(byte)
            current = (
                f"{nybbles.low_nybble}"
                if nybble_index % 2 == 0
                else f"{nybbles.high_nybble}"
            )
            result += current
        return UnpackResult(result, len(data) - pos)


class FirstHighNibbleCounteddArray(BaseBinaryFormat[str]):
    # H5

    def __init__(self, count: int) -> None:
        self._count = count

    def _pack(self, value: str) -> bytes:
        result = []
        for i, nybble_str in enumerate(value):
            if i >= self._count:
                break
            nybble_num = int(nybble_str)
            is_high = i % 2 == 0
            if is_high:
                nybble_num <<= 4
            if i % 2 == 0:
                result.append(nybble_num)
            else:
                result[-1] += nybble_num
        res = bytes(result)
        if len(value) < self._count:
            res += b"\0"
        return res

    def _pack_none(self) -> bytes:
        return b"\0"

    def unpack(self, data: bytes, pos: int = 0) -> UnpackResult[str]:
        result = ""
        for nybble_index in range(self._count):
            byte_index = nybble_index // 2 + pos
            if byte_index >= len(data):
                break
            byte = data[byte_index]
            nybbles = ByteNybbles(byte)
            current = (
                f"{nybbles.high_nybble}"
                if nybble_index % 2 == 0
                else f"{nybbles.low_nybble}"
            )
            result += current
        return UnpackResult(result, len(data) - pos)


class GroupFormat(BaseBinaryFormat[tuple[Any, ...]]):
    _child_formats: tuple[BaseBinaryFormat[Any], ...]

    def __init__(self, child_formats: tuple[BaseBinaryFormat[Any], ...]):
        super().__init__()
        self._child_formats = child_formats

    def pack(self, values: tuple[Any, ...]) -> PackResult:
        current_args = values
        total_packed = b""
        total_packed_items = 0
        for _format in self._child_formats:
            try:
                current_pack_result = _format.pack(current_args)
            except Exception as ex:
                msg = f"Error pack {_format=} {current_args=}"
                raise ValueError(msg) from ex
            total_packed += current_pack_result.packed
            total_packed_items += current_pack_result.packed_items_count
            current_args = (
                current_args[current_pack_result.packed_items_count :]
                if current_pack_result.packed_items_count < len(current_args)
                else tuple()  # noqa: C408
            )
        return PackResult(total_packed, total_packed_items)

    def unpack(self, data: bytes, pos: int = 0) -> UnpackResult[tuple[Any, ...]]:
        result: list[Any] = []
        total_unpacked_bytes = 0
        current_pos = pos
        for _format in self._child_formats:
            try:
                unpack_result = _format.unpack(data, current_pos)
            except Exception as ex:
                data_part = data[current_pos:]
                msg = f"Unpack error {_format=}, {current_pos=}. {data_part=}, {data=}"
                raise ValueError(msg) from ex
            if isinstance(unpack_result.data, (tuple, list)):
                result.extend(unpack_result.data)
            else:
                result.append(unpack_result.data)
            total_unpacked_bytes += unpack_result.unpacked_bytes_length
            current_pos += unpack_result.unpacked_bytes_length
        return UnpackResult(tuple(result), total_unpacked_bytes)

    def __str__(self) -> str:
        return f"GroupFormat({self._child_formats})"

    def __repr__(self) -> str:
        return f"GroupFormat({self._child_formats})"
