import json

import requests
from inopaicli.core.api import build_url


def get_exports(url: str, session_id: str, app: int, debug=False):
    resp = requests.get(
        build_url(url, f"/api/exports/?app={app}"), cookies={"sessionid": session_id}
    )

    if debug or resp.status_code > 200:
        print(resp, resp.text)

    return resp.json()


def export_template_download(
    url: str, session_id: str, export_id: int, local_filename: str
):
    resp = requests.get(
        build_url(url, f"/api/exports/{export_id}/downloadtemplate/"),
        cookies={"sessionid": session_id},
        stream=True,
    )

    if resp.status_code == 200 and resp.status_code:
        with open(local_filename, "wb") as file:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)


def export_update(url: str, session_id: str, data, template_file):
    data_id = data.get("id")
    data["request_headers"] = json.dumps(data["request_headers"])
    data["default_values"] = json.dumps(data["default_values"])
    resp = requests.patch(
        build_url(url, f"/api/exports/{data_id}/"),
        data=data,
        files={"template_file": template_file},
        cookies={"sessionid": session_id},
    )

    if resp.status_code != 200:
        print(resp, resp.text)
        raise Exception(resp.status_code)
    print("Export upload ok", id)

    return resp.json()
