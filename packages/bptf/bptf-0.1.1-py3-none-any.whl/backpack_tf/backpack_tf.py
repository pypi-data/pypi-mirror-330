import requests
from tf2_utils import SchemaItemsUtils, sku_is_craftable, sku_to_quality

from .classes import Currencies, Listing
from .exceptions import InvalidIntent
from .utils import get_item_hash, needs_token


class BackpackTF:
    URL = "https://api.backpack.tf/api"

    def __init__(
        self,
        token: str,
        steam_id: str,
        api_key: str = None,
        user_agent: str = "Listed with <3",
    ) -> None:
        del api_key  # for future use

        self._token = token
        self._steam_id = steam_id
        self._user_agent = user_agent
        self._user_token = None
        self._schema = SchemaItemsUtils()
        self.__headers = {"User-Agent": f"{self._user_agent} | tf2-utils"}

    @needs_token
    def _request(self, method: str, endpoint: str, params: dict = {}, **kwargs) -> dict:
        params["token"] = self._token
        response = requests.request(
            method, self.URL + endpoint, params=params, headers=self.__headers, **kwargs
        )
        return response.json()

    def _get_sku_item_hash(self, sku: str) -> str:
        item_name = self._schema.sku_to_base_name(sku)
        return get_item_hash(item_name)

    def _construct_listing_item(self, sku: str) -> dict:
        return {
            "baseName": self._schema.sku_to_base_name(sku),
            "craftable": sku_is_craftable(sku),
            "tradable": True,
            "quality": {"id": sku_to_quality(sku)},
        }

    def _construct_listing(
        self, sku: str, intent: str, currencies: dict, details: str, asset_id: int = 0
    ) -> dict:
        if intent not in ["buy", "sell"]:
            raise InvalidIntent(f"{intent} must be buy or sell")

        listing = {
            "item": self._construct_listing_item(sku),
            "buyout": True,
            "offers": True,
            "promoted": False,
            "details": details,
            "currencies": Currencies(**currencies).__dict__,
        }

        if intent == "sell":
            listing["id"] = asset_id

        return listing

    def get_listings(self, skip: int = 0, limit: int = 100) -> dict:
        return self._request(
            "GET", "/v2/classifieds/listings", {"skip": skip, "limit": limit}
        )

    def create_listing(
        self, sku: str, intent: str, currencies: dict, details: str, asset_id: int = 0
    ) -> Listing:
        listing = self._construct_listing(sku, intent, currencies, details, asset_id)
        response = self._request("POST", "/v2/classifieds/listings", json=listing)

        return Listing(**response)

    def create_listings(self, listings: list[dict]) -> list[Listing]:
        to_list = [self._construct_listing(**listing) for listing in listings]
        response = self._request("POST", "/v2/classifieds/listings/batch", json=to_list)
        return [Listing(**listing["result"]) for listing in response]

    def delete_all_listings(self) -> dict:
        return self._request("DELETE", "/v2/classifieds/listings")

    def delete_listing(self, listing_id: str) -> dict:
        return self._request("DELETE", f"/v2/classifieds/listings/{listing_id}")

    def delete_listing_by_asset_id(self, asset_id: int) -> dict:
        listing_id = f"440_{asset_id}"
        return self.delete_listing(listing_id)

    def delete_listing_by_sku(self, sku: str) -> dict:
        item_hash = self._get_sku_item_hash(sku)
        listing_id = f"440_{self._steam_id}_{item_hash}"
        return self.delete_listing(listing_id)

    def register_user_agent(self) -> dict:
        return self._request("POST", "/agent/pulse")

    def get_user_agent_status(self) -> dict:
        return self._request("POST", "/agent/status")

    def stop_user_agent(self) -> dict:
        return self._request("POST", "/agent/stop")
