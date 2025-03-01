# simple-build

A simple build-backend for Python.

The package implements the build backend interface,
defined in <https://peps.python.org/pep-0517>,
and <https://peps.python.org/pep-0660>.

It is very similar to [flit](https://flit.readthedocs.io/) and [hatch](https://hatch.pypa.io/latest/config/build/#build-system),
but it has one key additional feature I required: [pre-write hooks](#pre-write-hooks).
This is bit similar to [hatch's build hook](https://hatch.pypa.io/latest/plugins/build-hook/reference/#hatchling.builders.hooks.plugin.interface.BuildHookInterface),
but offers a lot more freedom to modify the packaged files.

## Usage

Simply add the following to your `pyproject.toml`:

```toml
[build-system]
requires = ["simple-build"]
build-backend = "simple_build.backend"
```

## Features

### modules in `src` folder

The module will be found by the project name (normalising `-` to `_`),
and supports packages in the common `src` folder layout, or at the root of the package.

```toml
[project]
name = "my-project"
```

```plaintext
pyproject.toml
src/
    my_project/
        __init__.py
```

### Dynamic project metadata

The following fields can be set as dynamic values:

```toml
[project]
dynamic = ["version", "description", "authors"]
```

The values are then read from the root file of the package (`__init__.py` or the single module file):

```python
"""My project description."""
__version__ = "0.1.0"
__author__ = "John Doe"
__email__ = "johndoe@email.com"
```

### Git integration

By default the packaging will respect the `.gitignore` file, and exclude all files listed in it.

You can also configure this in the `pyproject.toml`:

```toml
[tool.build.sdist]
use_git = true
include = ["my_file.txt", ...]
exclude = ["my_file.txt", ...]
```

### pre-write hooks

In your `pyproject.toml` you can define a list of hooks that can modify the files before they are written to the sdist or wheel:

```toml
[tool.build]
pre_write_hooks = ["my_hook.py"]
```

A hook file should contain a function with the following signature:

```python
from pathlib import Path
from typing import Literal
from simple_build.analyse import PackageAnalysis

def pre_write_hook(
    type: Literal["sdist", "wheel"], src: Path, module: str | None, analysis: PackageAnalysis
) -> None:
    """A pre-write hook, to modify files before writing them to the sdist or wheel.

    :param path: The path to the temporary folder containing the files that will be written to the sdist/wheel.
        This can be modified in place, including deleting files and adding new ones.
    :param module: The name of the module.
    :param package: The package analysis.
    """
```
