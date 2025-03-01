from argparse import ArgumentParser
from inopaicli.concepts.app.api import get_app
from inopaicli.core.arguments import add_use_action_id
from inopaicli.core.file import write_json

DESCRIPTION = "Download workflow information from application id and generate json file to an output location"
EXAMPLES = [
    "inopaicli app_get_workflow_states -a 1 -o './directory'",
]


def init(parser: ArgumentParser):
    add_use_action_id(parser)
    parser.add_argument(
        "-o",
        "--outputdirectory",
        help="Specify the directory where to generate the json file with workflow information",
        required=True,
    )


def main(
    url: str,
    session_id: str,
    app: int,
    outputdirectory: str,
    **kwargs,
):
    data = get_app(url, app, session_id)
    workflow_states = data["application"].get("workflow_states", None)

    if workflow_states:
        for state in workflow_states:
            file_name = f'{outputdirectory}/app__{app}__wfstate__{state["id"]}.json'
            write_json(filename=file_name, data=state)

    return data
