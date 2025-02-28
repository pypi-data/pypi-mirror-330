[![PyPi](https://img.shields.io/pypi/v/warc-cache?style=flat-square)](https://pypi.org/project/warc-cache/)
[![CI](https://img.shields.io/github/actions/workflow/status/janheinrichmerker/warc-cache/ci.yml?branch=main&style=flat-square)](https://github.com/janheinrichmerker/warc-cache/actions/workflows/ci.yml)
[![Code coverage](https://img.shields.io/codecov/c/github/janheinrichmerker/warc-cache?style=flat-square)](https://codecov.io/github/janheinrichmerker/warc-cache/)
[![Python](https://img.shields.io/pypi/pyversions/warc-cache?style=flat-square)](https://pypi.org/project/warc-cache/)
[![Issues](https://img.shields.io/github/issues/janheinrichmerker/warc-cache?style=flat-square)](https://github.com/janheinrichmerker/warc-cache/issues)
[![Commit activity](https://img.shields.io/github/commit-activity/m/janheinrichmerker/warc-cache?style=flat-square)](https://github.com/janheinrichmerker/warc-cache/commits)
[![Downloads](https://img.shields.io/pypi/dm/warc-cache?style=flat-square)](https://pypi.org/project/warc-cache/)
[![License](https://img.shields.io/github/license/janheinrichmerker/warc-cache?style=flat-square)](LICENSE)

# 💾 warc-cache

Easy WARC records disk cache.

## Installation

Install the package from PyPI:

```shell
pip install warc-cache
```

## Usage

TODO

## Development

To build this package and contribute to its development you need to install the `build`, and `setuptools` and `wheel` packages:

```shell
pip install build setuptools wheel
```

(On most systems, these packages are already pre-installed.)

Then, install the package and test dependencies:

```shell
pip install -e .[tests]
```

You can now verify your changes against the test suite.

```shell
ruff check .                   # Code format and LINT
mypy .                         # Static typing
bandit -c pyproject.toml -r .  # Security
pytest .                       # Unit tests
```

Please also add tests for your newly developed code.

### Build wheels

Wheels for this package can be built with:

```shell
python -m build
```

## Support

If you hit any problems using this package, please file an [issue](https://github.com/janheinrichmerker/warc-cache/issues/new).
We're happy to help!

## License

This repository is released under the [MIT license](LICENSE).
