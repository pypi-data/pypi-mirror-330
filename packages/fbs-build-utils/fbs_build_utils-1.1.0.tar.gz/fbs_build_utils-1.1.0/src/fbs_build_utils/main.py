import json
import os
import re

import git


def get_default_settings():
    base_path = "src/build/settings/base.default.json"
    with open(base_path, "r") as f:
        return json.load(f)


def get_target_dir():
    current_dir = os.getcwd()
    return os.path.join(current_dir, "target")


def get_settings():
    base_path = "src/build/settings/base.json"
    with open(base_path, "r") as f:
        return json.load(f)


def get_full_version():
    repo = git.Repo(search_parent_directories=True)
    return repo.git.describe("--tags", always=True, dirty="-dirty")


def get_version():
    matches = re.search(r"v(\d+\.\d+\.\d+)", get_full_version())
    if matches is not None:
        return matches.group(1)
    else:
        return "0.0.0"


def update_version():
    print("Generating setting file")
    dest_path = "src/build/settings/base.json"

    # Update the version number in the settings file
    data = get_default_settings()
    data["version"] = get_version()
    data["full_version"] = get_full_version()

    with open(dest_path, "w") as f:
        json.dump(data, f, indent=4)
