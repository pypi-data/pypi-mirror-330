import hashlib
import os
import secrets
from datetime import datetime
from typing import List

from ..lib.InternTrain import get_train_state


def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_folder_hashes(folder_path):
    file_hashes = {}
    for file in os.listdir(folder_path):
        if file.startswith("model_tp") and file.endswith(".pt"):
            file_path = os.path.join(folder_path, file)
            file_hashes[file_path] = get_file_hash(file_path)
    return file_hashes


def merkle_tree(hashes: List[str]):
    if len(hashes) == 1:
        return hashes[0]

    if len(hashes) % 2 != 0:
        hashes.append(hashes[-1])

    new_level = []
    for i in range(0, len(hashes), 2):
        combined_hash = hashlib.sha256(hashes[i].encode("utf-8") + hashes[i + 1].encode("utf-8")).hexdigest()
        new_level.append(combined_hash)

    return merkle_tree(new_level)


def random_hash():
    random_data = secrets.token_hex()
    hash_object = hashlib.sha256()
    hash_object.update(random_data.encode())
    return hash_object.hexdigest()


def get_internlm_info(internlm_ckpt_path):
    results = []
    hasSnapshot = False
    for ckpt in list(set(os.listdir(internlm_ckpt_path)) - set(["pings"])):
        if ckpt == "snapshot":
            hasSnapshot = True
            continue
        try:
            step = int(ckpt)
            file_path = os.path.join(internlm_ckpt_path, ckpt)
            hashes = get_folder_hashes(file_path)
            for file_path, hash_value in hashes.items():
                print(f"File: {file_path}, SHA-256 Hash: {hash_value}")

            dt_object = datetime.fromtimestamp(os.path.getmtime(file_path))
            formatted_time = dt_object.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

            train_state = get_train_state(file_path)
            assert step == train_state["step"], f"path name {file_path} not match saved step {train_state['step']}"

            result = {
                "md5": merkle_tree(list(hashes.values())),
                "step": train_state["step"],
                "saveTime": formatted_time,
                "path": file_path,
                "tokens": train_state["token"],
                "isSnapshot": False,
                "isDelivery": False,
                "isRewardModel": False,
            }
            results.append(result)

            print("merkle tree:", result["md5"])
        except ValueError:
            continue
    if hasSnapshot:

        for snapshot in os.listdir(os.path.join(internlm_ckpt_path, "snapshot")):
            file_path = os.path.join(internlm_ckpt_path, "snapshot", snapshot)

    return results


if __name__ == "__main__":
    # folder_path = sys.argv[1]
    # print(get_internlm_info(folder_path))
    print(random_hash())
