# Python Charmers meta-package

This is a meta-package for [Python Charmers](https://pythoncharmers.com)
training participants. This depends on many packages used in Python Charmers
training courses.

This package is intended to be used from a Python Charmers Hub in the cloud
like https://cpuhub.pythoncharmers.com.

## Installation

Install it like this:

```
pip install pythoncharmers-meta
```

or, if you have [uv](https://docs.astral.sh/uv/), this will be much faster:

```
uv pip install pythoncharmers-meta
```

## Optional packages (extras)

The following sets of optional packages ("extras") are available:

- `gis`
- `ml`
- `dl`
- `scieng`
- `net`
- `web`

You can add them like this:

```
uv pip install "pythoncharmers-meta[gis, ml]" --reinstall
```

## Cutting a new release

```
uv build
uvx twine upload dist/*
```
