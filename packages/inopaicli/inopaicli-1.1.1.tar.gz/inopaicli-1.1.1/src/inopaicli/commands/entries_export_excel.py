from argparse import ArgumentParser
from inopaicli.concepts.app_view.api import get_app_view
from inopaicli.concepts.app_view.functions import get_group_list_from_appview_if_empty, get_io_properties_from_appview_columns
from inopaicli.concepts.io_search.constants import RELATION_LEVELS
from inopaicli.concepts.io_search.excel_export import build_excel_for_search_response, get_columns_from_search_response
from inopaicli.concepts.io_search.functions import get_app_view_io_search_params, io_search
from inopaicli.core.export import get_export_filename

DESCRIPTION = "Export group ios entries in excel format"
EXAMPLES = [
    "inopaicli entries_export_excel -g 1 -a 1 --printcolumns",
    "inopaicli entries_export_excel -g 1 -a 1 --printcolumns --relationlevel 2",
    'inopaicli entries_export_excel -g 1 -a 1 --columns "id, properties.firstname" --force',
    "inopaicli entries_export_excel -g 1 2 3 -a 1 -f '/filedir/filename.xlsx'",
]


def init(parser: ArgumentParser):
    parser.add_argument('-a', '--app', type=int, help='Application ID')
    parser.add_argument(
        '-g', '--group', type=int, nargs='+', help='Group ID or a list of IDs'
    )
    parser.add_argument(
        '-f',
        '--filename',
        help='Filename for destination json file (print if no filename given)'
    )
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--query')
    parser.add_argument('--columns')
    parser.add_argument(
        '--printcolumns',
        action='store_true',
        help='Print the columns that would be exported'
    )
    parser.add_argument(
        '--relationlevel',
        type=int,
        choices=list(map(lambda key: RELATION_LEVELS[key], RELATION_LEVELS.keys())),
        default=0,
        help="\n".join(
            [
                'Export relation properties in the excel too',
                'If no option is given there will be no relations',
                'The possible options are:',
                *list(
                    map(
                        lambda key: f'{RELATION_LEVELS[key]} for {key}',
                        RELATION_LEVELS.keys()
                    )
                )
            ]
        )
    )
    parser.add_argument('--appviewid', type=int, help='Application View ID')
    parser.add_argument(
        '--limitresults', type=int, help='Total Results Limit', default=0
    )


def main(
    url: str,
    session_id: str,
    group: list[int],
    app: int,
    filename: str,
    appviewid: str,
    query: str,
    columns: str,
    force: bool,
    printcolumns: bool,
    limitresults: int,
    relationlevel: int,
    **kwargs,
):
    app_view = get_app_view(url, session_id, appviewid)
    app_id = app if not app_view else app_view.get('app')
    group_list = get_group_list_from_appview_if_empty(group, app_view)
    app_view_properties = get_io_properties_from_appview_columns(app_view)

    if not app_id:
        print('App not found!')
        raise SystemExit(1)

    embedded_def = [
        'io_type',
    ]
    source_override = [
        'id',
        'io_type',
        'modified',
        'properties',
        'created',
        'tags',
        'state',
        'group',
        'title',
    ]

    if relationlevel > RELATION_LEVELS['NO_RELATIONS']:
        embedded_def.append('related_ios')
        source_override.append('relations')

    search_params = get_app_view_io_search_params(
        url=url,
        session_id=session_id,
        group=group_list,
        app=app,
        query=query,
        field_query_extra={},
        source_override=source_override,
        embedded=embedded_def,
        search_once=printcolumns,
        app_view=app_view,
        total_limit=limitresults,
    )
    search_response = io_search(**search_params)

    if printcolumns:
        columns_to_export = get_columns_from_search_response(
            app_id,
            search_response,
            columns,
            relationlevel,
            app_view_properties,
            search_params
        )

        print("The following columns will be exported in the given order:")
        print(',\n'.join(columns_to_export))
        print(f"Columns count: {len(columns_to_export)}")
    else:
        filename = get_export_filename(
            group_list,
            app_id,
            'xlsx',
            filename,
            force,
        )

        build_excel_for_search_response(
            main_app_id=app_id,
            search_response=search_response,
            filename=filename,
            columns=columns,
            relation_level=relationlevel,
            app_view_properties=app_view_properties,
            search_params=search_params,
        )
