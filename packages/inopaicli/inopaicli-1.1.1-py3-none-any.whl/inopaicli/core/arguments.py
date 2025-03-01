from argparse import ArgumentParser
import os

from inopaicli.core.config import environ_or_required


def add_allowed_urls_argument(parser: ArgumentParser):
    parser.add_argument(
        "--allowedurls", default=os.environ.get("INOPAICLI_ALLOWED_URLS")
    )


def add_use_action_id(parser: ArgumentParser):
    parser.add_argument(
        "-a",
        "--app",
        type=int,
        help="Application ID",
        required=True,
    )


def add_use_action_ids_argument(parser: ArgumentParser):
    parser.add_argument(
        "--useactionids",
        help="Use action ids instead of action identifiers",
        action="store_true",
    )


def add_initial_arguments(parser: ArgumentParser):
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("-u", "--url", **environ_or_required("INOPAI_URL"))
    parser.add_argument("-e", "--email", **environ_or_required("INOPAI_EMAIL"))
    parser.add_argument("-p", "--password", default=os.environ.get("INOPAI_PASSWORD"))
