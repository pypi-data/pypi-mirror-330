import os
import json
from argparse import ArgumentParser

from inopaicli.concepts.group.api import get_group

DESCRIPTION = "Download group from id and print it"
EXAMPLES = [
    "inopaicli group_get -g 1",
]


def write_json(base_folder, filename, data, force=True):
    fn = os.path.join(base_folder, filename)
    if os.path.exists(fn) and not force:
        raise ValueError("Already exists", fn)
    with open(fn, "wb") as fp:
        fp.write(json.dumps(data, indent=2, ensure_ascii=False).encode())


def init(parser: ArgumentParser):
    parser.add_argument(
        "-g",
        "--group",
        type=int,
        help="Group ID",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--force",
        help="Override data in folder",
        required=False,
        default=False,
        action="store_true",
    )


def main(
    url: str,
    session_id: str,
    group: int,
    force,
    **kwargs,
):
    data = get_group(url, group, session_id)
    print(json.dumps(data, indent=2))

    output_folder = f'group__{data["group"]["name"]}__{data["group"]["id"]}'

    if os.path.exists(output_folder):
        if not force:
            raise ValueError(f"Folder exists {output_folder}")
    else:
        os.makedirs(output_folder)

    write_json(
        output_folder,
        "menu_config.json",
        data["group"]["menu_config"],
    )
    del data["group"]["menu_config"]
    write_json(
        output_folder,
        "app_configs.json",
        data["group"]["app_configs"],
    )
    del data["group"]["app_configs"]
    write_json(
        output_folder,
        "dashboards.json",
        data["group"]["dashboards"],
    )
    del data["group"]["dashboards"]
    del data["group"]["_permissions"]

    write_json(
        output_folder,
        "group_config.json",
        data["group"],
    )
    # webio gna branding
    # roles
    # visualisations
    # gna
    # gna access
    # gna access remote group
    # gna public access
    # dashboard gna?
    # branding
    # background jobs
    # boards
    # conference
    return data
