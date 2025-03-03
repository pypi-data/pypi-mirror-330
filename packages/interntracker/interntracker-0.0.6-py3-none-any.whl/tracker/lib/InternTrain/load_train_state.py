import os

import torch


def load_state_file(file_path, **kwargs):
    return torch.load(file_path, **kwargs)


def get_train_state(file_path):
    load_state = load_state_file(os.path.join(file_path, "context.pt"))
    return {
        "token": load_state["num_consumed_tokens"],
        "step": load_state["step_count"],
        "batch": load_state["batch_count"],
        "tensorboard_folder": load_state["tensorboard_folder"],
    }
