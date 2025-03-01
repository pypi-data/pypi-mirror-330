# stactools-global-mangrove-watch

[![PyPI](https://img.shields.io/pypi/v/stactools-global-mangrove-watch?style=for-the-badge)](https://pypi.org/project/stactools-global-mangrove-watch/)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/stactools-packages/global-mangrove-watch/continuous-integration.yml?style=for-the-badge)

- Name: global-mangrove-watch
- Package: `stactools.global_mangrove_watch`
- [stactools-global-mangrove-watch on PyPI](https://pypi.org/project/stactools-global-mangrove-watch/)
- Owner: @hrodmn
- [Dataset homepage](https://zenodo.org/records/6894273)
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
  - [version](https://github.com/stac-extensions/version/)
  - [scientific](https://github.com/stac-extensions/scientific/)
  - [render](https://github.com/stac-extensions/render/)
- [Browse the example in human-readable form](https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/stactools-packages/global-mangrove-watch/main/examples/collection.json)
- [Browse a notebook demonstrating the example item and collection](https://github.com/stactools-packages/global-mangrove-watch/tree/main/docs/example.ipynb)

This package can be used to generate STAC metadata for the [Global Mangrove Watch Dataset](https://zenodo.org/records/6894273).

## Details

- It is assumed that the raw files have been downloaded from the source and unzipped in a persistent storage location in order to provide proper `hrefs` for the STAC assets.
- Each item represents a particular year (1996, 2007, 2008, etc) with assets for the annual mangrove mask raster (`cog`) and the 1996-`{year}` change raster (`change_cog`).
  - The vector files are not yet added as assets

## STAC examples

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

## Installation

```shell
pip install stactools-global-mangrove-watch
```

## Command-line usage

Create a collection json:

```shell
stac global-mangrove-watch create-collection {destination}
```

Create an item json:

```shell
stac global-mangrove-watch create-item {cog_asset_href} {destination}
```

Use `stac global-mangrove-watch --help` to see all subcommands and options.

## Contributing

We use [pre-commit](https://pre-commit.com/) to check any changes.
To set up your development environment:

```shell
uv sync
uv run pre-commit install
```

To check all files:

```shell
uv run pre-commit run --all-files
```

To run the tests:

```shell
uv run pytest -vv
```

If you've updated the STAC metadata output, update the examples:

```shell
uv run scripts/update-examples
```
