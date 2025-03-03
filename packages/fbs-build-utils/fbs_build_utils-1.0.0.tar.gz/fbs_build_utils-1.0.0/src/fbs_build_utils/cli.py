import os

import click

from fbs_build_utils.main import get_settings, get_target_dir, update_version
from fbs_build_utils.os_cmd import execute_command
from fbs_build_utils.rename_installer import name_installer
from fbs_build_utils.generate_icons import generate_icons
from qt_build_utils.convert_ui import convert_ui_glob
import platform
import distro

ICON_PATH = "src/main/icons/icon.png"


@click.group()
def cli():
    pass


def generate_files():
    update_version()
    generate_icons(ICON_PATH)
    settings = get_settings()
    for ui_dir in settings["ui_paths"]:
        convert_ui_glob(ui_dir, inplace=True)


@cli.command()
def generate():
    generate_files()


@cli.command()
@click.option("--debug", is_flag=True)
@click.option("--sign", is_flag=True)
@click.option("--only-keep-renamed", is_flag=True)
def build(debug: bool, only_keep_renamed: bool, sign: bool):
    # Run the generate command
    generate_files()

    # Create EXE
    if debug:
        execute_command("fbs freeze --debug")
    else:
        execute_command("fbs freeze")

    if sign:
        execute_command("fbs sign")

    execute_command("fbs installer")

    if sign:
        execute_command("fbs sign_installer")

    info = get_settings()

    name = f"{info['app_name']}_{info['version']}"

    name_with_underscore = name.replace(" ", "_")

    if platform.system() == "Linux":
        distro_name = distro.name(pretty=True).lower().replace(" ", "_")

    elif platform.system() == "Windows":
        distro_name = "win64"

    elif platform.system() == "Darwin":
        # Check if arm or intel
        if platform.processor() == "arm":
            distro_name = "mac_arm"
        else:
            distro_name = "mac_x86"

    else:
        raise NotImplementedError(f"{platform.system()} is not supported")

    name_installer(f"{name_with_underscore}_{distro_name}", remove_source=only_keep_renamed)


@cli.command()
def run():
    # Run the app
    info = get_settings()
    portable_path = os.path.join(get_target_dir(), info["app_name"])
    execute_command(f"{portable_path}/{info['app_name']}.exe")


@cli.command()
def run_python():
    execute_command("fbs run")


@cli.command()
def run_installer():
    # Run the installer
    execute_command(os.path.join(get_target_dir(), "latest.exe"))


if __name__ == "__main__":
    cli()
