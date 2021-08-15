![daeclipse Project Banner](assets/banner.png "daeclipse Project Banner")

[![PyPI](https://img.shields.io/pypi/v/daeclipse)](https://pypi.org/project/daeclipse/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/daeclipse)](https://pypi.org/project/daeclipse/) [![codecov](https://codecov.io/gh/Pepper-Wood/daeclipse/branch/main/graph/badge.svg?token=6HRQ3Y58TS)](https://codecov.io/gh/Pepper-Wood/daeclipse) [![PyPI - License](https://img.shields.io/pypi/l/daeclipse)](https://github.com/Pepper-Wood/daeclipse/blob/main/LICENSE)

[daeclipse](https://pypi.org/project/daeclipse/) is a reverse-engineered Python library for DeviantArt Eclipse functionality.

Also check out [daeclipse-cli](https://github.com/Pepper-Wood/daeclipse-cli), a handy CLI to bundle `daeclipse` capabilities.

## Installation

The Python library is available via https://pypi.org/project/daeclipse/

```bash
pip install daeclipse
```

## Usage

```py
import daeclipse

# Fetches a list of group names the user is a member of.
# You will need to be logged into DeviantArt and have a chrome page open.
eclipse = daeclipse.Eclipse()
groups, has_more, next_offset, total = eclipse.get_groups("Pepper-Wood", 0)
for group in groups:
    print(group.username)
```

For more examples, see the [code snippets within the daeclipse-cli commands](https://github.com/Pepper-Wood/daeclipse-cli/tree/main/daeclipse_cli/commands).

## Python Package Reference

For reference on the [daeclipse python package](https://pypi.org/project/daeclipse/) implementation, see the [PDoc-generated documentation](https://www.kathryndipippo.com/daeclipse/python).

## API Reference

For the crowd-sourced, unofficial OpenAPI spec for the DeviantArt Eclipse API, see the [ReDoc-generated documentation](https://www.kathryndipippo.com/daeclipse/api).
