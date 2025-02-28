# Kognic OpenLABEL

Python 3 library providing models and tools for OpenLABEL, the annotation format used in Kognic exports. 
This package is publicly available on [PyPi](https://pypi.org/project/kognic-openlabel/).

## Installation

To install the latest public version, run `pip install kognic-openlabel`.

For local development it is recommended to install locally with `pip install -e .` in the root folder.

## Documentation

The public documentation is hosted by the [public-docs](https://github.com/annotell/public-docs) repository and publicly 
available [here](https://docs.kognic.com/).

## Testing

You can install the test requirements with `pip install -r requirements-test.txt` and then run the tests with

```bash
pytest ./tests
```

## Releasing

Releasing new versions of the package is done by creating a git tag. This will trigger a GitHub action that will build
and publish the package to PyPi. The version number is determined by the git tag, so make sure to use the correct format
when creating a new tag. The format is `vX.Y.Z` where `X`, `Y` and `Z` are integers. To create a new tag and push it to
the remote repository, run the following commands

```bash
git tag vX.Y.Z; git push origin vX.Y.Z
```

**Important:** Don't forget to update the changelog with the new version number and a description of the changes before
releasing a new version. The changelog is located in the root folder and is named `CHANGELOG.md`.
