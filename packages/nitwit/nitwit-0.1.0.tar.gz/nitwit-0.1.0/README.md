
# nitwit

tools for converting git repository data into data tables

## Table Schemas

#### `commits`

```
- hash: String
- author: String
- email: String
- timestamp: DateTime('ms')
- message: String
- parents: String
- committer: String
- committer_email: String
- commit_timestamp: DateTime('ms')
- tree_hash: String
- repo: String
```

#### `authors`

```
- name: String
- email: String
- n_commits: Int64
- n_changed_files: Int64
- insertions: Int64
- deletions: Int64
- first_commit_timestamp: DateTime('ms')
- last_commit_timestamp: DateTime('ms')
- n_repos: Int64
```

#### `file_diffs`

```
- hash: String
- insertions: Int64
- deletions: Int64
- path: String
- repo: String
```

#### repos

```
- repo: String
- n_files: Int64
- n_commits: Int64
- n_authors: Int64
- first_commit_timestamp: DateTime('ms')
- last_commit_timestamp: DateTime('ms')
```


## Command Line Interface

```bash
# generate commits.parquet
nitwit commits [OUTPUT_PATH]

# generate authors.parquet
nitwit authors [OUTPUT_PATH]

# generate files.parquet
nitwit file_diffs [OUTPUT_PATH]
```


## Python Interface

```python
# specify repo(s), using path(s) or url(s)
repo = '/path/to/git/repo'
repo = 'https://github.com/author_name/repo_name'
repo = [
    '/path/to/git/repo1',
    '/path/to/git/repo2',
    'https://github.com/author_name1/repo_name2',
    'https://github.com/author_name1/repo_name2',
]

commits = nitwit.commits(repo)
authors = nitwit.authors(repo)
file_diffs = nitwit.file_diffs(repo)
```
