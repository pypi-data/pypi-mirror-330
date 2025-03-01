import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import rasterio.transform
import semver
from pystac import (
    Collection,
    Extent,
    Item,
    ItemAssetDefinition,
    Link,
    MediaType,
    Provider,
    ProviderRole,
    RelType,
    SpatialExtent,
    TemporalExtent,
    get_stac_version,
)
from pystac.extensions.classification import (
    Classification,
    ItemAssetsClassificationExtension,
)
from pystac.extensions.render import Render, RenderExtension
from pystac.extensions.scientific import Publication
from shapely.geometry import box, mapping

from stactools.global_mangrove_watch.constants import (
    CHANGE_ASSET_NAME,
    COG_ASSET_NAME,
    COLLECTION_ID,
    DATASET_CITATION,
    DATASET_DOI,
    DESCRIPTION,
    EPSG,
    ITEM_SHAPE,
    KEYWORDS,
    PUBLICATION_CITATION,
    PUBLICATION_DOI,
    TITLE,
    VERSION,
)


def format_multiline_string(string: str) -> str:
    """Format a multi-line string for use in metadata fields"""
    return re.sub(r" +", " ", re.sub(r"(?<!\n)\n(?!\n)", " ", string))


def parse_gmw_filename(cog_basename: str) -> Dict[str, Any] | None:
    """Parse a Global Mangrove Watch COG asset filename"""
    pattern = r"GMW_([NS]\d+)([EW]\d+)_(\d{4})_v(\d+)\.tif"
    match = re.match(pattern, cog_basename)

    if match:
        lat_str, lon_str, year, version = match.groups()

        lat_direction = lat_str[0]
        lat_value = float(lat_str[1:])
        latitude = lat_value if lat_direction == "N" else -lat_value

        lon_direction = lon_str[0]
        lon_value = float(lon_str[1:])
        longitude = lon_value if lon_direction == "E" else -lon_value
        bbox = (longitude, latitude - 1, longitude + 1, latitude)
        return {
            "datetime": datetime(year=int(year), month=12, day=31, tzinfo=timezone.utc),
            "version": int(version),
            "bbox": bbox,
            "geometry": mapping(box(*bbox)),
        }
    else:
        return None


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return "{:02x}{:02x}{:02x}".format(r, g, b)


ITEM_ASSETS = {
    COG_ASSET_NAME: ItemAssetDefinition.create(
        title="Mangrove cover",
        description="Gridded estimate of mangrove cover",
        media_type=MediaType.COG.value,
        roles=["data"],
    ),
    CHANGE_ASSET_NAME: ItemAssetDefinition.create(
        title="Mangrove cover change since 1996",
        description="Gridded estimate of mangrove cover change since 1996",
        media_type=MediaType.COG.value,
        roles=["data"],
    ),
}

# RGB values from the color table in the COGs
COLOR_HINTS = {
    COG_ASSET_NAME: {
        1: (0, 150, 0),
    },
    CHANGE_ASSET_NAME: {
        1: (255, 0, 0),
        2: (0, 0, 255),
    },
}


def create_collection() -> Collection:
    """Creates a STAC Collection.

    Returns:
        Collection: STAC Collection object
    """
    extent = Extent(
        SpatialExtent([[-180.0, -90.0, 180.0, 90.0]]),
        TemporalExtent(
            [
                [
                    datetime(1996, 1, 1, tzinfo=timezone.utc),
                    datetime(2020, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
                ]
            ]
        ),
    )

    collection = Collection(
        id=COLLECTION_ID,
        title=TITLE,
        description=format_multiline_string(DESCRIPTION),
        keywords=KEYWORDS,
        extent=extent,
        license="CC-BY-4.0",
        providers=[
            Provider(
                name="Zenodo",
                url="https://zenodo.org/records/6894273",
                roles=[
                    ProviderRole.HOST,
                ],
            ),
            Provider(
                name="Global Mangrove Watch",
                url="https://www.globalmangrovewatch.org/",
                roles=[
                    ProviderRole.PRODUCER,
                    ProviderRole.LICENSOR,
                ],
            ),
        ],
    )

    collection.add_link(
        Link(
            rel=RelType.LICENSE,
            target="https://creativecommons.org/licenses/by/4.0/",
            media_type=MediaType.HTML,
            title="CC-BY-4.0 license",
        ),
    )

    collection.item_assets = ITEM_ASSETS

    # classification values
    cog_classification = ItemAssetsClassificationExtension(
        collection.item_assets[COG_ASSET_NAME]
    )
    cog_classification.classes = [
        Classification.create(
            value=0,
            description="nodata",
            nodata=True,
            name="nodata",
        ),
        Classification.create(
            value=1,
            description="mangrove",
            name="mangrove",
            color_hint=rgb_to_hex(*COLOR_HINTS[COG_ASSET_NAME][1]),
        ),
    ]

    change_classification = ItemAssetsClassificationExtension(
        collection.item_assets[CHANGE_ASSET_NAME]
    )
    change_classification.classes = [
        Classification.create(
            value=0,
            description="nodata",
            nodata=True,
            name="nodata",
        ),
        Classification.create(
            value=1,
            description="mangrove gained",
            name="mangrove-gained",
            color_hint=rgb_to_hex(*COLOR_HINTS[CHANGE_ASSET_NAME][1]),
        ),
        Classification.create(
            value=2,
            description="mangrove lost",
            name="mangrove-lost",
            color_hint=rgb_to_hex(*COLOR_HINTS[CHANGE_ASSET_NAME][2]),
        ),
    ]

    collection.ext.add("version")
    collection.ext.version.version = VERSION

    collection.ext.add("sci")
    collection.ext.sci.doi = DATASET_DOI
    collection.ext.sci.citation = format_multiline_string(DATASET_CITATION)
    collection.ext.sci.publications = [
        Publication(
            doi=PUBLICATION_DOI,
            citation=format_multiline_string(PUBLICATION_CITATION),
        )
    ]

    # if using STAC v1.0.0, add raster and item-assets extensions
    if semver.Version.parse(get_stac_version()) <= semver.Version.parse("1.0.0"):
        collection.ext.add("raster")
        collection.ext.add("item_assets")

    # add render extension
    collection.ext.add("render")
    renders = {
        "mangroves": Render.create(
            assets=[COG_ASSET_NAME],
            colormap={
                str(value): rgb for value, rgb in COLOR_HINTS[COG_ASSET_NAME].items()
            },
        ),
        "change": Render.create(
            assets=[CHANGE_ASSET_NAME],
            colormap={
                str(value): rgb for value, rgb in COLOR_HINTS[CHANGE_ASSET_NAME].items()
            },
        ),
    }

    RenderExtension.ext(collection).apply(renders)

    return collection


def create_item(
    cog_asset_href: str,
    change_asset_href: Optional[str] = None,
    vector_asset_href: Optional[str] = None,
    change_vector_asset_href: Optional[str] = None,
) -> Item:
    """Creates a STAC item from a asset href.

    NOTE: The vector files will not be added as assets but the args are included as
        placeholders for future support.

    Args:
        cog_asset_href (str): The HREF pointing to the COG asset associated with the
            item
        change_asset_href (str): Optional, The HREF pointing to the mangrove change COG
            asset associated with the item
        vector_asset_href (str): Optional, the HREF pointing to the vector file
            associated with the item
        change_vector_asset_href (str): Optional, the HREF pointing to the mangrove
            change vector file associated with the item

    Returns:
        Item: STAC Item object
    """
    cog_basename = os.path.basename(cog_asset_href)
    item_attributes = parse_gmw_filename(cog_basename)

    if not item_attributes:
        raise ValueError(f"could not parse item properties from {cog_asset_href}")

    assets = {
        asset_key: ITEM_ASSETS[asset_key].create_asset(href=asset_href)
        for asset_key, asset_href in zip(
            [COG_ASSET_NAME, CHANGE_ASSET_NAME], [cog_asset_href, change_asset_href]
        )
        if asset_href
    }

    item = Item(
        id=cog_basename.replace(".tif", ""),
        bbox=item_attributes["bbox"],
        geometry=item_attributes["geometry"],
        datetime=item_attributes["datetime"],
        assets=assets,
        properties={},
    )
    item.ext.add("proj")
    item.ext.proj.apply(
        epsg=EPSG,
        geometry=item_attributes["geometry"],
        bbox=item_attributes["bbox"],
        shape=ITEM_SHAPE,
        transform=rasterio.transform.from_bounds(*item_attributes["bbox"], *ITEM_SHAPE),
    )

    # ensure proj:epsg gets set (pystac bug)
    item.properties["proj:epsg"] = EPSG

    # we need to stick with projection extension <v2.0 in order to maintain
    # compatibility with the STACIT driver in older GDAL versions
    extensions = ["https://stac-extensions.github.io/projection/v1.2.0/schema.json"]
    extensions.extend(
        (
            e
            for e in item.stac_extensions
            if not e.startswith("https://stac-extensions.github.io/projection")
        )
    )
    item.stac_extensions = extensions

    assert isinstance(item, Item)

    return item
