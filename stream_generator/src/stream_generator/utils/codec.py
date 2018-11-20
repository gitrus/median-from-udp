from datetime import datetime
from typing import Union, Any, Tuple


def decode_msg(obj: Union[str, int, float]) -> Union[datetime, int, float]:
    if isinstance(obj, str):
        return datetime.strptime(obj, "%Y%m%dT%H:%M:%S.%f")
    elif isinstance(obj, (int, float)):
        return obj
    else:
        raise NotImplementedError()


def encode_msg(obj: Union[datetime, int, float]) -> Union[str, int, float]:
    if isinstance(obj, datetime):
        return obj.strftime("%Y%m%dT%H:%M:%S.%f")
    elif isinstance(obj, (int, float)):
        return obj
    else:
        raise NotImplementedError()
