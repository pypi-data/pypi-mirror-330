import os
from argparse import ArgumentParser
from inopaicli.concepts.app_export.api import export_template_download, get_exports
from inopaicli.core.api import get_id_or_identifier
from inopaicli.core.arguments import add_use_action_id, add_use_action_ids_argument
from inopaicli.core.file import write_json
from inopaicli.core.util import check_if_its_directory

DESCRIPTION = "Downloads export in app based on a folder containing data"
EXAMPLES = [
    "inopaicli exports_download_all -a 1 -o './directory'",
    "inopaicli exports_download_all -a 1 -o './directory' --useactionids",
]


def init(parser: ArgumentParser):
    add_use_action_id(parser)
    parser.add_argument(
        "-o",
        "--outputdirectory",
        help="Specify the directory where to generate the json file with exported files",
        default="exports",
    )
    add_use_action_ids_argument(parser)


def main(
    url: str,
    session_id: str,
    app: int,
    outputdirectory: str,
    debug=False,
    useactionids=False,
    **kwargs,
):
    dir_path = os.path.realpath(outputdirectory)

    check_if_its_directory(dir_path)

    for export in get_exports(
        url=url,
        session_id=session_id,
        app=app,
        debug=debug,
    ):
        export.pop("_gnas")
        id_or_identifier = get_id_or_identifier(export, useactionids)
        local_filename = file_name = os.path.join(
            dir_path,
            f"app__{export['app']}__export__{id_or_identifier}__TEMPLATE.docx"
        )

        export_template_download(
            url=url,
            session_id=session_id,
            export_id=export["id"],
            local_filename=local_filename,
        )

        if "exportgna_count" not in export or export.get("exportgna_count", None) == 0:
            print("Ignoring unused export")
            continue

        print("exportgna_count ", export["exportgna_count"])
        file_name = f"app__{export['app']}__export__{export['id']}__"
        file_name += f"data__{export['semantic_identifier']}__{export['text']}.json"
        final_file_name = os.path.join(dir_path, file_name)

        print("export", export.get("id", None), "-->", final_file_name)
        write_json(data=export, filename=final_file_name)
