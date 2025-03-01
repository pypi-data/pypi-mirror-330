import os
import datetime


def get_export_filename(
    group: int | list[int],
    app: int,
    suffix: str,
    filename: str | None = None,
    prefix='out',
    force: bool = False
) -> str:
    group = [group] if isinstance(group, int) else group

    if not filename:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f'{prefix}__g_{",".join([str(g) for g in group]) if group else "ALLGROUPS"}__a_{app}_{today}.{suffix}'

    if filename and os.path.exists(filename) and not force:
        raise Exception(f'File exists {filename}')

    print(f'Output filename is {filename}')

    return filename
