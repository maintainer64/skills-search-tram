import logging
from dataclasses import dataclass

from application.clients.doublegis.base.client import DoubleGisBaseApi
from application.clients.doublegis.suggests.models import (
    DoubleGisSuggestRequests,
    DoubleGisSuggestResponse,
    DoubleGisSuggestBuildingResponse,
    DoubleGisSuggestRegionResponse,
)

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class DoubleGisSuggests(DoubleGisBaseApi):
    base_url: str = "https://catalog.api.2gis.com"
    verify_ssl: bool = False
    security_key: str = ""
    timeout: float = 3.0

    async def suggests_transport(self, params: DoubleGisSuggestRequests) -> DoubleGisSuggestResponse:
        assert params.lat, "Не указана ширина"
        assert params.lon, "Не указана долгота"
        assert params.search, "Не указан поисковой запрос"
        path = "/3.0/suggests"
        response = await self._request(
            method="GET",
            url=self.base_url + path,
            json=params.model_dump(),
            params={
                "key": self.security_key,
                "locale": "ru_RU",
                "fields": "items.routes,items.platforms,items.directions",
                "search_is_query_text_complete": "true",
                "search_nearby": "true",
                "search_input_method": "voice",
                "type": "route",
                "q": params.search,
                "location": f"{params.lon}, {params.lat}",
                "page_size": 30,
            },
        )
        return DoubleGisSuggestResponse.model_validate_json(response)

    async def suggests_building(self, params: DoubleGisSuggestRequests) -> DoubleGisSuggestBuildingResponse:
        assert params.search, "Не указан поисковой запрос"
        path = "/3.0/items/geocode"
        response = await self._request(
            method="GET",
            url=self.base_url + path,
            json=params.model_dump(),
            params={
                "key": self.security_key,
                "locale": "ru_RU",
                "search_is_query_text_complete": "true",
                "search_input_method": "voice",
                "type": "building",
                "fields": "items.point,items.full_address_name",
                "q": params.search,
                "page_size": 3,
                "page": 1,
            },
        )
        return DoubleGisSuggestBuildingResponse.model_validate_json(response)

    async def region_by_branch_id(self, branch_id: str) -> DoubleGisSuggestRegionResponse:
        path = "/2.0/region/get"
        response = await self._request(
            method="GET",
            url=self.base_url + path,
            json=None,
            params={
                "key": self.security_key,
                "branch_id": branch_id,
                "fields": "items.time_zone,items.uri_code,items.code",
            },
        )
        return DoubleGisSuggestRegionResponse.model_validate_json(response)
