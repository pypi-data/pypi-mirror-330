import asyncio
import logging
from typing import Tuple

import aiofiles
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, generate_latest

from ._context import METRIC_CONTEXT as _METRIC_CONTEXT

LOGGER = logging.getLogger(__name__)

# Limit for a series of exceptions during saving metrics to file.
# Just to not send too much spam to sentry.
# If we failed to write to a file with this limit, the most probably
# we will fail in the future too. Possible errors:
# * not mounted directory (only container restart will help)
# * insufficiient rights to write to the directory
# * no space left on the disk
_MAX_FILE_WRITE_ERRORS = 5


async def _update_metric_file(
    file_path: str, update_delay: float, registry: CollectorRegistry
) -> None:
    LOGGER.info("Writing metrics to %s", file_path)
    err_count = 0
    while True:
        await asyncio.sleep(update_delay)
        try:
            LOGGER.debug("Updating metrics file")
            async with aiofiles.open(file_path, "wb") as dst:
                await dst.write(generate_latest(registry))
            err_count = 0
        except asyncio.CancelledError:
            LOGGER.info("Write metric task is cancelled")
            break
        except Exception:
            err_count += 1
            LOGGER.warning("Failed to write metrics to file: %s", file_path)
            if err_count >= _MAX_FILE_WRITE_ERRORS:
                LOGGER.exception("Update metrics file: total number of errors %s. Exit", err_count)
                break


def start_export_to_file(file_path: str, update_delay: float) -> None:
    """Starts background asyncio task to dump metrics into a file.
    :param file_path: file name
    :param update_delay: interval in seconds between writing to file.
    """
    assert file_path
    assert _METRIC_CONTEXT.registry is not None
    task = asyncio.create_task(
        _update_metric_file(file_path, update_delay, _METRIC_CONTEXT.registry)
    )
    _METRIC_CONTEXT.write_to_file_task = task


def stop_export_to_file() -> None:
    task = _METRIC_CONTEXT.write_to_file_task
    if task is not None:
        task.cancel()
    _METRIC_CONTEXT.write_to_file_task = None


def export_to_http_response() -> Tuple[bytes, str]:
    """Returns tuple of exported metrics and content-type value"""
    assert _METRIC_CONTEXT.registry is not None
    return generate_latest(_METRIC_CONTEXT.registry), CONTENT_TYPE_LATEST
