import asyncio
import time
from unittest.mock import Mock
from uuid import uuid4

from huntflow_base_metrics.base import (
    COMMON_LABELS_VALUES,
    REGISTRY,
    observe_metrics,
    register_method_observe_histogram,
    start_metrics,
)


async def test_disabled_metrics():
    histogram_mock = Mock()
    method = "asdfg"

    @observe_metrics(method, histogram_mock)
    async def observable_func(sleep_time=None):
        if sleep_time:
            await asyncio.sleep(sleep_time)
        return sleep_time

    @observe_metrics(method, histogram_mock)
    def sync_observable_func(sleep_time=None):
        if sleep_time:
            time.sleep(sleep_time)
        return sleep_time

    sleep_time = 0.3
    result = await observable_func(sleep_time)
    assert sleep_time == result

    result = sync_observable_func(sleep_time)
    assert sleep_time == result

    assert not histogram_mock.labels.called


async def test_histogram_metrics():
    method = "asdfg"
    metric_name = "test_timing_histogram"
    histogram = register_method_observe_histogram(metric_name, "Test histogram")

    @observe_metrics(method, histogram)
    async def observable_func(sleep_time=None):
        if sleep_time:
            await asyncio.sleep(sleep_time)
        return sleep_time

    facility_name = uuid4().hex
    facility_id = uuid4().hex

    start_metrics(facility_name, facility_id)

    sleep_time = 0.3
    result = await observable_func(sleep_time)
    assert sleep_time == result

    labels = COMMON_LABELS_VALUES.copy()
    labels.update(
        {
            "method": method,
        }
    )

    time_sum = REGISTRY.get_sample_value(
        "test_timing_histogram_sum",
        labels,
    )
    assert time_sum is not None
    assert sleep_time <= time_sum < sleep_time + 0.01

    @observe_metrics(method, histogram)
    def sync_observable_func(sleep_time=None):
        if sleep_time:
            time.sleep(sleep_time)
        return sleep_time

    result = sync_observable_func(sleep_time)
    assert sleep_time == result

    time_sum = REGISTRY.get_sample_value(
        "test_timing_histogram_sum",
        labels,
    )
    assert time_sum is not None
    assert sleep_time * 2 <= time_sum < sleep_time * 2 + 0.01
