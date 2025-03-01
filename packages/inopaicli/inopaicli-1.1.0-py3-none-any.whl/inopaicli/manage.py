import os
import argparse
from typing import Callable
from argparse import _SubParsersAction
from dotenv import load_dotenv
from inopaicli.core.arguments import add_initial_arguments
from inopaicli.core.auth import ask_for_password_if_missing, do_login
from inopaicli.core.commands import (
    get_subcommand_functions_map,
    print_plugin_folder_files_names,
    validate_selected_command,
)


def main(
    subcommand: str,
    subcommand_functions: dict[str, Callable],
    subparsers: _SubParsersAction,
    url: str,
    email: str,
    password: str,
    debug: bool,
    **subcommand_params,
) -> Callable:
    validate_selected_command(subcommand, subcommand_functions)

    print(f">>> Using INOPAI installation ### {url} ### with user {email}")

    if debug:
        print_plugin_folder_files_names()

    session_id = do_login(url=url, email=email, password=password)

    subcommand_params["subparsers"] = subparsers
    subcommand_params["session_id"] = session_id
    subcommand_params["url"] = url
    subcommand_params["debug"] = debug

    return subcommand_functions[subcommand](**subcommand_params)


def load_config():
    dotenvpath = f"{os.getcwd()}/.env"
    load_dotenv(dotenvpath, verbose=True)


def init():
    load_config()

    parser = argparse.ArgumentParser(
        description="Cli interface to execute inopai related tasks"
    )

    add_initial_arguments(parser)

    subparsers = parser.add_subparsers(dest="subcommand")

    subcommand_functions = get_subcommand_functions_map(subparsers)

    kwargs = vars(parser.parse_args())

    ask_for_password_if_missing(kwargs)

    main(**kwargs, subcommand_functions=subcommand_functions, subparsers=subparsers)
