from argparse import ArgumentParser

DESCRIPTION = "Prints curl command with your session id and url"
EXAMPLES = [
    "inopaicli curl_print",
]


def init(parser: ArgumentParser):
    return


def main(url: str, session_id: str, **kwargs):
    print(
        f"curl -H 'cookie: sessionid={session_id}'"
        f"' -H 'Content-Type: application/json' '{url}'"
    )
