# Note: this file is a copy of the one in https://github.com/griptape-ai/griptape/
from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from attrs import define


@define
class BaseSqlDriver(ABC):
    @dataclass
    class RowResult:
        cells: dict[str, Any]

    @abstractmethod
    def execute_query(self, query: str) -> list[RowResult] | None: ...

    @abstractmethod
    def execute_query_raw(self, query: str) -> list[dict[str, Any]] | None: ...

    @abstractmethod
    def get_table_schema(self, table_name: str, schema: str | None = None) -> str | None: ...
