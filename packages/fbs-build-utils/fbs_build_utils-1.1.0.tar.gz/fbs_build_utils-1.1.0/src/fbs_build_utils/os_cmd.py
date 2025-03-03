import os
import subprocess


# from icons.icongenerator import generate_icons  # noqa: E402
from qt_build_utils.path_manager import manager


def execute_command(cmd: str):
    if not manager.is_path_setup():
        manager.is_path_setup()

    # Execute a command and print to stdout and stderr
    print(f"Executing command: '{cmd}'")

    proc = subprocess.Popen(cmd, shell=True, cwd=os.getcwd())

    # Check for erros
    if proc.wait() != 0:
        raise RuntimeError(f"Command {cmd} failed with error code {proc.returncode}")
