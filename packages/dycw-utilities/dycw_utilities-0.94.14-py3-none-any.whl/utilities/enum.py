from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import Generic, Literal, TypeAlias, TypeVar, assert_never, overload

from typing_extensions import override

from utilities.errors import ImpossibleCaseError
from utilities.functions import ensure_str
from utilities.iterables import _OneStrEmptyError, _OneStrNonUniqueError, one_str
from utilities.types import EnumOrStr

_E = TypeVar("_E", bound=Enum)


##


@overload
def ensure_enum(
    value: None, enum: type[_E], /, *, case_sensitive: bool = ...
) -> None: ...
@overload
def ensure_enum(
    value: EnumOrStr[_E], enum: type[_E], /, *, case_sensitive: bool = ...
) -> _E: ...
def ensure_enum(
    value: EnumOrStr[_E] | None, enum: type[_E], /, *, case_sensitive: bool = False
) -> _E | None:
    """Ensure the object is a member of the enum."""
    if value is None:
        return None
    if isinstance(value, enum):
        return value
    if isinstance(value, Enum):
        raise _EnsureEnumTypeEnumError(value=value, enum=enum)
    try:
        return parse_enum(value, enum, case_sensitive=case_sensitive)
    except ParseEnumError as error:
        raise _EnsureEnumParseError(value=error.value, enum=error.enum) from None


@dataclass(kw_only=True, slots=True)
class EnsureEnumError(Exception, Generic[_E]):
    value: EnumOrStr[_E]
    enum: type[_E]


@dataclass(kw_only=True, slots=True)
class _EnsureEnumTypeEnumError(EnsureEnumError):
    @override
    def __str__(self) -> str:
        return f"{self.value!r} is not an instance of {self.enum!r}"


@dataclass(kw_only=True, slots=True)
class _EnsureEnumParseError(EnsureEnumError):
    @override
    def __str__(self) -> str:
        return f"Unable to ensure enum; got {self.value!r}"


##


def parse_enum(
    value: str, enum: type[_E], /, *, case_sensitive: bool = False
) -> _E | None:
    """Parse a string into the enum."""
    by_name = _parse_enum_one(value, enum, "names", case_sensitive=case_sensitive)
    if not issubclass(enum, StrEnum):
        if by_name is not None:
            return by_name
        raise _ParseEnumGenericEnumEmptyError(
            value=value,
            enum=enum,
            case_sensitive=case_sensitive,
            names_or_values="names",
        )
    by_value = _parse_enum_one(value, enum, "values", case_sensitive=case_sensitive)
    if (by_name is None) and (by_value is None):
        raise _ParseEnumStrEnumEmptyError(
            value=value, enum=enum, case_sensitive=case_sensitive
        )
    if (by_name is not None) and (by_value is None):
        return by_name
    if (by_name is None) and (by_value is not None):
        return by_value
    if (by_name is not None) and (by_value is not None):
        if by_name is by_value:
            return by_name
        raise _ParseEnumStrEnumNonUniqueError(
            value=value,
            enum=enum,
            case_sensitive=case_sensitive,
            by_name=by_name.name,
            by_value=by_value.name,
        )
    raise ImpossibleCaseError(case=[f"{by_name=}", f"{by_value=}"])  # pragma: no cover


_NamesOrValues: TypeAlias = Literal["names", "values"]


def _parse_enum_one(
    value: str,
    enum: type[_E],
    names_or_values: _NamesOrValues,
    /,
    *,
    case_sensitive: bool = False,
) -> _E | None:
    """Pair one aspect of the enums."""
    match names_or_values:
        case "names":
            names = [e.name for e in enum]
        case "values":
            names = [ensure_str(e.value) for e in enum]
        case _ as never:
            assert_never(never)
    try:
        name = one_str(names, value, case_sensitive=case_sensitive)
    except _OneStrEmptyError:
        return None
    except _OneStrNonUniqueError as error:
        raise _ParseEnumByKindNonUniqueError(
            value=value,
            enum=enum,
            names_or_values=names_or_values,
            first=error.first,
            second=error.second,
        ) from None
    index = names.index(name)
    return list(enum)[index]


@dataclass(kw_only=True, slots=True)
class ParseEnumError(Exception, Generic[_E]):
    value: str
    enum: type[_E]


@dataclass(kw_only=True, slots=True)
class _ParseEnumByKindNonUniqueError(ParseEnumError):
    names_or_values: _NamesOrValues
    first: str
    second: str

    @override
    def __str__(self) -> str:
        desc = "StrEnum" if issubclass(self.enum, StrEnum) else "Enum"
        return f"{desc} {self.enum.__name__!r} member {self.names_or_values} must contain {self.value!r} exactly once (modulo case); got {self.first!r}, {self.second!r} and perhaps more"


@dataclass(kw_only=True, slots=True)
class _ParseEnumGenericEnumEmptyError(ParseEnumError):
    names_or_values: _NamesOrValues
    case_sensitive: bool = False

    @override
    def __str__(self) -> str:
        desc = f"Enum {self.enum.__name__!r} member {self.names_or_values} do not contain {self.value!r}"
        if not self.case_sensitive:
            desc += " (modulo case)"
        return desc


@dataclass(kw_only=True, slots=True)
class _ParseEnumStrEnumEmptyError(ParseEnumError):
    case_sensitive: bool = False

    @override
    def __str__(self) -> str:
        desc = f"StrEnum {self.enum.__name__!r} member names and values do not contain {self.value!r}"
        if not self.case_sensitive:
            desc += " (modulo case)"
        return desc


@dataclass(kw_only=True, slots=True)
class _ParseEnumStrEnumNonUniqueError(ParseEnumError):
    case_sensitive: bool = False
    by_name: str
    by_value: str

    @override
    def __str__(self) -> str:
        desc = f"StrEnum {self.enum.__name__!r} member names and values must contain {self.value!r} exactly once"
        if not self.case_sensitive:
            desc += " (modulo case)"
        return f"{desc}; got {self.by_name!r} by name and {self.by_value!r} by value"


__all__ = [
    "EnsureEnumError",
    "EnumOrStr",
    "ParseEnumError",
    "ensure_enum",
    "parse_enum",
]
