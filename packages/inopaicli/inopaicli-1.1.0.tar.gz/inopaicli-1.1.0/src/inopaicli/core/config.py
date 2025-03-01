import os


def environ_or_required(key):
    if os.environ.get(key):
        return {"default": os.environ.get(key)}
    return {"required": True}


def parse_allowed_urls(argument_value: str) -> list[str]:
    if not argument_value:
        return []

    return [x.strip() for x in argument_value.split(",")]
