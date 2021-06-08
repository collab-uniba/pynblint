import os
from pathlib import Path

# TODO: test both the default and the environment variable
temp_dir_env_key = "PYNBLINT_TEMP_DIR_PATH"
default_dir_path = "./pynblint_temp"

if os.environ.get(temp_dir_env_key) is None:
    if not os.path.exists(default_dir_path):
        os.mkdir(default_dir_path)
        print(f"Created temp directory at '{default_dir_path}'")
temp_data_dir_path = Path(os.environ.get(temp_dir_env_key, default_dir_path)).expanduser()

if not os.path.exists(temp_data_dir_path):
    raise ValueError("The temp directory specified by the environment variable "
                     f"'{temp_dir_env_key}' does not exist.")

