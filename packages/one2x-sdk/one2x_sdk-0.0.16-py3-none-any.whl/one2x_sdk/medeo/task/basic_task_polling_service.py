import asyncio
from typing import Callable, Dict, List, Optional, Awaitable, Protocol


class LoggerProtocol(Protocol):
    """定义日志接口协议"""

    def info(self, message: str):
        ...

    def error(self, message: str):
        ...


class BasicTaskPollingService:
    def __init__(
        self,
        logger: LoggerProtocol,
        job_processor: Callable[[Dict], Awaitable[None]],
        max_concurrent_tasks: int = 20,
        poll_gap: float = 5.0,
    ):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self.running_tasks = set()
        self.job_queue = asyncio.Queue()
        self.logger = logger
        self.poll_gap = poll_gap
        self.job_processor = job_processor
        self._stop_event = asyncio.Event()

        self.logger.info(
            f"Polling service initialized with max {max_concurrent_tasks} "
            f"concurrent tasks and poll gap {poll_gap}s"
        )

    async def worker(self):
        """从队列中获取任务并处理"""
        while not self._stop_event.is_set():
            try:
                job = await self.job_queue.get()
                task = asyncio.create_task(self._safe_process_job(job))
                self.running_tasks.add(task)

                task.add_done_callback(self._handle_task_done)
                self.job_queue.task_done()
            except asyncio.CancelledError:
                break

    def _handle_task_done(self, task: asyncio.Task):
        """处理任务完成的回调"""
        try:
            task.result()
        except Exception as e:
            self.logger.error(f"Unhandled exception in task: {str(e)}")
        finally:
            self.running_tasks.discard(task)

    async def _safe_process_job(self, job: Dict):
        """安全地调用外部提供的任务处理函数"""
        async with self.semaphore:
            try:
                self.logger.info(f"Processing job {job.get('id', 'unknown')}...")
                await self.job_processor(job)
            except Exception as e:
                self.logger.error(
                    f"Error processing job {job.get('id', 'unknown')}: {str(e)}"
                )
            finally:
                self.running_tasks.discard(asyncio.current_task())

    async def poll_and_process(
        self,
        fetch_jobs: Callable[[Optional[Dict]], Awaitable[List[Dict]]],
        fetch_params: Optional[Dict] = None,
    ):
        """轮询任务并处理"""
        workers = [
            asyncio.create_task(self.worker()) for _ in range(self.max_concurrent_tasks)
        ]

        interval = self.poll_gap
        try:
            while not self._stop_event.is_set():
                try:
                    # 调用异步 fetch_jobs，并传入参数 fetch_params
                    jobs = await fetch_jobs(fetch_params)
                    if jobs:
                        for job in jobs:
                            await self.job_queue.put(job)
                        interval = self.poll_gap  # 重置间隔为默认值
                    else:
                        interval = min(interval + 1, 10)  # 动态调整轮询间隔

                    # 清理已完成的任务
                    self.running_tasks = {
                        task for task in self.running_tasks if not task.done()
                    }

                except Exception as e:
                    self.logger.error(f"Error in poll_and_process: {str(e)}")

                await asyncio.sleep(interval)

        except asyncio.CancelledError:
            self.logger.info("Polling service is shutting down...")
            await self.job_queue.join()
            for task in self.running_tasks:
                task.cancel()
            await asyncio.gather(*self.running_tasks, return_exceptions=True)
            raise

        finally:
            for worker in workers:
                worker.cancel()
            await asyncio.gather(*workers, return_exceptions=True)

    async def start_polling(
        self,
        fetch_jobs: Callable[[Optional[Dict]], Awaitable[List[Dict]]],
        fetch_params: Optional[Dict] = None,
    ):
        """开始轮询任务"""
        self.logger.info("Polling service started.")
        await self.poll_and_process(fetch_jobs, fetch_params)

    async def stop_polling(self):
        """停止轮询任务"""
        self.logger.info("Stopping polling service...")
        self._stop_event.set()
