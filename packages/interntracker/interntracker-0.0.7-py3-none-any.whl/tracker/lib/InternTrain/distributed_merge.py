import os
import re

import numpy as np

from .load_train_state import load_state_file


def get_ckpt_rank(parallel_string, file_name):
    pattern = re.compile(r"([a-zA-Z]+)(\d+)")

    match = pattern.match(parallel_string)
    assert match, f"Invalid InternTrain ckpt file name: {file_name}"
    letters = match.group(1)
    number = int(match.group(2))
    return letters, number


def split_weight(file_name):
    rank_dict = {}
    fn = os.path.basename(file_name)
    if fn.startswith("model_tp") and fn.endswith(".pt"):
        segements = os.path.splitext(fn)[0].split("_")
        for segment in segements:
            mode, rank = get_ckpt_rank(segment, fn)
            rank_dict[mode] = rank
    return rank_dict


def get_parallel_size_from_file(fns, suffix="model_tp"):
    dims = [0, 0, 0, 0]
    fn_dict = {}
    for fn in fns:
        if fn.startswith(suffix) and fn.endswith(".pt"):
            rank_dict: dict = split_weight(fn)
            if rank_dict:
                fn_dict[fn] = [
                    rank_dict.get("pp", 0),
                    rank_dict.get("wp", 0),
                    rank_dict.get("tp", 0),
                    rank_dict.get("zo", 0),
                ]
                dims[0] = max(dims[0], fn_dict[fn][0])
                dims[1] = max(dims[1], fn_dict[fn][1])
                dims[2] = max(dims[2], fn_dict[fn][2])
                dims[3] = max(dims[3], fn_dict[fn][3])

    matrix = np.empty([x + 1 for x in dims], dtype=str)

    for fn, index in fn_dict.items():
        matrix[index] = fn

    return matrix.tolist()


def load_pp_tp_internlm_ckpt(folder, fns, old_tp, old_pp):
    pipeline_states = [[None for _ in range(old_tp)] for _ in range(old_pp)]
    for fn in fns:
        _, tp, pp = os.path.splitext(fn)[0].split("_")
        tp_rank = int(tp[2:])
        pp_rank = int(pp[2:])
        assert tp_rank < old_tp, f"tp_rank {tp_rank} out of range {old_tp}."
        assert pp_rank < old_pp, f"pp_rank {pp_rank} out of range {old_pp}."
        assert (
            pipeline_states[pp_rank][tp_rank] is None
        ), f"more than one ckpt for tp_rank {tp_rank}, pp_rank {pp_rank}."
        pipeline_states[pp_rank][tp_rank] = load_state_file(os.path.join(folder, fn), map_location="cpu")
    assert all(all(states is not None for states in tensor_states) for tensor_states in pipeline_states)
    return pipeline_states
