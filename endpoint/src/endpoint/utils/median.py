import dataclasses
from datetime import datetime
from typing import Dict, Optional as Opt, TypeVar

from endpoint.utils.structs import DLList

Value = TypeVar('Value')


@dataclasses.dataclass(frozen=True)
class StreamValue:
    value: int
    date: datetime


@dataclasses.dataclass
class Metrics:
    min: Opt[Value] = None
    max: Opt[Value] = None


@dataclasses.dataclass
class PercentileBuffer:
    size: int
    change_delay: int
    metrics: Metrics = Metrics()
    store: Dict[int, StreamValue] = dataclasses.field(default_factory=dict)

    def append(self, value: StreamValue, sequence: int):
        sequence_keys = self.store.keys()
        if len(sequence_keys) == self.size:
            sequence_value = min(sequence_keys)
            if sequence_value - sequence <= self.change_delay:
                return

            del self.store[sequence_value]

        self.store[sequence] = value

    def replace_lifo(self, s_val: StreamValue, seq: int) -> None:
        candidate_keys = set(self.store.keys())
        if len(candidate_keys) == 0:
            self.store[seq] = s_val

        rm_key = min(candidate_keys)
        while not self.is_min_or_max(rm_key):
            candidate_keys.discard(rm_key)
            rm_key = min(candidate_keys)

        del self.store[rm_key]

        self.store[seq] = s_val

    def is_min_or_max(self, key: int) -> bool:
        return self.store[key].value == self.metrics.max or self.store[key] == self.metrics.min

    def max_sequence(self) -> int:
        return max(self.store.keys())

    def is_full(self) -> bool:
        return len(self.store.keys()) == self.size

    def __reasign(self, store: Dict[int, StreamValue], min: Value, max: Value):
        self.store = store.copy()
        self.metrics.min = min
        self.metrics.max = max

    @classmethod
    def split_buffer(cls, buffer: 'PercentileBuffer') -> 'PercentileBuffer':
        new_buff = cls(
            size=buffer.size,
            change_delay=buffer.change_delay,
        )

        sorted_buffer_items = sorted(
            buffer.store.items(),
            key=lambda x: x[1].value,
        )
        middle_idx = len(sorted_buffer_items) // 2

        new_buff.__reasign(
            dict(sorted_buffer_items[:middle_idx]),
            sorted_buffer_items[0].value,
            sorted_buffer_items[middle_idx - 1].value
        )
        buffer.__reasign(
            dict(sorted_buffer_items[middle_idx:]),
            sorted_buffer_items[middle_idx].value,
            sorted_buffer_items[len(sorted_buffer_items) - 1].value
        )

        return new_buff


class StreamMetrics:
    """
    Stream metrics has 100 buckets for storing values (percentiles)
    Inner stream_sequence for delete oldest values and buckets.

    """
    buffer_count = 100

    def __init__(self, buffer_size: int = 40, check_time: int = 50) -> None:
        self.buffer_size = buffer_size
        self.check_time = check_time
        self.stream_sequence = 0

        self.buffers = DLList(PercentileBuffer(buffer_size, buffer_size * 2))

    def append(self, s_val: StreamValue) -> None:
        if self.stream_sequence > 0:
            if self.buffers._head.val.metrics.min > s_val.value:
                self.buffers._head.val.replace_lifo(s_val)
            elif self.buffers._tail.val.metrics.max < s_val.value:
                self.buffers._tail.val.replace_lifo(s_val)

            for buffer in self.buffers:
                if buffer.metrics.max > s_val.value > buffer.metrics.min.value:
                    if len(self.buffers) != self.buffer_count:
                        if not buffer.is_full():
                            buffer.append(s_val, self.stream_sequence)
                        else:
                            self.split_buffer(buffer)

        else:
            self.buffers._head.val.append(s_val, self.stream_sequence)

        self.stream_sequence += 1

    def split_buffer(self, buffer_for_split: PercentileBuffer):
        for buffer_node in self.buffers.iter_over_nodes():
            if buffer_node.val == buffer_for_split:
                new_buffer = buffer_for_split.split_buffer(buffer_for_split)
                self.buffers.insert(new_buffer, before_node=buffer_node)

    def current_metrics(self):
        pass


