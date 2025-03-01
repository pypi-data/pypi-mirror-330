import requests
from inopaicli.core.api import build_url


def action_update(url: str, session_id: str, data_id: int, data: any):
    resp = requests.put(
        build_url(url, f"/api/action/{data_id}/"),
        headers={
            "Content-Type": "application/json",
        },
        json=data,
        cookies={"sessionid": session_id},
    )

    if resp.status_code != 200:
        print(resp, resp.text)
        raise Exception(resp.status_code)

    return resp.json()


def get_actions(url: str, session_id: str, app: int, debug=False):
    resp = requests.get(
        build_url(url, f"/api/action/?app={app}"), cookies={"sessionid": session_id}
    )

    if debug or resp.status_code > 200:
        print(resp, resp.text)

    return resp.json()
