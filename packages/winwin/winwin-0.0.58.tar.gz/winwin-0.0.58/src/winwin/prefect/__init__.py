import prefect
from prefect.context import FlowRunContext

from .aliyun import AliyunOss, AliyunOssCredentials
from .ssh import SshCredentials


def change_result_store_key():
    flow_run_ctx = FlowRunContext.get()
    flow_run = flow_run_ctx.flow_run

    def storage_key_fn():
        return (
            f"{flow_run_ctx.start_time:%Y%m%d}/{flow_run_ctx.flow.name}/{flow_run.name}"
        )

    flow_run_ctx.result_store.storage_key_fn = storage_key_fn


def task(*args, **kwargs):
    # 定义默认参数
    default_kwargs = {
        "result_serializer": "json",
        "result_storage_key": (
            "{flow_run.scheduled_start_time:%Y%m%d}/"
            "{flow_run.flow_name}/{task_run.name}"
        ),
    }
    # 使用用户传入的参数覆盖默认参数
    final_kwargs = {**default_kwargs, **kwargs}

    return prefect.task(*args, **final_kwargs)


def flow(*args, **kwargs):
    # 定义默认参数
    default_kwargs = {
        "log_prints": True,
        "persist_result": True,
        "result_serializer": "json",
        "result_storage": "aliyun-oss/aliyun-oss-dev",
    }
    # 使用用户传入的参数覆盖默认参数
    final_kwargs = {**default_kwargs, **kwargs}

    return prefect.flow(*args, **final_kwargs)


__all__ = ["AliyunOss", "AliyunOssCredentials", "SshCredentials", "flow", "task"]
