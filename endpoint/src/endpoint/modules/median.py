import dataclasses
import logging
from datetime import datetime
from typing import Dict, Optional as Opt, TypeVar, Union

from endpoint.modules.structs import DLList

logger = logging.getLogger("info_log")

Value = TypeVar("Value")


@dataclasses.dataclass(frozen=True, eq=False)
class StreamValue:
    value: float
    date: datetime
    __EPSILON = 0.0001

    @staticmethod
    def __get_value(container: Union["StreamValue", int, float]) -> Union[float, int]:
        if isinstance(container, StreamValue):
            return container.value
        elif isinstance(container, (float, int)):
            return container
        else:
            raise TypeError(f"Comparing is not implemented for {type(container)}")

    def __lt__(self, other: "StreamValue") -> bool:
        v2 = self.__get_value(other)

        return v2 - self.value >= self.__EPSILON

    def __gt__(self, other: "StreamValue") -> bool:
        v2 = self.__get_value(other)

        return self.value - v2 >= self.__EPSILON

    def __eq__(self, other: Union["StreamValue", float, int]) -> bool:
        v2 = self.__get_value(other)

        return abs(self.value - v2) < self.__EPSILON


@dataclasses.dataclass
class Metrics:
    min: Opt[Value] = None
    max: Opt[Value] = None


@dataclasses.dataclass
class PercentileBuffer:
    size: int
    change_delay: int
    metrics: Metrics = dataclasses.field(default_factory=Metrics)
    store: Dict[int, StreamValue] = dataclasses.field(default_factory=dict)

    def set_min_max(self, val: StreamValue) -> None:
        if self.metrics.max is None:
            self.metrics.max = val.value
            self.metrics.min = val.value
        elif val > self.metrics.max:
            self.metrics.max = val.value
        elif val < self.metrics.min:
            self.metrics.min = val.value

    def append(self, val: StreamValue, seq: int) -> None:
        sequence_keys = self.store.keys()
        if len(sequence_keys) == self.size:
            sequence_value = min(sequence_keys)
            if sequence_value - seq <= self.change_delay:
                return

            del self.store[sequence_value]

        self.store[seq] = val
        self.set_min_max(val)

    def __replace_lifo(self, val: StreamValue, seq: int) -> None:
        candidate_keys = set(self.store.keys())
        if len(candidate_keys) == 0:
            self.store[seq] = val
            self.set_min_max(val)

        rm_key = min(candidate_keys)
        while not self.is_min_or_max(rm_key):
            candidate_keys.discard(rm_key)
            rm_key = min(candidate_keys)

        del self.store[rm_key]

        self.store[seq] = val
        self.set_min_max(val)

    def insert(self, val: StreamValue, seq: int) -> None:
        if self.is_full():
            self.__replace_lifo(val, seq)
        else:
            self.append(val, seq)

        self.set_min_max(val)

    def is_min_or_max(self, key: int) -> bool:
        return (
            self.store[key].value == self.metrics.max
            or self.store[key].value == self.metrics.min
        )

    def max_sequence(self) -> int:
        return max(self.store.keys())

    def is_full(self) -> bool:
        return len(self.store.keys()) == self.size

    def __reasign(self, store: Dict[int, StreamValue], min: Value, max: Value):
        self.store = store.copy()
        self.metrics.min = min
        self.metrics.max = max

    def split_buffer(self) -> "PercentileBuffer":
        new_buff = self.__class__(size=self.size, change_delay=self.change_delay)

        sorted_buffer_items = sorted(self.store.items(), key=lambda x: x[1].value)
        middle_idx = len(sorted_buffer_items) // 2

        new_buff.__reasign(
            dict(sorted_buffer_items[:middle_idx]),
            sorted_buffer_items[0][1].value,
            sorted_buffer_items[middle_idx - 1][1].value,
        )
        self.__reasign(
            dict(sorted_buffer_items[middle_idx:]),
            sorted_buffer_items[middle_idx][1].value,
            sorted_buffer_items[len(sorted_buffer_items) - 1][1].value,
        )

        return new_buff

    def __len__(self) -> int:
        return len(self.store)


class StreamMetrics:
    """
    Stream metrics has 100 buckets for storing values (percentiles)
    Inner stream_sequence for delete oldest values and buckets.

    """

    max_number_of_buffer = 100

    def __init__(self, buffer_size: int = 40, check_time: int = 50) -> None:
        self.buffer_size = buffer_size
        self.check_time = check_time
        self.stream_sequence = 0

        self.buffers = DLList(PercentileBuffer(buffer_size, buffer_size * 2))

    def append(self, val: StreamValue) -> None:
        if self.stream_sequence > 0:
            if self.buffers.head.val.metrics.min > val.value:
                self.buffers.head.val.insert(val, self.stream_sequence)
            elif self.buffers.tail.val.metrics.max < val.value:
                self.buffers.tail.val.insert(val, self.stream_sequence)

            prev_buffer = None
            for buffer in self.buffers:
                if buffer.metrics.max >= val.value >= buffer.metrics.min:
                    if len(self.buffers) != self.max_number_of_buffer:
                        if not buffer.is_full():
                            buffer.append(val, self.stream_sequence)
                        else:
                            self.split_buffer(buffer)
                elif (
                    prev_buffer
                    and prev_buffer.metrics.max < val.value < buffer.metrics.min
                ):
                    if len(prev_buffer) <= len(buffer):
                        prev_buffer.insert(val, self.stream_sequence)
                    else:
                        buffer.insert(val, self.stream_sequence)
                prev_buffer = buffer

        else:
            self.buffers.head.val.append(val, self.stream_sequence)

        self.stream_sequence += 1

    def split_buffer(self, buffer_for_split: PercentileBuffer) -> None:
        for buffer_node in self.buffers.iter_over_nodes():
            if buffer_node.val == buffer_for_split:
                node = buffer_node

        new_buffer = buffer_for_split.split_buffer()
        self.buffers.insert(new_buffer, before_node=node)

    def current_metrics(self) -> Dict[int, Union[int, float]]:
        if self.stream_sequence < self.max_number_of_buffer * self.buffer_size:
            raise Exception("Not enough data")

        percentiles = {}
        for i, buffer in enumerate(self.buffers):
            if i == 24:
                percentiles[25] = buffer.metrics.max
            elif i == 49:
                percentiles[50] = buffer.metrics.max
            elif i == 74:
                percentiles[75] = buffer.metrics.max

        return percentiles
