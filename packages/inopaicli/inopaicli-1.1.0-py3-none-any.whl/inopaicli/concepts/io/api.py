from inopaicli.core.api import simple_request


def io_import_json(base_url: str, session_id: str, json_data: any):
    resp = simple_request(
        base_url=base_url,
        url="/api/io/import_json/",
        session_id=session_id,
        json=json_data,
        method="post",
    )
    if resp.status_code != 200:
        print(resp.status_code, resp.content)
    return resp.json()


def ios_delete(base_url: str, session_id: str, ids_lst: any):
    resp = simple_request(
        base_url=base_url,
        url="api/io/delete/",
        session_id=session_id,
        json={"ios": ids_lst},
        method="post",
        systemexit=False,
    )
    if resp.status_code == 400:
        print(resp.status_code)
        return []
    return resp.json()


def io_single_get_history(base_url: str, session_id: str, io_id: int):
    resp = simple_request(
        base_url=base_url,
        url=f"/api/io/{io_id}/version/",
        session_id=session_id,
        method="get",
    )
    return resp.json()


def io_list(url: str, session_id: str, params: dict = {}):
    resp = simple_request(
        base_url=url, url="/api/io/", session_id=session_id, method="get", systemexit=False, params=params
    )
    if resp.status_code == 400:
        print(resp.status_code)
        return []
    return resp.json()
