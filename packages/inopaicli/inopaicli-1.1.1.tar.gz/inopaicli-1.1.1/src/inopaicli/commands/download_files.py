import asyncio
from argparse import ArgumentParser
from inopaicli.concepts.io_search.functions import io_search
from inopaicli.concepts.group.api import group_list
from inopaicli.concepts.group.functions import get_group_ids, get_subgroup_ids, get_group_mapping
from inopaicli.core.export import get_export_filename
from inopaicli.concepts.download_files.functions import get_file_urls, download_files_and_zip_async

DESCRIPTION = """
Export group io file entries in zip format and saving them to local file system
"""
EXAMPLES = [
    "inopaicli files_export -g 1 -a 1 -f '/filedir/filename.zip'",
]


def init(parser: ArgumentParser):
    parser.add_argument("-a", "--app", type=int, default=3, help="Application ID")
    parser.add_argument("-z", "--zip", action="store_true", help="Indicates zip flag is provided")
    parser.add_argument("--batch-size", type=int, default=5, help="Number of simultaneous downloads.")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("-g", "--group", type=int, help="Group ID")
    action.add_argument("-u", "--user", action="store_true", help="Indicates user flag is provided")
    action.add_argument("-o", "--org", type=int, help="Organization ID")


def main(
    url: str,
    session_id: str,
    app: int,
    user=False,
    org=None,
    group=None,
    zip=False,
    batch_size=5,
    subparsers=None,
    debug=None,
    force=False,
):
    group_list_data = group_list(url, session_id)
    group_mapping = get_group_mapping(group_list_data)

    io_groups = []
    if user:
        io_groups = get_group_ids(group_list_data)
    elif org:
        if group_mapping.get(org, {}).get("is_organisation") is not True:
            raise ValueError(f"Group {org} is not an organization")
        org_groups = get_subgroup_ids(group_list_data, org)
        io_groups = [org] + org_groups
    else:
        io_groups = [group]

    file_metas = []
    for group in io_groups:
        search_response = io_search(url=url, session_id=session_id, group=group, app=app, query=None)
        group_name = group_mapping.get(group, {}).get("name", f"group_{group}")
        group_file_urls = get_file_urls(url, search_response["hits"], group_id=group, group_name=group_name)
        file_metas.extend(group_file_urls)

    asyncio.run(
        download_files_and_zip_async(
            file_metas, cookies={"sessionid": session_id}, zip_flag=zip, batch_size=batch_size, debug=debug
        )
    )
