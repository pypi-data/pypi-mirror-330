from inopaicli.concepts.io.constants import IO_MAIN_ATTRIBUTES
from inopaicli.concepts.io_search.constants import RELATION_LEVELS
from inopaicli.concepts.io_search.functions import io_search
from inopaicli.core.file import write_excel
from inopaicli.core.util import flatten_dict


def get_columns_from_search_response(
    app_id: int,
    search_response: dict,
    columns: str,
    relation_level: int,
    app_view_properties: list[str],
    search_params: dict,
) -> dict:
    column_map = get_column_value_map(
        app_id, search_response, relation_level, search_params
    )
    ordered_columns = get_final_ordered_columns(
        column_map, columns, app_view_properties
    )

    return ordered_columns


def get_io_attribute_headers(relation_header_text="") -> list[str]:
    attribute_headers = [
        get_io_attribute_header("id", relation_header_text),
        get_io_attribute_header("title", relation_header_text),
    ]

    return attribute_headers


def get_io_attribute_header(attribute_name: str, relation_header_text="") -> list[str]:
    attribute_header = IO_MAIN_ATTRIBUTES.get(attribute_name)

    if relation_header_text:
        return f"{relation_header_text} {attribute_header}"
    return f"{attribute_header}"


def get_app_from_list(app_id: int, apps: list) -> list[str]:
    matches = list(filter(lambda app: app.get("id") == app_id, apps))
    return matches[0]


def get_io_property_columns(app_id: int, apps: list) -> dict[str, dict]:
    main_app = get_app_from_list(app_id, apps)
    main_app_schema = main_app.get("schema")
    main_app_schema_properties = main_app_schema.get("properties")
    columns = {}

    for propname, value in main_app_schema_properties.items():
        columns[propname] = {
            "is_relation": value.get("format") == "relation",
            "relation_app_id": value.get("ranges", [None])[0],
            "header_text": value.get("verbose_name"),
        }

    return columns


def get_io_headers(
    column_map: dict[str, str],
    ordered_columns: list[str],
) -> list[str]:
    headers = []

    for column_key in ordered_columns:
        column = column_map.get(column_key)
        headers.append(column)

    return headers


def get_io_rows(
    search_response: dict,
    ordered_columns: list[str],
) -> list:
    hits = search_response["hits"] if "hits" in search_response else []
    rows_data = []

    for io in hits:
        io_source = io.get("_source")
        line = []

        flat_source = flatten_dict(io_source)

        for column_key in ordered_columns:
            line.append(flat_source.get(column_key))

        rows_data.append(tuple(line))

    return rows_data


def get_column_value_map(
    app_id: int,
    search_response: dict,
    relation_level: int,
    search_params: dict,
) -> dict[str, str]:
    apps = search_response["apps"] if "apps" in search_response else []
    main_property_columns = get_io_property_columns(app_id, apps)
    headers = get_io_attribute_headers()
    deep_relation_properties_map = {}
    column_map = {
        "id": headers[0],
        "title": headers[1],
    }

    for column_key in main_property_columns:
        column = main_property_columns.get(column_key)

        if column.get("is_relation"):
            if not relation_level > RELATION_LEVELS["NO_RELATIONS"]:
                continue

            relation_header_text = column.get("header_text")
            relation_headers = get_io_attribute_headers(relation_header_text)
            column_map[f"properties.{column_key}.id"] = relation_headers[0]
            column_map[f"properties.{column_key}.title"] = relation_headers[1]
            relation_columns = get_io_property_columns(
                column.get("relation_app_id"), apps
            )

            for relation_column_key in relation_columns:
                relation_column = relation_columns.get(relation_column_key)
                current_header_text = relation_column.get("header_text")
                map_id = f"properties.{column_key}.properties.{relation_column_key}"

                if relation_column.get("is_relation"):
                    if not relation_level == RELATION_LEVELS["WITH_DEEP_RELATIONS"]:
                        continue

                    deep_relation_properties_map[map_id] = current_header_text
                else:
                    column_map[map_id] = f"{relation_header_text} {current_header_text}"
        else:
            column_map[f"properties.{column_key}"] = column.get("header_text")

    if deep_relation_properties_map:
        add_deep_relations(
            deep_relation_properties_map, column_map, search_response, search_params
        )

    return column_map


def add_deep_relations_to_column_map(
    rel_search_response: dict, column_map: dict[str, str], related_io_ids_map: dict
) -> None:
    rel_apps = rel_search_response["apps"] if "apps" in rel_search_response else []
    rel_hits = rel_search_response["hits"] if "hits" in rel_search_response else []

    for io in rel_hits:
        io_id = io.get("_id")
        io_source = io.get("_source")
        io_app_id = io_source.get("io_type")
        deep_relation_data = related_io_ids_map.get(io_id)

        if not deep_relation_data:
            continue

        deep_relation_property = deep_relation_data["deep_relation_property"]
        relation_header_text = deep_relation_data["relation_header_text"]
        related_app_columns = get_io_property_columns(io_app_id, rel_apps)

        for column_key in related_app_columns:
            column = related_app_columns.get(column_key)

            relation_headers = get_io_attribute_headers(relation_header_text)
            column_map[f"{deep_relation_property}.id"] = relation_headers[0]
            column_map[f"{deep_relation_property}.title"] = relation_headers[1]

            if not column.get("is_relation"):
                column_map[f"{deep_relation_property}.properties.{column_key}"] = (
                    f"{relation_header_text} {column.get('header_text')}"
                )


def add_deep_relations_to_search_response(
    rel_search_response: dict, search_response: dict, related_io_ids_map: dict
) -> None:
    rel_hits = rel_search_response["hits"] if "hits" in rel_search_response else []

    for io in rel_hits:
        io_id = io.get("_id")
        io_source = io.get("_source")
        deep_relation_data = related_io_ids_map.get(io_id)

        if not deep_relation_data:
            continue

        deep_relation_property = deep_relation_data["deep_relation_property"]
        base_io_id = deep_relation_data["base_io_id"]
        deep_relation_property_splitted = deep_relation_property.split(".")
        first_relation_property = deep_relation_property_splitted[1]
        second_relation_property = deep_relation_property_splitted[3]

        base_io = next(
            filter(lambda hit: hit.get("_id") == base_io_id, search_response["hits"]),
            None,
        )
        base_io["_source"]["properties"][first_relation_property]["properties"][
            second_relation_property
        ] = io_source


def add_deep_relations(
    deep_relation_properties_map: list[str],
    column_map: dict[str, str],
    search_response: dict,
    search_params: dict,
) -> None:
    hits = search_response["hits"] if "hits" in search_response else []
    related_io_ids_map = {}

    for io in hits:
        io_id = io.get("_id")
        io_source = io.get("_source")

        flat_source = flatten_dict(io_source)

        for deep_relation_property in deep_relation_properties_map:
            related_io_id = flat_source.get(deep_relation_property)
            relation_header_text = deep_relation_properties_map[deep_relation_property]

            if not related_io_id:
                continue

            related_io_ids_map[f"{related_io_id}"] = {
                "base_io_id": io_id,
                "deep_relation_property": deep_relation_property,
                "relation_header_text": relation_header_text,
            }

    related_io_ids = list(related_io_ids_map.keys())
    rel_search_response = io_search(**search_params, io_ids=related_io_ids)

    add_deep_relations_to_column_map(
        rel_search_response, column_map, related_io_ids_map
    )

    add_deep_relations_to_search_response(
        rel_search_response, search_response, related_io_ids_map
    )


def append_column_considering_app_view_properties(
    ordered_columns: list[str], app_view_properties: list[str], column
):
    column_with_stripped_inner_props = ".".join(column.split(".", 2)[:2])
    is_column_in_app_view = column_with_stripped_inner_props in app_view_properties

    if not app_view_properties or is_column_in_app_view:
        ordered_columns.append(column)


def get_final_ordered_columns(
    column_map: dict[str, str], columns: str, app_view_properties: list[str]
) -> list[str]:
    ordered_columns = []
    columns_map_keys = column_map.keys()

    if columns:
        for column in columns.split(","):
            if column in columns_map_keys:
                append_column_considering_app_view_properties(
                    ordered_columns, app_view_properties, column
                )
            else:
                print(f"Input column {column} does not exist in the search result")

        print("Ordered columns from argument: ", ordered_columns)
    else:
        for column in columns_map_keys:
            append_column_considering_app_view_properties(
                ordered_columns, app_view_properties, column
            )

    return ordered_columns


def build_excel_for_search_response(
    main_app_id: int,
    search_response: dict,
    filename: str,
    columns: str,
    relation_level: int,
    app_view_properties: list[str],
    search_params: list[str],
):
    column_map = get_column_value_map(
        main_app_id, search_response, relation_level, search_params
    )
    ordered_columns = get_final_ordered_columns(
        column_map, columns, app_view_properties
    )
    headers = get_io_headers(column_map, ordered_columns)
    rows = get_io_rows(search_response, ordered_columns)

    excel_data = [headers, *rows]

    write_excel(excel_data, filename, True)
