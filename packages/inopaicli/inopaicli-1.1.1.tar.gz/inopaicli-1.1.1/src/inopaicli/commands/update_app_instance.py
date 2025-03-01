import os
import json
from argparse import ArgumentParser

from inopaicli.concepts.app.api import update_app_instance
from inopaicli.core.file import get_all_files, read_json_file
from inopaicli.core.util import check_if_its_directory

DESCRIPTION = "Download instance from folder"
EXAMPLES = [
    "inopaicli update_app_instance -d .",
]


def write_json(base_folder, filename, data, force=True):
    fn = os.path.join(base_folder, filename)
    if os.path.exists(fn) and not force:
        raise ValueError("Already exists", fn)
    with open(fn, "wb") as fp:
        fp.write(json.dumps(data, indent=2, ensure_ascii=False).encode())


def init(parser: ArgumentParser):
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        help="Folder",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--force",
        help="Force",
        required=False,
        default=False,
        action="store_true",
    )


def main(
    url: str,
    session_id: str,
    directory: str,
    force,
    **kwargs,
):

    dir_path = os.path.realpath(directory)

    check_if_its_directory(dir_path)

    data: [str, dict] = {}

    for file_name in get_all_files(dir_path, recursive=True):
        file_path = file_name.split('/')
        if len(file_path) < 2:
            print(f"Ignore: {file_name}")
            continue
        dir_parts = file_path[-2].split("__")
        if len(dir_parts) != 3:
            print(f"Ignore: {file_name}")
            continue

        entity_type = dir_parts[0]
        entity_id = dir_parts[2]

        if entity_type not in data:
            data[entity_type] = {}
        if entity_id not in data[entity_type]:
            data[entity_type][entity_id] = {}

        sub_entity = data[entity_type][entity_id]
        for file_part in file_path[-1].split("__"):
            if "." in file_part:
                sub_entity[file_part.rsplit(".", 1)[0]] = read_json_file(file_name)
            else:
                if file_part not in sub_entity:
                    sub_entity[file_part] = {}
                sub_entity = sub_entity[file_part]

    write_json(".", "data.json", data)

    response = update_app_instance(url, session_id, data)

    print(response)

    return response
