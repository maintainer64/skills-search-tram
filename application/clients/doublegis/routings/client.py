import json
import logging
from dataclasses import dataclass, field

from application.clients.doublegis.base.client import DoubleGisBaseApi
from application.clients.doublegis.routings.models import SearchScheduleRequests, SearchScheduleResponses
from application.clients.doublegis.utils import px
from application.clients.doublegis.webapi.client import DoubleGisWebApiConfigParser

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class DoubleGisSearchSchedule(DoubleGisBaseApi):
    base_url: str = "https://routing.api.2gis.com"
    verify_ssl: bool = False
    security_key: str = ""
    timeout: float = 3.0
    config_parser: DoubleGisWebApiConfigParser = field(default_factory=DoubleGisWebApiConfigParser)

    async def search_schedule(self, params: SearchScheduleRequests) -> SearchScheduleResponses:
        path = "/ctx/search_schedule"
        config = await self.config_parser.get_config_cached()
        security_key = config.web_api_key or self.security_key
        response = await self._request(
            method="POST",
            url=self.base_url + path,
            json=params.model_dump(),
            params={
                "key": security_key,
                "r": px(path, security_key, json.dumps(params.model_dump(), ensure_ascii=False)),
            },
        )
        return SearchScheduleResponses.model_validate_json(response)
