from stactools.global_mangrove_watch import constants, stac

from . import test_data


def test_create_collection() -> None:
    # This function should be updated to exercise the attributes of interest on
    # the collection

    collection = stac.create_collection()
    collection.set_self_href(None)  # required for validation to pass
    assert collection.id == constants.COLLECTION_ID
    collection.validate()


def test_create_item() -> None:
    # This function should be updated to exercise the attributes of interest on
    # a typical item

    item = stac.create_item(test_data.get_path("data/GMW_N26W082_2020_v3.tif"))
    assert item.id == "GMW_N26W082_2020_v3"
    assert item.bbox == (-82.0, 25.0, -81.0, 26.0)  # type: ignore
    assert item.ext.proj.shape == constants.ITEM_SHAPE
    item.validate()
