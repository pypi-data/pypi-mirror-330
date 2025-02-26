from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal, TypedDict, TypeVar

from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin

IpCheckLookupSource = Literal["MaxMind", "NEP"]
IpCheckAccessGroup = Literal["NO", "EEA", "WORLD"]
DisplayAspectRatioVideo = Literal["16:9", "4:3"]

T = TypeVar("T", bound="DataClassORJSONMixin")


@dataclass
class BaseDataClassORJSONMixin(DataClassORJSONMixin):
    class Config(BaseConfig):
        omit_none = True
        allow_deserialization_not_by_alias = True


@dataclass
class IpCheck(BaseDataClassORJSONMixin):
    client_ip_address: str = field(metadata=field_options(alias="clientIpAddress"))
    country_code: str = field(metadata=field_options(alias="countryCode"))
    is_ip_norwegian: bool = field(metadata=field_options(alias="isIpNorwegian"))
    lookup_source: IpCheckLookupSource = field(metadata=field_options(alias="lookupSource"))
    access_group: IpCheckAccessGroup = field(metadata=field_options(alias="accessGroup"))


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def from_str(cls, value: str) -> StrEnum:
        return cls(value)


class Operation(TypedDict):
    """API operation (to be implemented)."""

    response_class: type[BaseDataClassORJSONMixin]
    path: str


class FetchedFileInfo(TypedDict):
    """Fetched file info."""

    content_length: int
    content_type: str | None


class SortOrder(StrEnum):
    """Sort order."""

    ASCENDING = "ascending"
    DESCENDING = "descending"


@dataclass
class Enabled(BaseDataClassORJSONMixin):
    """Enabled status."""

    enabled: bool
