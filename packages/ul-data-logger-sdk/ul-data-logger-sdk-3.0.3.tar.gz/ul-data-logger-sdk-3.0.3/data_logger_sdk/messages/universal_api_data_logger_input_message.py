from datetime import datetime
from enum import Enum
from typing import Any, Dict

from ul_unipipeline.message.uni_message import UniMessage


class UniversalApiType(Enum):
    USPD = "USPD"
    GENERAL_API = "GENERAL_API"


class UniversalApiDataLoggerInputV0Message(UniMessage):
    name: str
    type: UniversalApiType
    geo_latitude: float
    geo_longitude: float
    soft: str | None = None
    note: str | None = None
    ipv4: str | None = None
    current_dt: datetime
    uptime_s: int
    raw_message: str | Dict[str, Any]
