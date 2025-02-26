import asyncio
import pytest
from typing import Dict, List, Optional

from one2x_sdk.medeo.task.basic_task_polling_service import BasicTaskPollingService


class TestLogger:
    def __init__(self):
        self.logs = {"info": [], "error": []}

    def info(self, message: str):
        print(f"[INFO]: {message}")
        self.logs["info"].append(message)

    def error(self, message: str):
        print(f"[ERROR]: {message}")
        self.logs["error"].append(message)


# 模拟任务获取函数
async def mock_fetch_single_batch_jobs(params: Optional[Dict] = None) -> List[Dict]:
    """
    模拟从外部服务获取任务。
    - 第一次返回三个任务。
    - 后续返回空列表（模拟没有新任务）。
    """
    await asyncio.sleep(0.1)  # 模拟网络延迟
    if mock_fetch_single_batch_jobs.call_count == 0:
        mock_fetch_single_batch_jobs.call_count += 1
        return [{"id": 1, "value": 1}, {"id": 2, "value": 2}, {"id": 3, "value": 300}]
    else:
        return []


# 初始化调用计数器
mock_fetch_single_batch_jobs.call_count = 0


@pytest.mark.asyncio
async def test_simple_polling_service():
    """
    测试简单的轮询服务。
    """
    result = {"value": 0}

    async def mock_success_job_processor(job: Dict):
        result["value"] += job["value"]
        await asyncio.sleep(0.2)

    logger = TestLogger()
    service = BasicTaskPollingService(
        logger=logger,
        job_processor=mock_success_job_processor,
        max_concurrent_tasks=2,  # 最大并发任务数
        poll_gap=0.1,  # 轮询间隔
    )

    polling_task = asyncio.create_task(
        service.start_polling(fetch_jobs=mock_fetch_single_batch_jobs)
    )

    await asyncio.sleep(2)
    await service.stop_polling()

    await polling_task

    # 验证日志内容
    assert result["value"] == 303
