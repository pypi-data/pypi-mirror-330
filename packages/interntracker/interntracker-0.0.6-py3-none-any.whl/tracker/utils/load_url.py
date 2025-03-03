import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv


def load_environment_variables():
    necessary_vars = ["INTERNTRACK_API_URL"]
    all_vars_present = {var: os.getenv(var, None) for var in necessary_vars}

    if any(v is None for v in all_vars_present.values()):
        default_env = os.path.join(Path(__file__).parent.parent.parent.parent.as_posix(), ".env")
        user_env_path = find_dotenv(default_env)
        if user_env_path:
            load_dotenv(user_env_path, override=False)

        library_env_path = find_dotenv()
        if library_env_path:
            load_dotenv(library_env_path)
            for var, val in all_vars_present.items():
                if val:
                    os.environ[var] = val
