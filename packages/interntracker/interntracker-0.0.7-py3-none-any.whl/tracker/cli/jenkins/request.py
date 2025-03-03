import os

import jenkins

jenkins_url = os.getenv("JENKINS_URL")
jenkins_user = os.getenv("JENKINS_USER")
jenkins_password = os.getenv("JENKINS_PASSWORD")
try:
    jenkins_timeout = int(os.getenv("JENKINS_TIMEOUT", "600"))
    server = jenkins.Jenkins(jenkins_url, username=jenkins_user, password=jenkins_password, timeout=jenkins_timeout)
except Exception:
    jenkins_timeout = 600
    server = None


def opencompass_evaluate(**kwargs):
    job_name = "opencompass_eval/compass"

    default_params = {
        "feishu_token": "https://open.feishu.cn/open-apis/bot/v2/hook/6abc5a5c-3b4a-495c-9199-1b7253bfade7d",
        "cluster": "aliyun",
        "model_abbr": "volc_official_Ampere2_8_7b_0_0_8_256000_FT_s1_internlm2_5_baseline_2400",
        "model_path": (
            "/cpfs01/shared/public/xingshuhao.dispatch/ckpts/"
            "volc_official_Ampere2_8_7b_0_0_8_256000_FT_s1_internlm2_5_baseline/2400/"
        ),
        "gpu_num": "1",
        "corebench_version": "corebench_v1_7",
        "backend_type": "interntrain",
        "code_path": "/cpfs01/shared/public/xingshuhao.dispatch/InternTrain_20240509",
        "eval_type": "chat",
        "eval_cluster": "llmeval",
        "interntrain_type": "INTERNLM2",
    }

    default_params.update(kwargs)

    return server.build_job(job_name, default_params)
