from src.backpack_tf import BackpackTF, Listing

bptf = None
steam_id = "76561198253325712"


def test_initiate_backpack_tf(backpack_tf_token: str) -> None:
    global bptf
    bptf = BackpackTF(backpack_tf_token, steam_id)


def test_construct_listing_item() -> None:
    assert bptf._construct_listing_item("263;6") == {
        "baseName": "Ellis' Cap",
        "craftable": True,
        "quality": {"id": 6},
        "tradable": True,
    }


def test_construct_listing() -> None:
    assert bptf._construct_listing(
        "263;6",
        "sell",
        {"keys": 1, "metal": 1.55},
        "my description",
        13201231975,
    ) == {
        "buyout": True,
        "offers": True,
        "promoted": False,
        "item": {
            "baseName": "Ellis' Cap",
            "craftable": True,
            "quality": {"id": 6},
            "tradable": True,
        },
        "currencies": {"keys": 1, "metal": 1.55},
        "details": "my description",
        "id": 13201231975,
    }

    assert bptf._construct_listing(
        "263;6", "buy", {"keys": 1, "metal": 1.55}, "my description"
    ) == {
        "buyout": True,
        "offers": True,
        "promoted": False,
        "item": {
            "baseName": "Ellis' Cap",
            "craftable": True,
            "quality": {"id": 6},
            "tradable": True,
        },
        "currencies": {"keys": 1, "metal": 1.55},
        "details": "my description",
    }


def test_user_agent() -> None:
    data = bptf.register_user_agent()

    print(data)
    assert data["status"] == "active"
    assert data["client"] == "Listed with <3 | tf2-utils"
    assert data["current_time"] > 0
    assert data["expire_at"] > 0


def test_create_listing() -> None:
    listing = bptf.create_listing(
        "263;6", "buy", {"keys": 0, "metal": 0.11}, "my test description"
    )

    assert isinstance(listing, Listing)
    assert isinstance(listing.item, dict)
    assert isinstance(listing.currencies, dict)
    assert listing.steamid == steam_id
    assert listing.intent == "buy"
    assert listing.appid == 440
    assert listing.listedAt > 0
    assert listing.currencies == {"metal": 0.11}
    assert listing.details == "my test description"
    assert listing.item["craftable"]
    assert listing.item["quality"]["name"] == "Unique"
    assert listing.item["quality"]["id"] == 6
    assert listing.item["tradable"]
    assert listing.item["baseName"] == "Ellis' Cap"
    assert listing.item["defindex"] == 263
    assert listing.userAgent["client"] == "Listed with <3 | tf2-utils"
    assert listing.userAgent["lastPulse"] > 0


def test_delete_listing() -> None:
    listing = bptf.delete_listing_by_sku("263;6")

    assert isinstance(listing, bool)
    assert listing


def test_stop_user_agent() -> None:
    data = bptf.stop_user_agent()

    assert data["status"] == "inactive"
