import requests


def do_search_req(url: str, headers: str, json_data, cookies: str):
    resp = requests.post(url=url, headers=headers, json=json_data, cookies=cookies)

    if resp.status_code != 200:
        print(resp, resp.text)
        raise Exception(resp.status_code)

    return resp
