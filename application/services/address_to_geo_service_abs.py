from abc import ABC, abstractmethod

from pydantic import BaseModel


class GeoPoint(BaseModel):
    lat: float
    lon: float
    address: str
    city_alias_code: str


class AddressToGeoServiceABC(ABC):
    @abstractmethod
    async def get_by_address(self, address: str) -> GeoPoint | None: ...  # type: ignore[E704]
