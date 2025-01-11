from datetime import datetime

from pydantic import BaseModel, Field


class DoubleGisWebApiConfig(BaseModel):
    web_api_key: str | None = None
    web_api_3_url: str | None = None
    web_api_url: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
