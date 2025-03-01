import os


def flatten_dict(dd: dict, separator='.', prefix='') -> dict:
    return {
        prefix + separator + k if prefix else k: v
        for kk,
        vv in dd.items() for k,
        v in flatten_dict(vv, separator, kk).items()
    } if isinstance(dd, dict) else {
        prefix: dd
    }


def split_and_trim(string: str) -> list[str]:
    if not string:
        return []

    return [x.strip() for x in string.split(',')]


def check_if_its_directory(dir_path: str):
    if not os.path.isdir(dir_path):
        if os.path.exists(dir_path):
            raise ValueError("Not a directory", dir_path)
        os.mkdir(dir_path)
