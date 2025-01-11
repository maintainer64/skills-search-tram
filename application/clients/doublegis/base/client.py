import logging
from dataclasses import dataclass

import aiohttp

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class DoubleGisBaseApi:
    base_url: str = ""
    verify_ssl: bool = False
    security_key: str = ""
    timeout: float = 3.0

    async def _request(self, method: str, url: str, json: dict | None, params: dict | None, **kwargs) -> bytes:
        logger.debug(f"Отправка запроса в [{method}]{url} {json=} {params=}")
        logger.info(f"Отправка запроса в [{method}]{url}")
        async with aiohttp.ClientSession() as client:
            response = await client.request(
                method=method,
                url=url,
                json=json,
                verify_ssl=self.verify_ssl,
                params=params,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                **kwargs,
            )
            result = await response.read()
        logger.debug(f"Получен ответ от [{method}]{url} {result=}")
        logger.info(f"Получен ответ от [{method}]{url}")
        return result
