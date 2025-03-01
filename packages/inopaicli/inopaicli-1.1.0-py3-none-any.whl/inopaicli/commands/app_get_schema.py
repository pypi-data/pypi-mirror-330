from argparse import ArgumentParser
from inopaicli.concepts.app.api import get_app
from inopaicli.core.file import write_json

DESCRIPTION = "Returns app schema for specified application from data in folder"
EXAMPLES = [
    "inopaicli app_get_schema -a 1 -o './directory'",
]


def init(parser: ArgumentParser):
    parser.add_argument("-a", "--app", type=int, help="Application ID", required=True)
    parser.add_argument(
        "-o",
        "--outputdirectory",
        help="Specify the directory where to generate the json file with app schema",
        required=True,
    )


def main(
    url: str,
    session_id: str,
    app: int,
    outputdirectory=".",
    **kwargs,
):
    data = get_app(url, app, session_id)

    schema = data["application"].get("schema", None)
    file_name = f"{outputdirectory}/app__{app}__schema.json"
    write_json(filename=file_name, data=schema)

    webform_schema = data["application"].get("webform_schema", None)

    if webform_schema:
        file_name = f"{outputdirectory}/app__{app}__webform_schema.json"
        write_json(filename=file_name, data=webform_schema)

    return data
