from collections.abc import Iterator
from typing import overload
from typing_extensions import Self

__all__ = ["Range", "ContentRange"]

class Range:
    start: int | None
    end: int | None
    @overload
    def __init__(self, start: None, end: None) -> None: ...
    @overload
    def __init__(self, start: int, end: int | None) -> None: ...
    def range_for_length(self, length: int | None) -> tuple[int, int] | None: ...
    def content_range(self, length: int | None) -> ContentRange | None: ...
    def __iter__(self) -> Iterator[int | None]: ...
    @classmethod
    def parse(cls, header: str | None) -> Self | None: ...

class ContentRange:
    start: int | None
    stop: int | None
    length: int | None
    @overload
    def __init__(self, start: None, stop: None, length: int | None) -> None: ...
    @overload
    def __init__(self, start: int, stop: int, length: int | None) -> None: ...
    def __iter__(self) -> Iterator[int | None]: ...
    @classmethod
    def parse(cls, value: str | None) -> Self | None: ...
