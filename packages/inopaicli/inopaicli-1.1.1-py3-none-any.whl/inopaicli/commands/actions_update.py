import os
from argparse import ArgumentParser
from inopaicli.concepts.app_action.functions import update_one_action
from inopaicli.core.arguments import add_allowed_urls_argument, add_use_action_id, add_use_action_ids_argument
from inopaicli.core.config import parse_allowed_urls
from inopaicli.core.file import get_all_files
from inopaicli.core.util import check_if_its_directory

DESCRIPTION = "Update all actions for specified application from data in folder"
EXAMPLES = [
    "inopaicli actions_update -a 1 -f './actions' --allowedurls http://localhost:9000",
    "inopaicli actions_update -a 1 -f './actions' --allowedurls http://localhost:9000 --useactionids",
]


def init(parser: ArgumentParser):
    add_use_action_id(parser)
    parser.add_argument(
        "-f",
        "--folder",
        help="Folder with action files",
        required=True,
    )
    add_use_action_ids_argument(parser)
    add_allowed_urls_argument(parser)


def main(
    url: str,
    session_id: str,
    app: int,
    folder: str,
    allowedurls: str,
    useactionids=False,
    **kwargs
):
    assert url in parse_allowed_urls(allowedurls)
    dir_path = os.path.realpath(folder)

    check_if_its_directory(dir_path)

    for file_name in get_all_files(dir_path):
        if file_name == "app_schema_cps.json":
            print("Ignoring app form schema")
            continue

        fullpath = os.path.realpath(os.path.join(dir_path, file_name))

        try:
            update_one_action(
                url=url,
                session_id=session_id,
                app=app,
                fullpath=fullpath,
                useactionids=useactionids
            )
        except Exception as exc:
            print(exc)
            raise
