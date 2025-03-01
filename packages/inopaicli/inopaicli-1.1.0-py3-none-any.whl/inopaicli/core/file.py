import csv
from os import walk
import os
import json
import tablib


def get_all_files(path: str, filter_extension=".json", recursive=False) -> list[str]:
    files = []

    for dirpath, dirnames, filenames in walk(path):
        for file_name in filenames:
            path, ext = os.path.splitext(file_name)
            if not filter_extension or ext == filter_extension:
                files.append(file_name)
        if recursive:
            for dirname in dirnames:
                for fine_name in get_all_files(os.path.join(dirpath, dirname)):
                    files.append(dirname + "/" + fine_name)
        break

    return files


def read_json_file(fullpath: str, quiet=False) -> any:
    if not quiet:
        print("Reading json file: ", fullpath)
    with open(fullpath, "rb") as file:
        datastr = file.read()

    data = json.loads(datastr)  # simple check if action is valid json

    return data


def read_csv_file(fullpath: str, quiet=False) -> any:
    if not quiet:
        print("Reading csv file: ", fullpath)
    with open(fullpath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(row for row in reader)

    return data


def read_file(fullpath: str, quiet=False) -> bytes:
    if not quiet:
        print("Reading file", fullpath)

    with open(fullpath, "rb") as file:
        datastr = file.read()

    return datastr


def write_json(data: dict, filename: str):
    with open(filename, "wb") as file:
        file.write(json.dumps(data, indent=2, ensure_ascii=False).encode())


def write_excel(tablib_data: list, filename: str, verbose: bool):
    dataset = tablib.Dataset(*tablib_data)

    if verbose:
        print("Writing to", filename)

    with open(filename, "wb") as file:
        file.write(dataset.export("xlsx"))
