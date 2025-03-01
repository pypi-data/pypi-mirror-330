import os
import requests
import json
from argparse import ArgumentParser
from inopaicli.concepts.app.api import get_app, get_webios, get_webio_gna_branding_configs
from inopaicli.core.arguments import add_use_action_id

DESCRIPTION = "Download application from id and print it"
EXAMPLES = [
    "inopaicli app_get -a 1",
]

from inopaicli.core.api import simple_get


def get_applicationviews(baseurl: str, app_id: int, session_id: str) -> dict[str, dict]:
    return simple_get(
        baseurl=baseurl,
        url="/api/applicationview/",
        data={"app": app_id},
        session_id=session_id,
    )


def download_all_actions(*, url, session_id, app_id, output_folder):
    print("download_all_actions")
    for action in requests.get(
        f"{url}/api/action/?app={app_id}",
        cookies={
            "sessionid": session_id
        },
        timeout=60,
    ).json():
        # TODO: use same filename as in other projects: f"app__{action['application']}__action__{action['id']}.json"
        if not action["actiongna_count"]:
            print(f"Skipping action {action['id']} because actiongna_count == 0")
            continue
        for ignorekey in [
            "actiongna_count",
            "actionlog_stats",
            "activation_info",
            "context_requirements",
            "_permissions",
        ]:
            action.pop(ignorekey, None)
        write_json(
            base_folder=output_folder,
            data=action,
            filename=f"action__{action['semantic_identifier']}.json",
        )


def export_template_download(url, sessionid, exportid, local_filename):
    resp = requests.get(
        f"{url}/api/exports/{exportid}/downloadtemplate/",
        cookies={"sessionid": sessionid},
        stream=True,
        timeout=60,
    )
    if resp.status_code != 200:
        raise ValueError(f"File not available {resp.status_code}")
    with open(local_filename, "wb") as fp:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                fp.write(chunk)
                # f.flush() commented by recommendation from J.F.Sebastian


def download_all_exports(*, url, session_id, app_id, output_folder):
    print("download_all_exports")
    for export in simple_get(baseurl=url, url=f"/api/exports/?app={app_id}", session_id=session_id):
        export.pop("_gnas")
        if not export.get("exportgna_count"):
            print(f"Skipping export {export['id']} because exportgna_count == 0")
            continue
        exportbasename = f"templateexport__{export['semantic_identifier']}"
        filen = f"{exportbasename}.json"
        # print("export", export.get("id", None), "-->", filen)
        write_json(base_folder=output_folder, data=export, filename=filen)
        try:
            export_template_download(
                url=url,
                sessionid=session_id,
                exportid=export["id"],
                local_filename=os.path.join(output_folder, f"{exportbasename}__TEMPLATE.docx"),
            )
        except ValueError as exc:
            print(f"Export {export['id']} has no file --> Skipping", exc)
            continue


def download_all_forms(*, output_folder, app_id, url, session_id):
    print("download_all_forms")
    views = get_applicationviews(baseurl=url, session_id=session_id, app_id=app_id)
    for view in views:
        if not view["is_active"]:
            print(f"Skipping form {view['id']} because is_active == False")
            continue
        name = view["description"] or view["name"]
        fn = f"form__{name.replace('/', '__').replace(' ', '_')}__{view['id']}.json"
        # print(view, "-->", fn)
        write_json(output_folder, fn, view)


def download_all_webio_configs(*, output_folder, app_id, url, session_id):
    print("download_all_webio_configs")

    webios = get_webios(baseurl=url, session_id=session_id, app_id=app_id)
    for webio in webios:
        name = webio["name"] or webio["identifier"]
        fn = f"webio__{webio['id']}.json"
        write_json(output_folder, fn, webio)

        webio_branding_configs = get_webio_gna_branding_configs(
            baseurl=url, session_id=session_id, webio_id=webio["id"]
        )
        for webio_branding_config in webio_branding_configs:
            fn = f"webio_branding_config__{webio_branding_config['id']}.json"
            write_json(output_folder, fn, webio_branding_config)


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

    dat = data if "application" not in data else data["application"]

    output_folder = f'app__{dat["name"]}__{dat["id"]}'

    # print(data["application"]["schema"].keys())

    if os.path.exists(output_folder):
        if not force:
            raise ValueError(f"Folder exists {output_folder}")
    else:
        os.makedirs(output_folder)

    write_json(
        output_folder,
        "schema__properties.json",
        data["schema"]["properties"],
    )
    if 'definitions' in data["schema"]:
        write_json(
            output_folder,
            "schema__definitions.json",
            data["schema"]["definitions"],
        )
    if 'element_definitions' in data["schema"]:
        write_json(
            output_folder,
            "schema__element_definitions.json",
            data["schema"]["element_definitions"],
        )
    if 'createPageSchema' in data["schema"]:
        write_json(
            output_folder,
            "schema__createPageSchema.json",
            data["schema"]["createPageSchema"],
        )
    download_all_forms(
        output_folder=output_folder,
        app_id=app,
        url=url,
        session_id=session_id,
    )
    download_all_actions(
        output_folder=output_folder,
        app_id=app,
        url=url,
        session_id=session_id,
    )
    download_all_exports(
        output_folder=output_folder,
        app_id=app,
        url=url,
        session_id=session_id,
    )
    download_all_webio_configs(
        output_folder=output_folder,
        app_id=app,
        url=url,
        session_id=session_id,
    )
    return data
