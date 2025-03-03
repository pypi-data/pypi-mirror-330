from enum import Enum
from typing import Any, Dict

from ul_unipipeline.message.uni_message import UniMessage


class BsLogType(Enum):
    device_data = "device_data"
    heartbit = "heartbit"


class BsDataLoggerInputV0Message(UniMessage):
    latitude: float
    longitude: float
    soft: str | None = None
    station_id: int
    time: float
    log_type: BsLogType | None = None
    init_message: Dict[str, Any] | None = None
