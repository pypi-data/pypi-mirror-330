import requests


def build_url(base_url: str, path: str) -> str:
    return f"{base_url}{path}"


def calculate_end(*, i: int, chunk_count: int, chunk_size: int, rest: int) -> int:
    result = ((i + 1) * chunk_size) - 1
    if i == (chunk_count - 1):
        result = (i + 1) * chunk_size + rest
    return result


def get_id_or_identifier(data: any, useactionids: bool) -> int:
    return data.get("id") if useactionids else data.get("identifier")


def get_requests_func(method: str) -> requests.Response:
    if method == "put":
        return requests.put
    if method == "post":
        return requests.post
    if method == "get":
        return requests.get
    if method == "delete":
        return requests.delete
    if method == "patch":
        return requests.patch
    raise ValueError(f"Please add method {method}")


def simple_request(
    base_url: str,
    url: str,
    session_id: str,
    method: str,
    systemexit=True,
    **requestskw,
):
    func = get_requests_func(method)
    full_url = build_url(base_url, url)

    resp = func(full_url, cookies={"sessionid": session_id}, **requestskw)

    if resp.status_code > 201:
        print(full_url, method, requestskw)
        print(resp, resp.text)
        if systemexit:
            raise SystemExit(1)

    return resp


def simple_get(baseurl: str, url: str, session_id: str, **kw):
    resp = requests.get(
        build_url(baseurl, url),
        **kw,
        cookies={"sessionid": session_id},
        timeout=120,
    )

    if resp.status_code > 200:
        print(resp, resp.text)

    return resp.json()
