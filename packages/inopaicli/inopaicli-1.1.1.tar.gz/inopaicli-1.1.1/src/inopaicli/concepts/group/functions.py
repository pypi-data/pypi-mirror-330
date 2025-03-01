def get_group_ids(group_list_data: dict[str, dict]):
    return [group["id"] for group in group_list_data["rows"]]


def get_subgroup_ids(group_list_data: dict[str, dict], org: int):
    return [group["id"] for group in group_list_data["rows"] if group["parent"] is org]


def get_group_mapping(group_list_data: dict[str, dict]):
    return {group["id"]: group for group in group_list_data["rows"]}
