from inopaicli.concepts.app_action.api import action_update
from inopaicli.core.api import get_id_or_identifier
from inopaicli.core.file import read_json_file


def update_one_action(
    url: str, session_id: str, app: int, fullpath: str, useactionids: bool
):
    data = read_json_file(fullpath, quiet=True)
    data_id = data.get("id")
    identifier = f"app__{app}__action__{get_id_or_identifier(data, useactionids)}"

    if identifier not in fullpath:
        return

    print("-->", "action", identifier)

    action_update(
        url=url,
        session_id=session_id,
        data_id=data_id,
        data=data,
    )

    print(f"Action {identifier} updated")
