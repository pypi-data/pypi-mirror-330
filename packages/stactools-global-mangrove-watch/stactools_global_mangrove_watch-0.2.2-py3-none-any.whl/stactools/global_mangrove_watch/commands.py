import logging

import click
from click import Command, Group

from stactools.global_mangrove_watch import stac

logger = logging.getLogger(__name__)


def create_globalmangrovewatch_command(cli: Group) -> Command:
    """Creates the stactools-global-mangrove-watch command line utility."""

    @cli.group(
        "globalmangrovewatch",
        short_help=("Commands for working with stactools-global-mangrove-watch"),
    )
    def globalmangrovewatch() -> None:
        pass

    @globalmangrovewatch.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.argument("destination")
    def create_collection_command(destination: str) -> None:
        """Creates a STAC Collection

        Args:
            destination: An HREF for the Collection JSON
        """
        collection = stac.create_collection()
        collection.set_self_href(destination)
        collection.save_object()

    @globalmangrovewatch.command("create-item", short_help="Create a STAC item")
    @click.argument("source")
    @click.argument("destination")
    def create_item_command(source: str, destination: str) -> None:
        """Creates a STAC Item

        Args:
            source: HREF of the Asset associated with the Item
            destination: An HREF for the STAC Item
        """
        item = stac.create_item(source)
        item.save_object(dest_href=destination)

    return globalmangrovewatch
