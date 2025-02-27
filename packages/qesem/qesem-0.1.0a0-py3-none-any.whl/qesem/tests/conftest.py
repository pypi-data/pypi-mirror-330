"""Pytest configuration for qesem tests."""
from collections.abc import Iterator
from typing import Any

import loguru
import pytest


logger = loguru.logger


@pytest.fixture
def caplog(
    caplog: pytest.LogCaptureFixture,  # pylint: disable=redefined-outer-name
) -> Iterator[pytest.LogCaptureFixture]:
    """Emitting logs from loguru's logger.log means that they will not show up in
    caplog which only works with Python's standard logging. This adds the same
    LogCaptureHandler being used by caplog to hook into loguru.

    Args:
        caplog (LogCaptureFixture): caplog fixture

    Yields:
        LogCaptureFixture
    """

    def filter_(record: Any) -> bool:
        return record["level"].no >= caplog.handler.level  # type: ignore[no-any-return]

    handler_id = logger.add(caplog.handler, level=0, format="{message}", filter=filter_)
    yield caplog
    logger.remove(handler_id)
