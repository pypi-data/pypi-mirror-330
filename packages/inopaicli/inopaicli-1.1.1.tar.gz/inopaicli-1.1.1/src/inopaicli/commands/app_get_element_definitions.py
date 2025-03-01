import os
from argparse import ArgumentParser
from inopaicli.concepts.app.api import get_app
from inopaicli.core.arguments import add_use_action_id
from inopaicli.core.file import write_json

DESCRIPTION = "Download element definitions and generate json file to an output location"
EXAMPLES = [
    "inopaicli app_get_element_definitions -a 1 -o './directory'",
]


def init(parser: ArgumentParser):
    add_use_action_id(parser)
    parser.add_argument(
        "-o",
        "--outputdirectory",
        help="Specify the directory where to generate the json file with element definiton",
        required=False,
    )


def main(
    url: str,
    session_id: str,
    app: int,
    outputdirectory: str,
    **kwargs,
):
    data = get_app(url, app, session_id)

    element_definitions = data["application"]["schema"].get("element_definitions", None)

    if not os.path.exists(outputdirectory):
        os.makedirs(outputdirectory)

    if element_definitions:
        for definitionname, data in element_definitions.items():
            file_name = f"{outputdirectory}/app__{app}__el__{definitionname}.json"
            write_json(filename=file_name, data=data)

    return data
