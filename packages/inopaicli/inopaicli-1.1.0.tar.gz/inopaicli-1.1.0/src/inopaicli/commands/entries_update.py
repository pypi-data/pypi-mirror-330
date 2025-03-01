import json
from argparse import ArgumentParser

from inopaicli.core.api import simple_request

DESCRIPTION = "Update entries from requested file"
EXAMPLES = [
    "inopaicli ios_patch --request_data_file ./requested-file.json",
]


def init(parser: ArgumentParser):
    parser.add_argument('--request_data_file', help="Requested file")


def main(url: str, session_id: str, request_data_file: str, **kwargs):
    with open(request_data_file, "rb") as file:
        request_data = json.loads(file.read())

    print('request data: ', request_data)

    resp = simple_request(
        base_url=url,
        url="/api/io/ios_patch/",
        session_id=session_id,
        json=request_data,
        method="post",
    )
    print(resp)
