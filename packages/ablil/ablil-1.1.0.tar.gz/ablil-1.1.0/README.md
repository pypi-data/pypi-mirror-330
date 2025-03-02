# Python starter with Poetry

This is a ready to use starter for Python packages, clone it and make sure to update:

* pyproject.toml
* README.md

## Develop locally

Start a new virtual env
```shell
poetry shell
```

Install all dependencies (declared on pyproject.toml) from all groups
```shell
poetry install

# only main group
poetry install --only main

# without test group
poetry install --without test
```

Add new dependency
```shell
# add dep to main group
poetry add requests

# add dep to dev group
poetry add black --group dev

# add dep to test group
poetry add pytest --group test
```

## Build and publish

Build package
```shell
poetry build
```

Publish package
```shell
poetry publish
```

Authenticate to PyPI
```shell
poetry config pypi-token.pypi $PYPI_TOKEN
```


# Referencs

[Guide to Python module](https://docs.python.org/3/tutorial/modules.htmldir)
[Python packaging user guide](https://packaging.python.org/en/latest/)