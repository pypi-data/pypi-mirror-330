from __future__ import annotations

import typing

from . import github_requests
from .. import references


async def async_get_github_repos_metadata(
    repo: str | list[str],
    github_token: str,
) -> list[dict[str, typing.Any]]:
    if isinstance(repo, str):
        repo = [repo]
    return await github_requests.async_get_github_data(
        [references.parse_repo_reference(ref) for ref in repo],
        datatype='repo',
        github_token=github_token,
    )


async def async_get_github_users_metadata(
    username: str | list[str], github_token: str
) -> list[dict[str, typing.Any]]:
    if isinstance(username, str):
        username = [username]
    return await github_requests.async_get_github_data(
        [{'username': value} for value in username],
        datatype='user',
        github_token=github_token,
    )
