import prefect
from prefect.utilities.dispatch import register_type

from .aliyun import AliyunOss, AliyunOssCredentials

task = prefect.task(
    result_serializer="json",
    result_storage_key="{flow_run.scheduled_start_time:%Y%m%d}/{task_run.name}",
)

flow = prefect.flow(
    log_prints=True,
    persist_result=True,
    result_serializer="json",
    result_storage="aliyun-oss/aliyun-oss-dev",
)

register_type(AliyunOss)

__all__ = ["AliyunOss", "AliyunOssCredentials", "flow", "task"]