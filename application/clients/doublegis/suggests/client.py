import json
import logging

import aiohttp
from aiohttp import ClientSession

from application.clients.doublegis.suggests.models import DoubleGisSuggestRequests, DoubleGisSuggestResponse

logger = logging.getLogger(__name__)


class DoubleGisSuggests:
    base_url = "https://catalog.api.2gis.com"
    verify_ssl = False

    def __init__(
        self,
        security_key: str,
    ):
        self._security_key = security_key
        self.session = ClientSession()

    async def _request(self, method: str, url: str, json: dict | None, params: dict | None) -> bytes:
        logger.debug(f"Отправка запроса в [{method}]{url} {json=} {params=}")
        logger.info(f"Отправка запроса в [{method}]{url}")
        async with aiohttp.ClientSession() as client:
            response = await client.request(
                method=method,
                url=url,
                json=json,
                verify_ssl=self.verify_ssl,
                params=params,
                raise_for_status=True,
            )
            result = await response.read()
        logger.info(f"Получен ответ от [{method}]{url}")
        logger.info(f"Получен ответ от [{method}]{url}")
        logger.debug(f"Получен ответ от [{method}]{url} {result=}")
        return result

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
                "key": self._security_key,
                "locale": "ru_RU",
                "fields": "items.routes,items.platforms,items.directions",
                "search_is_query_text_complete": "true",
                "search_nearby": "true",
                "search_input_method": "voice",
                "type": "route",
                "q": params.search,
                "location": f"{params.lon}, {params.lat}",
                "page_size": 3,
            },
        )
        return DoubleGisSuggestResponse.model_validate_json(response)

    async def suggests_building(self, params: DoubleGisSuggestRequests) -> dict:
        assert params.search, "Не указан поисковой запрос"
        path = "/3.0/items/geocode"
        response = await self._request(
            method="GET",
            url=self.base_url + path,
            json=params.model_dump(),
            params={
                "key": self._security_key,
                "locale": "ru_RU",
                "search_is_query_text_complete": "true",
                "search_input_method": "voice",
                "type": "building",
                "fields": "items.address,items.point,items.adm_div,items.full_address_name",
                "q": params.search,
                "page_size": 3,
                "page": 1,
            },
        )
        return json.loads(response)
