from argparse import _SubParsersAction, ArgumentParser, RawTextHelpFormatter
import glob
from importlib import import_module, util
from importlib.machinery import SourceFileLoader
import os
from os.path import basename, dirname, isfile, join
from types import ModuleType
from typing import Callable

from inopaicli.core.constants import EXTERNAL_PLUGINS_FOLDER


def sort_commands(command_names: list[str]) -> list[str]:
    return sorted(command_names)


def get_commands_documentation(subparsers: _SubParsersAction) -> str:
    command_parsers_map: dict[str, ArgumentParser] = {}

    for name, subp in subparsers.choices.items():
        command_parsers_map[name] = subp

    sorted_command_names = sort_commands(command_parsers_map.keys())
    commands_documentation_text = "# Inopai CLI commands documentation\n\n"
    commands_documentation_text += "You can use the [commands_print](#commands_print)"
    commands_documentation_text += " command to get the documentation in terminal\n\n"
    commands_documentation_text += "## Here is a list of all the commands\n\n"

    for name in sorted_command_names:
        commands_documentation_text += f"- [{name}](#{name})\n"

    commands_documentation_text += "\n"

    for name in sorted_command_names:
        commands_documentation_text += f"## {name}\n"
        commands_documentation_text += f"{command_parsers_map[name].format_help()}"

    return commands_documentation_text


def print_commands_documentation(subparsers: _SubParsersAction) -> None:
    print(get_commands_documentation(subparsers))


def update_commands_documentation(subparsers: _SubParsersAction) -> None:
    with open(get_commands_documentation_path(), "wb") as file:
        file.write(get_commands_documentation(subparsers).replace("\n", "  \n"))


def add_subcommand_description(description: str, examples: list[str]) -> str:
    examples_description = ""

    for example in examples:
        examples_description += f"`{example}`\n"

    return f"description:\n{description}\n\n\nexamples: \n{examples_description}"


def add_subcommand_parser(
    subparsers: _SubParsersAction,
    command_name: str,
    description: str,
    *examples: list[str],
) -> ArgumentParser:
    return subparsers.add_parser(
        name=command_name,
        description=add_subcommand_description(description, examples),
        formatter_class=RawTextHelpFormatter,
    )


def validate_selected_command(
    subcommand: str,
    subcommand_functions: dict[str, Callable],
) -> None:
    if subcommand not in subcommand_functions:
        print(
            f'Unknown subcommand "{subcommand}".'
            f'Please use one of {", ".join(subcommand_functions.keys())}.'
        )
        raise SystemExit(1)

    return subcommand_functions


def get_subcommand_functions_map(subparsers: _SubParsersAction) -> str | None:
    subcommand_functions = {}
    subcommand_modules_map = {}
    all_commands = get_all_command_names()

    for command in all_commands:
        command_module = import_module(f".{command}", "inopaicli.commands")

        subcommand_modules_map[command] = {
            "module": command_module,
            "is_plugin": False,
        }

    all_plugins = get_all_plugin_names()

    for plugin in all_plugins:
        plugin_path = f"{get_external_plugins_folder_path()}{plugin}.py"

        subcommand_modules_map[plugin] = {
            "module": load_module(plugin, plugin_path),
            "is_plugin": True,
        }

    sorted_command_names = sort_commands(subcommand_modules_map.keys())

    for module_name in sorted_command_names:
        module = subcommand_modules_map[module_name]["module"]
        is_plugin = subcommand_modules_map[module_name]["is_plugin"]
        module_subcommand = get_subcommand_from_module(module_name, module, is_plugin)
        subcommand_parser = add_subcommand_parser(
            subparsers,
            module_name,
            module_subcommand["description"],
            *module_subcommand["examples"],
        )
        module_subcommand["init_function"](subcommand_parser)
        subcommand_functions[module_name] = module_subcommand["main_function"]

    return subcommand_functions


def load_module(name, filepath):
    loader = SourceFileLoader(name, filepath)
    spec = util.spec_from_loader(loader.name, loader)
    module = util.module_from_spec(spec)
    loader.exec_module(module)

    return module


def get_module_error(subcommand_name: str, problem: str, is_plugin: bool):
    plugin_prefix = f'Plugin "plugins/{subcommand_name}.py"'
    command_prefix = f'Command "commands/{subcommand_name}.py"'
    error_prefix = plugin_prefix if is_plugin else command_prefix

    print(f"{error_prefix} does not have a {problem}")
    raise SystemExit(1)


def get_subcommand_from_module(
    subcommand_name: str, module: ModuleType, is_plugin: bool
):
    try:
        description = getattr(module, "DESCRIPTION")
    except AttributeError:
        get_module_error(subcommand_name, "DESCRIPTION string constant", is_plugin)

    try:
        examples = getattr(module, "EXAMPLES")
    except AttributeError:
        get_module_error(subcommand_name, "EXAMPLES string array constant", is_plugin)

    try:
        init_function = getattr(module, "init")
    except AttributeError:
        get_module_error(subcommand_name, "init function", is_plugin)

    try:
        main_function = getattr(module, "main")
    except AttributeError:
        get_module_error(subcommand_name, "main function", is_plugin)

    return {
        "description": description,
        "examples": examples,
        "init_function": init_function,
        "main_function": main_function,
    }


def get_external_plugins_folder_path() -> str | None:
    path = f"{os.getcwd()}/{EXTERNAL_PLUGINS_FOLDER}/"
    return path


def print_plugin_folder_files_names():
    plugins_folder = "inopaicli-plugins"
    for root, dirs, _files in os.walk(os.getcwd()):
        if plugins_folder in dirs:
            folder_path = os.path.join(root, plugins_folder)

            try:
                file_names = [f for f in os.listdir(folder_path) if f.endswith(".py")]
            except FileNotFoundError:
                print(
                    f"Could not show the files in folder {folder_path}, because the folder does not exist or is not a directory"
                )
                return
            if file_names:
                print(
                    f"Looking for plugins in the folder {folder_path}, found files {file_names}"
                )
            else:
                print(f"{folder_path} folder found but no python files found")


def get_commands_folder_path() -> str | None:
    path = f"{dirname(dirname(__file__))}/commands/"

    return path


def get_commands_documentation_path() -> str | None:
    path = f"{dirname(dirname(dirname(dirname(__file__))))}/COMMANDS.md"

    return path


def get_all_command_names() -> list[str]:
    command_files = glob.glob(join(get_commands_folder_path(), "*.py"))
    all_command_names = [
        basename(f)[:-3]
        for f in command_files
        if isfile(f) and not f.endswith("__init__.py")
    ]

    return all_command_names


def get_all_plugin_names() -> list[str]:
    plugin_files = glob.glob(f"{get_external_plugins_folder_path()}*.py")
    all_plugin_names = [
        basename(f)[:-3]
        for f in plugin_files
        if isfile(f) and not f.endswith("__init__.py")
    ]
    return all_plugin_names


def get_all_subcommand_names() -> list[str]:
    command_files = glob.glob(join(get_commands_folder_path(), "*.py"))
    all_subcommands = [
        basename(f)[:-3]
        for f in command_files
        if isfile(f) and not f.endswith("__init__.py")
    ]

    return all_subcommands
