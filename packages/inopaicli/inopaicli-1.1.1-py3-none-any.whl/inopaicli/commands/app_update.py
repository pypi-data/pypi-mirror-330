import os
import json
from argparse import ArgumentParser
from inopaicli.concepts.app.api import get_app
from inopaicli.core.arguments import add_use_action_id

DESCRIPTION = "Download application from id and print it"
EXAMPLES = [
    "inopaicli app_get -a 1",
]

from inopaicli.core.api import simple_get


#     re_path(
#         r'app/(?P<app_id>\d+)/schema/',
#         hdv(routes={'put': trip.flexio.views.app_update_schema_view})
#     ),
# @return_401_if_is_anonymous
# @require_json_request_get_request_content(
#     allowed_properties=[
#         'definitions',
#         'uiSchema',
#         'createPageSchema',
#     ],
#     required_properties=[
#         'properties',
#         'type',
#     ]
# )


# definitions
# element_definitions
# createPageSchema


def get_applicationviews(baseurl: str, app_id: int, session_id: str) -> dict[str, dict]:
    return simple_get(
        baseurl=baseurl,
        url="/api/applicationview/",
        data={"app": app_id},
        session_id=session_id,
    )


def action_update(url, sessionid, identifier, data):
    actionurl = build_url(url, f"/api/action/{identifier}/")

    resp = requests.put(
        actionurl,
        headers={
            "Content-Type": "application/json",
        },
        json=data,
        cookies={"sessionid": sessionid},
    )
    if resp.status_code != 200:
        print(resp, resp.text)
        raise Exception(resp.status_code)

    return resp.json()


def update_one_action(url, sessionid, app, fullpath):
    data = read_json_file(fullpath)
    # print(data)

    app_in_data = data.get("application")
    if app_in_data != app:
        print(app_in_data, "!=", app)
        raise Exception(
            "Safety flag: Please make sure you pass the correct app before you update!"
        )
    identifier = data.pop("id")  # path.split('_')[1]
    print("-->", "action", identifier)
    if str(identifier) not in fullpath:
        raise Exception(
            f'Assumption is that the action id is also contained inside the filename --> Cannot continue, please check "id": {identifier} property in file {filename}'
        )
    action_update(
        url=url,
        sessionid=sessionid,
        identifier=identifier,
        data=data,
    )
    print(f"Action {identifier} updated :)")


def actions_update(url, sessionid, app, folder, debug=False):
    # os.path.dirname(
    dir_path = os.path.realpath(folder)
    if not os.path.isdir(dir_path):
        raise ValueError("Not a directory", dir_path)
    for fn in get_all_files(dir_path):
        if fn == "app_schema_cps.json":
            print("Ignoring app form schema")
            continue
        fullpath = os.path.realpath(os.path.join(dir_path, fn))
        try:
            update_one_action(
                url=url,
                sessionid=sessionid,
                app=app,
                fullpath=fullpath,
            )
        except Exception as exc:
            print(exc)


def export_update(url, sessionid, data, template_file):
    id = data.get("id")
    data["request_headers"] = json.dumps(data["request_headers"])
    data["default_values"] = json.dumps(data["default_values"])
    resp = requests.patch(
        build_url(url, f"/api/exports/{id}/"),
        data=data,
        files={"template_file": template_file},
        cookies={"sessionid": sessionid},
    )
    if resp.status_code != 200:
        print(resp, resp.text)
        raise Exception(resp.status_code)
    else:
        print("Export upload ok", id)
    return resp.json()


def exports_update(url, sessionid, folder, app=None, debug=False):
    dir_path = os.path.realpath(folder)

    print("url", url)

    assert url in ALLOWED_URLS

    if not os.path.isdir(dir_path):
        raise ValueError("Not a directory", dir_path)
    for fn in get_all_files(dir_path):
        if ".docx" in fn:
            print("Ignoring template")
            continue

        path = os.path.realpath(os.path.join(dir_path, fn))
        data = read_json_file(path)

        export_app = export_id = data.get("app")
        if app and app != export_app:
            print("Skipping", fn, "Only syncing exports for app", app)
            continue

        export_id = data.get("id")
        template_docx_path = os.path.realpath(
            os.path.join(
                dir_path, f"app__{export_app}__export__{export_id}__TEMPLATE.docx"
            )
        )
        template_file = read_file(template_docx_path)

        export_update(
            url=url,
            sessionid=sessionid,
            data=data,
            template_file=template_file,
        )


def applicationview_patch(url, sessionid, identifier, data):
    url = build_url(url, f"/api/applicationview/{identifier}/")
    resp = requests.patch(
        url,
        headers={
            "Content-Type": "application/json",
        },
        json=data,
        cookies={"sessionid": sessionid},
    )
    if resp.status_code != 200:
        print(resp, resp.text)
        raise Exception(resp.status_code)

    return resp.json()


def update_one_applicationview(url, sessionid, app, fullpath):
    data = read_json_file(fullpath)

    identifier = data.pop("id")

    if data["app"] != app:
        print(
            f"Skipping applicationview id {identifier} because it belongs to app {data['app']} (currently updating app {app}) "
        )
        return
        # print(data)
        # print(data['app'], '!=', app)
        # raise Exception(
        #     'Safety flag: Please make sure you pass the correct app before you update!'
        # )

    print(f'App {data.get("app")} applicationview {identifier} patch')

    applicationview_patch(
        url=url,
        sessionid=sessionid,
        identifier=identifier,
        data=data,
    )


def applicationviews_update(url, sessionid, app, folder, debug=False):
    # os.path.dirname(
    dir_path = os.path.realpath(folder)
    if not os.path.isdir(dir_path):
        raise ValueError("Not a directory", dir_path)

    for fn in get_all_files(dir_path):
        if fn == "app_schema_cps.json":
            print("Ignoring app form schema")
            continue
        if fn == "element_definitions.json":  # TODO: this line can be removed
            print("Ignoring element_definitions")
            continue

        path, ext = os.path.splitext(fn)
        fullpath = os.path.realpath(os.path.join(dir_path, fn))
        update_one_applicationview(
            url=url, sessionid=sessionid, app=app, fullpath=fullpath
        )


def write_json(base_folder, filename, data, force=True):
    fn = os.path.join(base_folder, filename)
    if os.path.exists(fn) and not force:
        raise ValueError("Already exists", fn)
    with open(fn, "wb") as fp:
        fp.write(json.dumps(data, indent=2, ensure_ascii=False).encode())


def init(parser: ArgumentParser):
    add_use_action_id(parser)
    parser.add_argument(
        "-f",
        "--force",
        help="Override data in folder",
        required=False,
        default=False,
        action="store_true",
    )


def main(
    url: str,
    session_id: str,
    app: int,
    force,
    **kwargs,
):
    data = get_app(url, app, session_id)
    # print(json.dumps(data, indent=2))

    output_folder = f'{data["application"]["name"]}__{data["application"]["id"]}'

    # print(data["application"]["schema"].keys())

    if os.path.exists(output_folder):
        if not force:
            raise ValueError(f"Folder exists {output_folder}")
    else:
        os.makedirs(output_folder)

    write_json(
        output_folder, "properties.json", data["application"]["schema"]["properties"]
    )
    write_json(
        output_folder, "definitions.json", data["application"]["schema"]["definitions"]
    )
    write_json(
        output_folder,
        "element_definitions.json",
        data["application"]["schema"]["element_definitions"],
    )
    write_json(
        output_folder,
        "createPageSchema.json",
        data["application"]["schema"]["createPageSchema"],
    )

    views = get_applicationviews(baseurl=url, session_id=session_id, app_id=app)
    for view in views:
        fn = f"form__{view['id']}__{view['name'].replace('/', '__').replace(' ', '_')}.json"
        # print(view, "-->", fn)
        write_json(output_folder, fn, view)

    return data
