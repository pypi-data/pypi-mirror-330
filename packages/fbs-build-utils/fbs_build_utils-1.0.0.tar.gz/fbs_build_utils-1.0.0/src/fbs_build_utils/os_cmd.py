import os
import subprocess


# from icons.icongenerator import generate_icons  # noqa: E402
from qt_build_utils.setup import setup_path, is_path_setup


def execute_command(cmd: str):
    if not is_path_setup():
        setup_path()

    # Execute a command and print to stdout and stderr
    print(f"Executing command: '{cmd}'")

    proc = subprocess.Popen(cmd, shell=True, cwd=os.getcwd())

    # Check for erros
    if proc.wait() != 0:
        raise RuntimeError(f"Command {cmd} failed with error code {proc.returncode}")
