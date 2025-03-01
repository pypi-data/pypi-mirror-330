import os
import asyncio
import zipfile
from pathlib import Path
from typing import List
from inopaicli.core.auth import build_url
from inopaicli.concepts.download_files.api import do_file_req_async


def get_file_urls(url: str, search_response: List[dict], group_id: int, group_name: str) -> List[dict]:
    urls = []
    for response_item in search_response:
        source = response_item.get("_source")
        if not source:
            continue
        properties = source.get('properties')
        if not properties:
            continue
        file_property = properties.get('file')
        if not file_property:
            continue

        urls.append(
            {
                "url": build_url(url, file_property['url']),
                "group_id": group_id,
                "group_name": group_name,
                "file_id": source['id'],
                "file_name": file_property['name'],
            }
        )
    return urls


async def download_file_async(file_meta, cookies, file_count, total_count, debug=False):
    """
    Downloads a single file asynchronously.

    Args:
        file_meta (dict): File metadata including URL, group info, and name.
        cookies (dict): Cookies for the request.
        file_count (int): Current file count.
        total_count (int): Total number of files.
        debug (bool): Whether to print debug information.

    Returns:
        str: Path to the downloaded file.
    """
    try:
        group_dir = os.path.join('data', 'download_files', f"{file_meta['group_id']}_{file_meta['group_name']}")
        os.makedirs(group_dir, exist_ok=True)

        # Construct file path
        file_name = file_meta["file_name"]
        file_path = os.path.join(group_dir, file_name)

        # Skip download if file already exists
        if os.path.exists(file_path):
            if debug:
                print(f"Skipped ({file_count + 1}/{total_count}): {file_path}")
            return file_path

        # Perform asynchronous file request
        file_content = await do_file_req_async(file_meta["url"], cookies)

        # Save file locally
        with open(file_path, "wb") as file:
            file.write(file_content)

        print(f"Downloaded ({file_count + 1}/{total_count}): {file_path}")
        return file_path

    except Exception as e:
        print(f"Failed to download {file_meta['url']}: {e}")
        return None


async def download_files_in_batches(batch_size, tasks):
    """
    Processes download tasks in batches.

    Args:
        batch_size (int): Number of simultaneous downloads.
        tasks (list of coroutine): Download tasks to process.

    Returns:
        list: Results of completed tasks.
    """
    semaphore = asyncio.Semaphore(batch_size)

    async def limited_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(limited_task(task) for task in tasks))


async def download_files_and_zip_async(
    file_metas: List[dict],
    cookies: dict,
    zip_flag=False,
    batch_size=5,
    debug=False,
):
    """
    Downloads files asynchronously and optionally zips them.

    Args:
        file_metas (List[dict]): List of file metadata for download.
        filename (str): Name of the zip file.
        cookies (dict): Cookies for requests.
        zip_flag (bool): Whether to create zip files per group.
        batch_size (int): Number of simultaneous downloads.
        debug (bool): Whether to print debug information.

    Returns:
        None
    """
    file_names = []
    for file_meta in file_metas:
        if file_meta["file_name"] in file_names:
            name, ext = os.path.splitext(file_meta["file_name"])
            file_meta["file_name"] = f"{name}_{file_meta['file_id']}{ext}"
            file_names.append(file_meta["file_name"])
        else:
            file_names.append(file_meta["file_name"])

    try:
        # Download files asynchronously
        total_count = len(file_metas)
        print(f"Downloading {total_count} files...")
        tasks = [
            download_file_async(file_meta, cookies, file_count, total_count, debug)
            for file_count, file_meta in enumerate(file_metas)
        ]
        downloaded_files = await download_files_in_batches(batch_size, tasks)

        # Filter out failed downloads
        downloaded_files = [f for f in downloaded_files if f]

        if zip_flag:
            # Group files by directory for zipping
            groups = {}
            for file_path in downloaded_files:
                group_dir = str(Path(file_path).parent)
                groups.setdefault(group_dir, []).append(file_path)

            # Create zip files for each group
            for group_dir, files in groups.items():
                zip_name = f"{Path(group_dir).name}.zip"
                zip_path = os.path.join("data", "download_files", zip_name)
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for file_path in files:
                        zipf.write(file_path, arcname=os.path.basename(file_path))
                print(f"Zipped: {zip_path}")

    except Exception as e:
        print(f"Error during download or zipping: {e}")
