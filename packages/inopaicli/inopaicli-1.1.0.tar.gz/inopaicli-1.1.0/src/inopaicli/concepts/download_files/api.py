import aiohttp


async def do_file_req_async(url, cookies):
    """Performs an asynchronous file request."""
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.read()
