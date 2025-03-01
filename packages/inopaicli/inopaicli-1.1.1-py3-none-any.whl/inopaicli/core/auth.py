import getpass

import requests
from inopaicli.core.api import build_url


def do_login(url: str, email: str, password: str) -> str:
    resp = requests.post(
        build_url(url, "/api/_session/"),
        data={
            "email": email,
            "password": password,
        },
        timeout=60,
    )

    if resp.status_code > 200:
        print(resp, resp.text)

    if "sessionid" not in resp.cookies:
        raise Exception(f"Login not successful {url}")

    return resp.cookies["sessionid"]


def ask_for_password_if_missing(kwargs: dict[str, any]):
    missing_password_prompt_message = "Please enter your login password: "

    if not kwargs.get("password"):
        kwargs["password"] = getpass.getpass(missing_password_prompt_message)

        if not kwargs["password"]:
            kwargs["password"] = getpass.getpass(missing_password_prompt_message)
