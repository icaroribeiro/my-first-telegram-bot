import asyncio
import random
from typing import Any

from app.core.logging.logger import get_logger
from app.infrastructure.task_queue.models.task_item_model import TaskItemModel
from app.infrastructure.task_queue.task_queue import TaskQueue

logger = get_logger()


class TaskQueueConsumer:
    def __init__(
        self,
        task_queue: TaskQueue,
        max_retries: int,
        initial_backoff_seconds: float,
        async_task_timeout_seconds: float,
    ) -> None:
        self.task_queue = task_queue
        self.max_retries = max_retries
        self.initial_backoff_seconds = initial_backoff_seconds
        self.async_task_timeout_seconds = async_task_timeout_seconds
        self._running_task: asyncio.Task[Any] | None = None
        self.should_stop = asyncio.Event()

    async def _consume_task_with_retry(self, task_item: TaskItemModel) -> bool:
        logger.info(f"Consuming {task_item}...")
        is_final_attempt: bool = False
        for attempt in range(self.max_retries + 1):
            if attempt == self.max_retries:
                is_final_attempt = True
            try:
                logger.info(
                    f"{task_item} Starting attempt {attempt + 1}/{self.max_retries + 1}..."
                )
                success = await task_item.async_func()
                if success:
                    logger.info(f"{task_item} consumed.")
                    return True
                else:
                    if not is_final_attempt:
                        retry_delay = self.initial_backoff_seconds * (2**attempt)
                        logger.warning(
                            f"{task_item} Recoverable failure. Retrying in {retry_delay:.2f}s..."
                        )
                        await asyncio.sleep(delay=retry_delay)
                    else:
                        logger.error(
                            f"{task_item} Failed after all {self.max_retries + 1} attempts. Giving up."
                        )
                        return False
            except Exception as error:
                logger.error(
                    f"{task_item} Unexpected exception while handling recoverable failure: {error}",
                    exc_info=True,
                )
                if not is_final_attempt:
                    retry_delay = self.initial_backoff_seconds * (
                        2**attempt
                    ) + random.uniform(0, 1)
                    logger.error(
                        f"{task_item} Retrying in {retry_delay:.2f}s...",
                    )
                    await asyncio.sleep(delay=retry_delay)
                else:
                    logger.error(
                        f"{task_item} failed after all {self.max_retries + 1} attempts due to exception. Giving up."
                    )
                    return False
            return False

    async def __run_loop(self) -> None:
        logger.info("Starting running consumer loop...")
        while not self.should_stop.is_set():
            task_item: TaskItemModel | None = None
            try:
                task_item = await self.task_queue.get_item()
                logger.info(
                    f"Retrieved {task_item}. Queue size: {self.task_queue.check_size()}"
                )
                success = await asyncio.wait_for(
                    self._consume_task_with_retry(task_item=task_item),
                    timeout=self.async_task_timeout_seconds,
                )
                if success:
                    logger.info(f"{task_item} finished")
                else:
                    logger.info(
                        f"{task_item} failed after all {self.max_retries} retries"
                    )
            except asyncio.TimeoutError:
                logger.error(
                    f"{task_item if task_item else 'Unknown'} exceeded "
                    f"hard timeout of {self.async_task_timeout_seconds}s. Giving up."
                )
            except asyncio.CancelledError:
                logger.info("Consumer loop cancelled.")
                break
            except Exception as error:
                logger.error(
                    f"Unexpected error in consumer loop: {error}", exc_info=True
                )
                await asyncio.sleep(1)
            finally:
                if task_item:
                    self.task_queue.task_done()
                    logger.info(
                        f"{task_item if task_item else 'Unknown'} done marked. "
                        + f"Latest Queue size: {self.task_queue.check_size()}"
                    )

    async def start(self) -> None:
        if not self._running_task:
            logger.info(
                "Starting TaskQueueConsumer background task. "
                + f"Max retries: {self.max_retries}, "
                + f"Timeout: {self.async_task_timeout_seconds}"
            )
            self.should_stop.clear()
            self._running_task = asyncio.create_task(self.__run_loop())
            logger.info("TaskQueueConsumer started.")

    async def stop(self) -> None:
        if self._running_task:
            logger.info("Stopping TaskQueueConsumer...")
            self.should_stop.set()
            self._running_task.cancel()
            try:
                await self._running_task
            except asyncio.CancelledError:
                pass
            self._running_task = None
            logger.info("TaskQueueConsumer stopped.")
