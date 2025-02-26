from __future__ import annotations

import typing

if typing:
    import polars as pl

from .. import sources
from . import file_diffs


def collect_commits(
    repo: str | list[str],
    include_file_stats: bool = False,
    _extra_log_args: list[str] | None = None,
    n_processes: int = 16,
) -> pl.DataFrame:
    import multiprocessing

    if isinstance(repo, str):
        raw_repos = [repo]
    else:
        raw_repos = repo
    repos = sources.resolve_repo_references(raw_repos)

    with multiprocessing.get_context('spawn').Pool(
        processes=n_processes
    ) as pool:
        tasks = [
            (raw_source, source, include_file_stats, _extra_log_args)
            for raw_source, source in zip(raw_repos, repos)
        ]
        pieces = pool.map(_process_repo, tasks)
    pool.close()
    pool.join()

    return pl.concat(pieces)


def _process_repo(
    args: tuple[str, str, bool, list[str] | None],
) -> pl.DataFrame:
    raw_source, source, include_file_stats, extra_log_args = args
    commits = _collect_commit_basics(source, extra_log_args)

    if include_file_stats:
        stats = file_diffs.collect_file_diffs(source)
        stats = stats.group_by('hash').agg(
            n_changed_files=pl.len(),
            insertions=pl.col.insertions.sum(),
            deletions=pl.col.deletions.sum(),
        )
        commits = commits.join(stats, on='hash', how='left')

    return sources.add_repo_columns(commits, source)


def _collect_commit_basics(
    repo: str, _extra_log_args: list[str] | None
) -> pl.DataFrame:
    import io
    import subprocess
    import polars as pl

    schema = {
        'hash': pl.String,
        'author': pl.String,
        'email': pl.String,
        'timestamp': pl.Int64,
        'message': pl.String,
        'parents': pl.String,
        'committer': pl.String,
        'committer_email': pl.String,
        'commit_timestamp': pl.Int64,
        'tree_hash': pl.String,
    }
    datetime = pl.Datetime('ms', time_zone='UTC')

    COMMIT_SEP = '\u001e'
    SEP = '\u001f'

    cmd = [
        'git',
        '-C',
        repo,
        'log',
        '--all',
        '--format='
        + COMMIT_SEP
        + '"%H|%an|%ae|%at|%s|%P|%cn|%ce|%ct|%T"'.replace('|', SEP),
        '--no-abbrev-commit',
    ]
    if _extra_log_args is not None:
        cmd.extend(_extra_log_args)
    output = subprocess.check_output(cmd, universal_newlines=True)

    if output == '':
        return pl.DataFrame(schema=schema).with_columns(
            is_merge=pl.lit(False),
            timestamp=(pl.col.timestamp * 1000).cast(datetime),
            commit_timestamp=(pl.col.commit_timestamp * 1000).cast(datetime),
        )

    commits = output.split(COMMIT_SEP)[1:]
    cleaned = '\n'.join(commit.replace('\n', ' ') for commit in commits)

    df = pl.read_csv(
        io.StringIO(cleaned),
        schema=schema,
        has_header=False,
        separator=SEP,
        quote_char=None,
        truncate_ragged_lines=False,
    )

    df = df.with_columns(is_merge=pl.col.parents.str.contains(' '))

    df = df.with_columns(
        timestamp=(pl.col.timestamp * 1000).cast(datetime),
        commit_timestamp=(pl.col.commit_timestamp * 1000).cast(datetime),
    )

    return df
