from __future__ import annotations


def get_endpoint_url(datatype: str) -> str:
    return {
        'repo': 'https://api.github.com/repos/{owner}/{name}',
        'user': 'https://api.github.com/users/{username}',
    }[datatype]


def get_endpoint_path_keys(datatype: str) -> list[str]:
    return {
        'repo': ['github_repos', 'metadata', '{owner}', '{name}'],
        'user': ['github_users', 'metadata', '{username}'],
    }[datatype]
