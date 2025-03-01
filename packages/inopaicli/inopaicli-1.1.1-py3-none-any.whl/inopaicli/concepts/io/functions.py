import json
from inopaicli.concepts.io.api import io_import_json


def import_ios(
    *,
    url: str,
    session_id: str,
    app: int,
    group: int,
    property_name: str,
    ios: list[any],
    prevent_io_create: bool,
    prevent_io_update: bool,
    debug: bool,
    user_forces_skip_actions=None,
):
    json_data = {
        "app": app,
        "group": group,
        "property_name": property_name,
        "ios": ios,
        "prevent_io_create": prevent_io_create,
        "prevent_io_update": prevent_io_update,
    }
    if user_forces_skip_actions:
        json_data['user_forces_skip_actions'] = user_forces_skip_actions

    data = io_import_json(url, session_id, json_data)

    if debug:
        print(json.dumps(data, indent=2))

    return data
