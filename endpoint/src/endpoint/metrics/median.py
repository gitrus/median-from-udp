import dataclasses
from typing import List


@dataclasses.dataclass
class PercentileBuffer:
    store: List[int]
    size: int
    max_index: int
    is_empty: bool = True

    def append(self, value: int):
        is_empty = False

        if len(self.store) < self.size-1:
            self.store.append(value)  # TODO: here sort append
        else:
            pass  # TODO: here remove some element


class StreamMetrics:
    def __init__(self, buffer_size: int = 40) -> None:
        self.buffer_size = buffer_size
        self.total_length = 0

        self.candidates_25_percentile = []
        self.candidates_50_percentile = []
        self.candidates_75_percentile = []

    def append(self, value) -> None:
        if self.total_length > self.buffer_size * 3:
            pass

        else:
            pass
