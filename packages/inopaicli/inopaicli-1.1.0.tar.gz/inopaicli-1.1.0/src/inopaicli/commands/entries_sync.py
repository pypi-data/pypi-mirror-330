import os
import json
import time
from argparse import ArgumentParser
from inopaicli.concepts.io.functions import import_ios
from inopaicli.core.api import calculate_end
from inopaicli.core.arguments import add_use_action_id
from inopaicli.core.file import read_csv_file, read_json_file

DESCRIPTION = "Synchronize ios from id in json/csv file"
EXAMPLES = [
    "inopaicli entries_sync -a 1 -g 1 -p fdjshk -f FILENAME",
]


def init(parser: ArgumentParser):
    add_use_action_id(parser)
    parser.add_argument("-g", "--group", type=int, help="Group ID", required=True)
    parser.add_argument(
        "-f",
        "--filename",
        help="Filename for spare part input data json/csv file",
        required=True,
    )
    parser.add_argument(
        "-p_name", "--property_name", type=str, help="Property name", required=False
    )
    parser.add_argument("-c", "--chunk_size", type=int, default=1000, required=False)
    parser.add_argument("--prevent_io_create", action="store_true")
    parser.add_argument("--prevent_io_update", action="store_true")
    parser.add_argument(
        "--user_forces_skip_actions",
        help="User forces skip actions",
        nargs="+",
        required=False,
    )


def get_entries(filename):
    if not os.path.exists(filename):
        raise ValueError(f"File does not exist {filename}")
    if filename.endswith(".json"):
        return read_json_file(filename)
    elif filename.endswith(".csv"):
        return read_csv_file(filename)
    raise ValueError(f"Unsupported file type {filename}")


def main(
    url: str,
    session_id: str,
    app: int,
    group: int,
    property_name: str,
    filename: str = None,
    importdataentries=None,
    debug=False,
    chunk_size=1000,
    prevent_io_create=False,
    prevent_io_update=False,
    user_forces_skip_actions=None,
    # **kwargs,
):
    if importdataentries is None:
        importdataentries = get_entries(filename)
    if hasattr(importdataentries, "write_json"):
        # print("Assuming importdataentries is a polars DataFrame")
        importdataentries = json.loads(
            importdataentries.write_json(
                # row_oriented=True,
            )
        )

    chunk_count = (
        (len(importdataentries) // chunk_size) if chunk_size != 0 else 1
    ) or 1
    # print("chunk_count", chunk_count, "chunk_size", chunk_size)
    rest = len(importdataentries) % (chunk_count * chunk_size)
    start_time = time.time()
    print("Splitting input file in", chunk_count, "chunks")

    for i in range(0, chunk_count):
        # print(i)
        start = i * chunk_size
        end = calculate_end(
            chunk_count=chunk_count, chunk_size=chunk_size, rest=rest, i=i
        )
        # print("start", start, "end", end, "-> +1", end + 1)
        importentrieschunk = importdataentries[start : (end + 1)]
        respdata = import_ios(
            url=url,
            session_id=session_id,
            app=app,
            group=group,
            property_name=property_name,
            ios=importentrieschunk,
            prevent_io_create=prevent_io_create,
            prevent_io_update=prevent_io_update,
            debug=debug,
            user_forces_skip_actions=user_forces_skip_actions,
        )
        updated = f"{respdata['updated']}"
        created = f"{respdata['created']}"
        unchanged = f"{respdata['unchanged']}"
        took = time.time() - start_time
        estimatedtimeleft = (chunk_count - i) * took
        print(
            f"Chunk {i:>2}/{chunk_count} took {took:>6.3f}s: updated:{updated:>4} created:{created:>4} unchanged:{unchanged:>4} (estimated time left {estimatedtimeleft:>7.2f}s)",
        )
        start_time = time.time()
