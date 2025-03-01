from inopaicli.core.api import simple_get


def get_group(baseurl: str, group_id: int, session_id: str) -> dict[str, dict]:
    return simple_get(baseurl=baseurl, url=f"/api/group/{group_id}/", session_id=session_id)


def group_list(baseurl: str, session_id: str, params: dict = {}) -> dict[str, dict]:
    return simple_get(baseurl=baseurl, url="/api/group/", session_id=session_id, params=params)
