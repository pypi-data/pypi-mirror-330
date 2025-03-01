from argparse import _SubParsersAction, ArgumentParser
from inopaicli.core.commands import print_commands_documentation, update_commands_documentation

DESCRIPTION = "Prints all command documentations"
EXAMPLES = [
    "inopaicli commands_print",
    "inopaicli commands_print --devupdate",
]


def init(parser: ArgumentParser):
    parser.add_argument(
        "-d",
        "--devupdate",
        action="store_true",
        help="Used from a developer to update the COMMANDS.md file",
    )


def main(subparsers: _SubParsersAction, devupdate: bool, **kwargs):
    if devupdate:
        update_commands_documentation(subparsers)

        print("Updated COMMANDS.md file")
    else:
        print_commands_documentation(subparsers)
