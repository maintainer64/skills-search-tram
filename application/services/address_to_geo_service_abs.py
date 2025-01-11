from abc import ABC, abstractmethod

from pydantic import BaseModel


class GeoPoint(BaseModel):
    lat: float
    lon: float
    address: str
    time_zone_offset: int
    code: str


class AddressToGeoServiceABC(ABC):
    @abstractmethod
    async def get_by_address(self, address: str) -> GeoPoint | None: ...  # type: ignore[E704]
