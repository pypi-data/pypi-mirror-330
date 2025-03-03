from functools import partial

from .cli import (
    opencompass_evaluate,
    save_ckpt_online_mutation,
    save_eval_result_mutation,
    save_proc_online_mutation,
    save_roadmap_offline_mutation,
)
from .model import (
    Checkpoint,
    ClusterType,
    ProcType,
    Serializable,
    TrainConfig,
    TrainProc,
    TrainTask,
)
from .utils import get_process_md5, load_environment_variables

load_environment_variables()
save_proc_online_mutation = partial(save_proc_online_mutation, procMd5=get_process_md5())
save_ckpt_online_mutation = partial(save_ckpt_online_mutation, procMd5=get_process_md5())

__all__ = [
    "load_environment_variables",
    "get_process_md5",
    "save_roadmap_offline_mutation",
    "save_proc_online_mutation",
    "save_ckpt_online_mutation",
    "save_eval_result_mutation",
    "opencompass_evaluate",
    "Serializable",
    "TrainTask",
    "TrainConfig",
    "TrainProc",
    "Checkpoint",
    "ProcType",
    "ClusterType",
]
