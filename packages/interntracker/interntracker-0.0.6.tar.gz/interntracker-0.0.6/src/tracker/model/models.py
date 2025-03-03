import json
from datetime import datetime
from enum import Enum
from typing import List, get_type_hints


def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False


def load_json_string(string):
    try:
        return json.loads(string)
    except (TypeError, OverflowError):
        return None


def load_type_string(dtype, string):
    try:
        if dtype in [int, float, bool]:
            return dtype(string)
        else:
            return None
    except (TypeError, OverflowError):
        return None


def get_enum_by_value(enum_class, value):
    for member in enum_class:
        if member.value == value:
            return member
    return None


def is_typing(dtype):
    try:
        return dtype.__module__ == "typing"
    except AttributeError:
        return False


def get_typing(dtype):
    try:
        origin = dtype.__origin__
    except AttributeError:
        origin = dtype
    try:
        args = dtype.__args__
    except AttributeError:
        args = tuple()
    return origin, args


def object_hook(dtype, json_object):
    if dtype == str:
        return json_object
    elif json_object in ["null", "None"]:
        return None
    if issubclass(dtype, Enum):
        return get_enum_by_value(dtype, json_object)
    elif issubclass(dtype, datetime):
        return datetime.strptime(json_object, "%Y-%m-%dT%H:%M:%S.%fZ")
    elif issubclass(dtype, Serializable):
        obj = dtype()
        return obj.object_hook(json_object)
    return load_type_string(dtype, json_object)


class Serializable:
    """
    JSON Serialization
    """

    id: str = None
    key: str = None
    revision: str = None

    def __new__(cls):
        cls.annotations = get_type_hints(cls)
        return super(Serializable, cls).__new__(cls)

    def __init__(self):
        super().__init__()

    @classmethod
    def serialize(cls, data):
        if isinstance(data, dict):
            return {key: cls.serialize(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [cls.serialize(item) for item in data]
        elif isinstance(data, tuple):
            return tuple(cls.serialize(item) for item in data)
        elif isinstance(data, set):
            return {cls.serialize(item) for item in data}
        elif isinstance(data, datetime):
            return datetime.strftime(data, "%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        elif isinstance(data, Serializable):
            return data.state_dict()
        elif isinstance(data, Enum):
            return data.value
        elif is_json_serializable(data):
            return data
        else:
            return repr(data)

    def state_dict(self):
        result = {}
        var = vars(self).copy()
        var.update({"id": self.id})
        for attr in var:
            value = self.serialize(getattr(self, attr))
            if value is not None:
                result[attr] = value
        return result

    def load_state_dict(self, states: dict):
        for key, value in states.items():
            if hasattr(self, key) and key in self.annotations:
                if is_typing(self.annotations[key]):
                    # pylint: disable=W0612
                    dtype, dargs = get_typing(self.annotations[key])
                    assert isinstance(value, dtype)
                    setattr(self, key, value)
                elif isinstance(value, self.annotations[key]):
                    setattr(self, key, value)
                elif isinstance(value, str):
                    setattr(self, key, object_hook(self.annotations[key], value))
                elif value is not None:
                    raise Exception(f"key {key} {value} is not {self.annotations[key]} type")
            else:
                setattr(self, key, value)

    def __setattr__(self, key, value):
        if key in self.annotations and isinstance(value, str):
            super().__setattr__(key, object_hook(self.annotations[key], value))
        else:
            super().__setattr__(key, value)

    def object_hook(self, json_object):
        for key, value in json_object:
            if hasattr(self, key):
                setattr(self, key, value)
        return self


class Checkpoint(Serializable):
    """
    Checkpoint
    """

    config: str = None
    md5: str = None
    path: str = None
    step: int = None
    saveTime: datetime = None
    tokens: int = None
    isDelivery: bool = False
    isRewardModel: bool = False
    isSnapshot: bool = False


class ProcType(Enum):
    RUNNING = "running"
    FAILED = "failed"
    FINISHED = "finished"


class ClusterType(Enum):
    ALI = "Ali"
    ALI_H_A = "Ali-H-A"
    ALI_H_B = "Ali-H-B"
    _910B = "910B"
    A800 = "A800"
    VOLC = "volc"


class TrainConfig(Serializable):
    """
    Training Config
    """

    task: str = None
    loadCkpt: str = None
    configContent: str = None
    dataConfig: dict = None
    modelConfig: dict = None
    optimizerConfig: dict = None
    parallelConfig: dict = None
    startStep: int = 0
    startToken: int = 0
    ckpts: List[Checkpoint] = None

    # TrainProc
    cluster: ClusterType = None
    envVar: dict = None
    gpuNum: int = None
    startTime: datetime = datetime.now()
    endtime: datetime = None
    state: ProcType = ProcType.RUNNING
    currentStep: int = 0
    totalStep: int = None

    # TrainLog
    configPath: str = None
    logFolder: str = None
    tbFolder: str = None

    ckpts: List[Checkpoint] = []

    def __init__(self):
        super().__init__()

    def object_hook(self, json_object):
        for key, value in json_object:
            if key == "ckpts":
                assert isinstance(value, list), "ckpts should be a list"
                setattr(self, key, [Checkpoint().object_hook(ckpt) for ckpt in value])
            elif hasattr(self, key):
                setattr(self, key, value)
        return self


class TaskType(Enum):
    PRETRAIN = "pretrain"
    RLHF_PPO = "rlhf_ppo"
    RLHF_RM = "rlhf_rm"
    SFT = "sft"


class TrainTask(Serializable):
    """
    Train Task
    """

    loadCkpt: str = None
    name: str = None
    type: TaskType = TaskType.PRETRAIN
    desc: str = None
    configs: List[TrainConfig] = None

    def __init__(self):
        super().__init__()

    def object_hook(self, json_object):
        for key, value in json_object:
            if key == "configs":
                assert isinstance(value, list), "configs should be a list"
                setattr(self, key, [TrainConfig().object_hook(conf) for conf in value])
            elif hasattr(self, key):
                setattr(self, key, value)
        return self


class TrainProc(Serializable):
    """
    Training Process
    """

    # TrainTask
    name: str = None
    type: TaskType = None
    desc: str = None

    # TrainConfig
    configContent: str = None
    dataConfig: dict = None
    modelConfig: dict = None
    optimizerConfig: dict = None
    parallelConfig: dict = None
    startStep: int = 0
    startToken: int = 0

    # TrainProc
    cluster: ClusterType = None
    envVar: dict = None
    gpuNum: int = None
    startTime: datetime = datetime.now()
    endtime: datetime = None
    state: ProcType = ProcType.RUNNING
    currentStep: int = 0
    totalStep: int = None

    # TrainLog
    configPath: str = None
    logFolder: str = None
    tbFolder: str = None

    ckpts: List[Checkpoint] = []

    def __init__(self):
        super().__init__()

    def save_local_json(self, ckptMd5: str = None):
        task = TrainTask()
        task.load_state_dict(
            {
                "name": self.name,
                "type": self.type,
                "desc": self.desc,
            }
        )
        config = TrainConfig()
        if self.id is not None:
            config.id = self.id
        config.load_state_dict(
            {
                "configContent": self.configContent,
                "dataConfig": self.dataConfig,
                "modelConfig": self.modelConfig,
                "optimizerConfig": self.optimizerConfig,
                "parallelConfig": self.parallelConfig,
                "startStep": self.startStep,
                "startToken": self.startToken,
                "configPath": self.configPath,
                "logFolder": self.logFolder,
                "tbFolder": self.tbFolder,
                "cluster": self.cluster,
                "envVar": self.envVar,
                "gpuNum": self.gpuNum,
                "startTime": self.startTime,
                "endtime": self.endtime,
                "state": self.state,
                "currentStep": self.currentStep,
                "totalStep": self.totalStep,
                "ckpts": self.ckpts,
            }
        )
        if self.name is None:
            task.loadCkpt = ckptMd5
        else:
            config.loadCkpt = ckptMd5
        task.configs = [config]
        return task

    def object_hook(self, json_object):
        for key, value in json_object:
            if hasattr(self, key):
                if key == "configs":
                    assert isinstance(value, list), "configs should be a list"
                    for conf in value:
                        for k, v in conf.items():
                            if k == "ckpts":
                                setattr(self, k, [Checkpoint().object_hook(ckpt) for ckpt in v])
                            else:
                                setattr(self, k, v)
                elif hasattr(self, key):
                    setattr(self, key, value)
        return self


class EvalScore(Serializable):
    """
    Eval Score
    """

    datasetMd5: str = None
    datasetName: str = None
    metric: str = None
    mode: str = None
    score: float = None
    subsetName: str = None


class EvalResult(Serializable):
    """
    Eval Result
    """

    finishTime: datetime = None
    isValid: bool = True
    logFolder: str = None
    scores: List[EvalScore] = None

    def __init__(self):
        super().__init__()

    def object_hook(self, json_object):
        for key, value in json_object:
            if hasattr(self, key):
                if key == "scores":
                    assert isinstance(value, list), "configs should be a list"
                    scores_list = []
                    for score in value:
                        scores_list.append(EvalScore().object_hook(score))
                    setattr(self, key, scores_list)
                elif hasattr(self, key):
                    setattr(self, key, value)
        return self
