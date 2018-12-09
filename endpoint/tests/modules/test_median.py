import pytest

from endpoint.modules.median import Metrics


class TestMetrics:
    def test_metrics_init(self):
        m = Metrics(13, 15)
        assert m.min == 13
        assert m.max == 15

        m2 = Metrics(12)
        assert m2.min == 12
        assert m2.max is None

    def test_metrics_contains(self):
        m = Metrics(13, 15)
        assert m.__contains__(14) is True
