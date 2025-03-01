def get_group_list_from_appview_if_empty(group_list: list[int],
                                         app_view: dict) -> list[str]:
    final_group_list = []

    if not group_list:
        if app_view and 'group' in app_view and app_view.get('group'):
            app_view_group_id = app_view.get('group')

            print(f"Using group from appview definition: {app_view_group_id}")

            final_group_list = [app_view_group_id]
    else:
        final_group_list = group_list

    return final_group_list


def get_io_properties_from_appview_columns(app_view: dict) -> list[str]:
    final_properties = []

    if app_view and 'columns' in app_view and app_view.get('columns'):
        app_view_columns = app_view.get('columns')
        app_view_column_names = []

        for app_view_column in app_view_columns:
            if 'name' in app_view_column and app_view_column.get('name'):
                app_view_column_names.append(app_view_column.get('name'))

        final_properties = [
            name.replace('property__', 'properties.') for name in app_view_column_names
        ]

    return final_properties
