import json
import logging

import aiohttp

from application.clients.doublegis.routings.models import SearchScheduleRequests, SearchScheduleResponses
from application.clients.doublegis.utils import px

logger = logging.getLogger(__name__)


class DoubleGisSearchSchedule:
    base_url = "https://routing.api.2gis.com"
    ssl_verify = False

    def __init__(self, security_key: str):
        self._security_key = security_key

    async def _request(self, method: str, url: str, json: dict | None, params: dict | None) -> bytes:
        logger.debug(f"Отправка запроса в [{method}]{url} {json=} {params=}")
        logger.info(f"Отправка запроса в [{method}]{url}")
        async with aiohttp.ClientSession() as client:
            response = await client.request(
                method=method,
                url=url,
                json=json,
                verify=self.ssl_verify,
                params=params,
            )
            result = await response.read()
        logger.info(f"Получен ответ от [{method}]{url}")
        logger.info(f"Получен ответ от [{method}]{url}")
        logger.debug(f"Получен ответ от [{method}]{url} {result=}")
        return result

    async def search_schedule(self, params: SearchScheduleRequests) -> SearchScheduleResponses:
        path = "/ctx/search_schedule"
        response = await self._request(
            method="POST",
            url=self.base_url + path,
            json=params.model_dump(),
            params={
                "key": self._security_key,
                "r": px(path, self._security_key, json.dumps(params.model_dump(), ensure_ascii=False)),
            },
        )
        return SearchScheduleResponses.model_json_validate(response)
