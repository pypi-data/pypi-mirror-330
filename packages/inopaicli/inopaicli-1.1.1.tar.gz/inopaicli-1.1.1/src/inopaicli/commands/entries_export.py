import json
from argparse import ArgumentParser
from inopaicli.concepts.io_search.functions import io_search
from inopaicli.core.export import get_export_filename
from inopaicli.core.file import write_json

DESCRIPTION = "Export group ios entries in json format"
EXAMPLES = [
    "inopaicli entries_export -g 1 -a 1 -f '/filedir/filename.json'",
]


def init(parser: ArgumentParser):
    parser.add_argument("-a", "--app", type=int, help="Application ID")
    parser.add_argument("-g", "--group", type=int, help="Group ID")
    parser.add_argument(
        "-f",
        "--filename",
        help="Filename for destination json file (print if no filename given)",
    )
    parser.add_argument("--force", action="store_true", default=False)
    parser.add_argument("--query")
    parser.add_argument("--sourceoverride", default=None)
    parser.add_argument(
        "--limitresults", type=int, help="Total Results Limit", default=0
    )


def main(
    url: str,
    session_id: str,
    group: int,
    app: int,
    filename: str,
    limitresults: int = 0,
    query=None,
    force=False,
    sourceoverride=None,
    search_response_return=False,
    sort=None,
    embedded=None,
    detailled_query=None,
):
    if not search_response_return:
        filename = get_export_filename(
            group=group,
            app=app,
            suffix="json",
            filename=filename,
            force=force,
        )
    source_override = (
        json.loads(sourceoverride)
        if sourceoverride and isinstance(sourceoverride, str)
        else sourceoverride
    )

    search_response = io_search(
        url=url,
        session_id=session_id,
        group=group,
        app=app,
        query=query,
        modified=False,
        field_query_extra={},
        source_override=source_override,
        total_limit=limitresults,
        sort=sort,
        embedded=embedded,
        detailled_query=detailled_query,
    )
    if search_response_return:
        return search_response
    write_json(data=search_response["hits"], filename=filename)
