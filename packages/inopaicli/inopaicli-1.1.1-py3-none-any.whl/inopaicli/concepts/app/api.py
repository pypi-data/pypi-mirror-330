from inopaicli.core.api import simple_get, simple_request


def get_app(baseurl: str, app_id: int, session_id: str) -> dict[str, dict]:
    return simple_get(
        baseurl=baseurl, url=f"/api/app/{app_id}/", session_id=session_id
    )["application"]


def get_apps(baseurl: str, app_ids: list[int], session_id: str) -> dict[str, dict]:
    query = "&id[]=".join([str(a) for a in app_ids])
    return simple_get(
        baseurl=baseurl, url=f"/api/app/?id[]={query}", session_id=session_id
    )


def get_time_entries(
    baseurl: str, app_id: int, session_id: str, debug: bool
) -> dict[str, list]:
    results: dict[str, list] = {}
    load = True
    page = 1
    while load:
        try:
            response = simple_get(
                baseurl=baseurl,
                url=f"/api/extended_timeentry/?app={app_id}&page={page}",
                session_id=session_id,
            )
            for r in response:
                if results.get(str(r.get("io")), None) is None:
                    results[str(r.get("io"))] = [r]
                else:
                    results[str(r.get("io"))].append(r)
            if debug:
                print(f"loading page {page}")
            page = page + 1
        except Exception:
            load = False
    return results


def get_webios(baseurl: str, app_id: int, session_id: str) -> dict[str, dict]:
    return simple_get(
        baseurl=baseurl, url=f"/api/app/{app_id}/webio/", session_id=session_id
    )


def get_webio_gna_branding_configs(
    baseurl: str, webio_id: int, session_id: str
) -> dict[str, dict]:
    return simple_get(
        baseurl=baseurl,
        url=f"/api/webio/gna_branding_config/list/{webio_id}/",
        session_id=session_id,
    )


def update_app_instance(base_url: str, session_id: str, data: dict):
    response = simple_request(
        base_url=base_url,
        url="/api/update_app_instance/",
        session_id=session_id,
        json=data,
        method="post",
        systemexit=False,
    )

    if response.status_code > 201:
        raise ValueError(response.text)
        return {"ok": False, "status": response.status_code}

    return response.json()
