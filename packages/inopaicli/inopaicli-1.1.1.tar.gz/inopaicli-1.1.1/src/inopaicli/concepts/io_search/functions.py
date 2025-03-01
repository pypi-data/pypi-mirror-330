import time
import copy
from inopaicli.concepts.io_search.api import do_search_req
from inopaicli.concepts.io_search.constants import CHUNK_SIZE
from inopaicli.core.api import build_url


def get_app_view_io_search_params(
    url: str,
    session_id: str,
    group: list[str],
    app: int,
    field_query_extra: dict,
    query: str,
    source_override: list,
    embedded: list,
    search_once: bool,
    app_view: dict,
    modified: bool = False,
    sort: list = None,
    detailled_query: dict = None,
    total_limit=None,
):
    app_view = app_view if app_view else {}
    final_app = app_view.get("app") if app_view.get("app") else app
    final_query = app_view.get("q") if app_view.get("q") else query
    final_sort = app_view.get("sort") if app_view.get("sort") else sort
    final_field_query = (
        app_view.get("field_query")
        if app_view.get("field_query")
        else field_query_extra
    )
    final_detailled_query = (
        app_view.get("detailled_query")
        if app_view.get("detailled_query")
        else detailled_query
    )

    return {
        "url": url,
        "session_id": session_id,
        "embedded": embedded,
        "search_once": search_once,
        "modified": modified,
        "group": group,
        "app": final_app,
        "field_query_extra": final_field_query,
        "detailled_query": final_detailled_query,
        "query": final_query,
        "sort": final_sort,
        "source_override": source_override,
        "total_limit": total_limit,
    }


def io_search(
    url: str,
    session_id: str,
    group: int | list[int],
    app: int,
    query: str,
    modified=False,
    field_query_extra=None,
    sort=None,
    source_override=None,
    embedded=None,
    search_once=False,
    detailled_query=None,
    io_ids=None,
    total_limit=None,
):
    limit = CHUNK_SIZE if not total_limit or CHUNK_SIZE < total_limit else total_limit

    if field_query_extra is None:
        field_query_extra = {}

    if sort is None:
        sort = [{"id": {"order": "desc"}}]

    if embedded is None:
        embedded = []

    if io_ids is None:
        io_ids = []

    final_field_query = field_query_extra

    if group:
        final_field_query["group"] = group
    if io_ids:
        final_field_query["id"] = io_ids
        final_field_query.pop("io_type")
    elif app:
        final_field_query["io_type"] = [app]
    if modified:
        final_field_query["modified"] = [int(modified)]

    json_data = {
        "q": query,
        "field_query": final_field_query,
        "detailled_query": detailled_query,
        "limit": limit,
        "sort": sort,
        "exclude_permissions": True,
        "_embedded": embedded,
        # 'use_scroll': True, <-- this will cause the search view to return all in one response --> use_scroll=True
        # 'scroll_token': os.environ.get('SEARCHSCROLLTOKEN'),
    }

    if source_override:
        json_data["_source_override"] = source_override

    query_params = dict(
        url=build_url(url, "/api/search/"),
        headers={
            "Content-Type": "application/json",
        },
        json_data=json_data,
        cookies={"sessionid": session_id},
    )

    # print(json.dumps(query_params))
    # print('Search query start')

    start_time = time.time()
    resp = do_search_req(**query_params)
    resp_data = resp.json()

    hits = resp_data["hits"]["hits"]
    total = resp_data["hits"]["total"]

    print(
        f"app {app}" if all else "",
        f"> Total {total}, {round(resp.elapsed.total_seconds(), 2)}s.",
        #  jsondata: {json.dumps(json_data)}"
        end=" ",
        flush=True,
    )

    if not search_once:
        total = resp_data["hits"]["total"]
        current_hits = resp_data["hits"]["hits"]

        while total > len(hits) and (not total_limit or total_limit > len(hits)):
            current_hits = resp_data["hits"]["hits"]
            next_query_params = copy.deepcopy(query_params)

            current_hits_len = len(current_hits)
            if total_limit and current_hits_len + limit <= total_limit:
                next_query_params["json_data"]["offset"] = current_hits_len
            elif not current_hits and total - current_hits_len < 10:
                break
            else:
                last_item_array = current_hits[current_hits_len - 1 : current_hits_len]

                if last_item_array:
                    last_item = last_item_array.pop()
                    last_item_id = last_item.get("_id")
                    next_query_params["json_data"]["search_after"] = [last_item_id]
                    next_query_params["json_data"]["offset"] = 0
            print(
                # "There are more results in this query --> Do another request",
                # total,
                len(hits),
                # next_query_params["json_data"].get("offset", None),
                f"{round(time.time() - start_time, 2)}s",
                end=" ",
                flush=True,
            )
            start_time = time.time()
            resp = do_search_req(**next_query_params)
            resp_data = resp.json()
            hits.extend(resp_data["hits"]["hits"])

    print()
    embedded = resp_data["_embedded"] if "_embedded" in resp_data else None
    apps = embedded["apps"] if embedded and "apps" in embedded else []
    r_ios = embedded["related_ios"] if embedded and "related_ios" in embedded else []

    return {
        "hits": hits,
        "total": total,
        "apps": apps,
        "related_ios": r_ios,
    }
