import os
from argparse import ArgumentParser
from inopaicli.concepts.app_export.api import export_update
from inopaicli.core.api import get_id_or_identifier
from inopaicli.core.arguments import add_allowed_urls_argument, add_use_action_id, add_use_action_ids_argument
from inopaicli.core.config import parse_allowed_urls
from inopaicli.core.file import get_all_files, read_file, read_json_file
from inopaicli.core.util import check_if_its_directory

DESCRIPTION = "Update export in app based on a folder containing data (.json) and template files (.docx)"
EXAMPLES = [
    "inopaicli exports_update -a 1 -f './directory' --allowedurls http://localhost:9000",
    "inopaicli exports_update -a 1 -f './directory' --allowedurls http://localhost:9000 --useactionids",
]


def init(parser: ArgumentParser):
    add_use_action_id(parser)
    add_use_action_ids_argument(parser)
    add_allowed_urls_argument(parser)


def main(
    url: str,
    session_id: str,
    app: int,
    folder: str,
    allowedurls: str,
    useactionids=False,
    **kwargs,
):
    dir_path = os.path.realpath(folder)

    assert url in parse_allowed_urls(allowedurls)

    check_if_its_directory(dir_path)

    for file_name in get_all_files(dir_path):
        if ".docx" in file_name:
            print("Ignoring template")
            continue

        path = os.path.realpath(os.path.join(dir_path, file_name))
        data = read_json_file(path, quiet=True)

        export_app = data.get("app")
        if app and app != export_app:
            continue

        id_or_identifier = get_id_or_identifier(data, useactionids)
        template_docx_path = os.path.realpath(
            os.path.join(
                dir_path,
                f"app__{export_app}__export__{id_or_identifier}__TEMPLATE.docx"
            )
        )
        template_file = read_file(template_docx_path, quiet=True)

        export_update(
            url=url,
            session_id=session_id,
            data=data,
            template_file=template_file,
        )
