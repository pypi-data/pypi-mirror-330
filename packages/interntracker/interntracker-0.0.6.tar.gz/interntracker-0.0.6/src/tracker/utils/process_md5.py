import uuid

import psutil


def get_process_md5():
    process = psutil.Process()

    start_timestamp = process.create_time()

    md5 = to_upper_hex(uuid.getnode()) + to_upper_hex(start_timestamp) + to_upper_hex(process.pid)

    # 0x [MAC 地址] [process start timestamp] [process_id]
    return md5.zfill(36)


def to_upper_hex(number):
    return hex(int(number)).replace("0x", "").upper()
