from inopaicli.core.api import simple_get


def get_app_view(baseurl: str, session_id: str, appview_id: int) -> dict[str, dict]:
    if not appview_id:
        return None

    return simple_get(
        baseurl=baseurl, url=f"/api/appview/{appview_id}/", session_id=session_id
    )
