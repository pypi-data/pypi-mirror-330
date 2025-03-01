# MCAP Bag Parser

Parse MCAP rosbags into pandas dataframes

## Build and upload
Following instructions from https://packaging.python.org/en/latest/tutorials/packaging-projects/

To install build requirements
```commandline
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```

To build and upload to pypi, bump revision in `pyproject.toml`, then
```commandline
rm -rf dist
python3 -m build
python3 -m twine upload dist/*
```
