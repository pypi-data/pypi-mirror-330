from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import aiohttp

from . import github_endpoints
from . import github_cache


async def async_get_github_data(
    refs: dict[str, str] | list[dict[str, str]],
    datatype: str,
    github_token: str,
) -> list[dict[str, typing.Any]]:
    import asyncio
    import aiohttp

    if isinstance(refs, dict):
        refs = [refs]

    async with aiohttp.ClientSession() as session:
        coroutines = []
        for ref in refs:
            if github_cache.has_local_github_data(ref=ref, datatype=datatype):
                coroutine = github_cache._async_load_local_github_data(
                    ref=ref,
                    datatype=datatype,
                )
            else:
                coroutine = _async_github_request(
                    ref=ref,
                    datatype=datatype,
                    session=session,
                    github_token=github_token,
                )
            coroutines.append(coroutine)
        return await asyncio.gather(*coroutines)


async def _async_github_request(
    ref: dict[str, str],
    datatype: str,
    session: aiohttp.ClientSession,
    github_token: str,
) -> dict[str, typing.Any]:
    url = github_endpoints.get_endpoint_url(datatype).format(**ref)
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token ' + github_token,
    }
    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            raise Exception(
                'HTTP error ' + str(response.status) + ':' + str(response.text)
            )
        result: dict[str, typing.Any] = await response.json()
        await github_cache._async_save_local_github_data(
            data=result, ref=ref, datatype=datatype
        )
        return result
