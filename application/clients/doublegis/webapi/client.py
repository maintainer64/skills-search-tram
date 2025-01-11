import logging
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Pattern

from application.clients.doublegis.base.client import DoubleGisBaseApi
from application.clients.doublegis.webapi.models import DoubleGisWebApiConfig

logger = logging.getLogger(__name__)

RE_WEB_API_URL = re.compile('"webApiUrl":"([^"]+)"')
RE_WEB_API_KEY = re.compile('"webApiKey":"([^"]+)"')
RE_WEB_API_URL_3 = re.compile('"webApi3Url":"([^"]+)"')


@dataclass(kw_only=True)
class DoubleGisWebApiConfigParser(DoubleGisBaseApi):
    base_url: str = "https://2gis.ru"
    verify_ssl: bool = False
    timeout: float = 3.0
    cache_minutes: int = 5
    _cached_value: DoubleGisWebApiConfig | None = None

    @staticmethod
    def parse_group_regex(pattern: Pattern[str], text: str) -> str | None:
        match = pattern.search(text)
        return match.group(1) if match else None

    async def get_config(
        self,
    ) -> DoubleGisWebApiConfig:
        response = await self._request(
            method="GET",
            url=self.base_url,
            json=None,
            params=None,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            },
        )
        html_page = response.decode()
        config = DoubleGisWebApiConfig(
            web_api_key=self.parse_group_regex(pattern=RE_WEB_API_KEY, text=html_page),
            web_api_3_url=self.parse_group_regex(pattern=RE_WEB_API_URL_3, text=html_page),
            web_api_url=self.parse_group_regex(pattern=RE_WEB_API_URL, text=html_page),
        )
        logger.debug(f"Получили конфигурацию API 2GIS WEB {config.model_dump()}")
        return config

    async def get_config_cached(
        self,
    ) -> DoubleGisWebApiConfig:
        if self._cached_value and self._cached_value.created_at >= datetime.utcnow() - timedelta(
            minutes=self.cache_minutes
        ):
            logger.info("Получение настроек API 2GIS WEB из кеша")
            return self._cached_value
        logger.info("Получение настроек API 2GIS WEB из сервиса")
        self._cached_value = await self.get_config()
        return self._cached_value
