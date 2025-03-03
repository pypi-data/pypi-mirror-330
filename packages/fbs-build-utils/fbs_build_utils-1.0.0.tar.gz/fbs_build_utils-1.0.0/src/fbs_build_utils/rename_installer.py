from fbs_build_utils.main import get_settings
import os
import shutil
import platform


def name_installer(target_name: str, remove_source=False):
    data = get_settings()

    # Rename the installer
    if platform.system() == "Windows":
        source_file = f"target/{data['app_name']}Setup.exe"
        # dest_file = f"target/{data['app_name']}_{data['version']}_Installer_win64.exe"
        dest_file = f"target/{target_name}.exe"
    elif platform.system() == "Darwin":
        source_file = f"target/{data['app_name']}.dmg"
        dest_file = f"target/{target_name}.dmg"
    elif platform.system() == "Linux":
        source_file = f"target/{data['app_name']}.deb"
        dest_file = f"target/{target_name}.deb"

    else:
        raise NotImplementedError(f"{platform.system()} is not supported")

    # Remove the old installer if it exists
    if os.path.exists(dest_file):
        os.remove(dest_file)

    # Rename the installer
    shutil.copyfile(source_file, dest_file)

    if remove_source:
        os.remove(source_file)


def package_portable(target_name: str):
    data = get_settings()
    source_path = f"target/{data['app_name']}"
    target_path = f"target/{target_name}"
    # Create zip
    shutil.make_archive(target_path, "zip", source_path)
