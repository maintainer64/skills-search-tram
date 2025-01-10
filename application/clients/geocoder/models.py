"""
https://yandex.ru/maps-api/products/geocoder-api
"""

from dataclasses import dataclass


@dataclass
class GeocoderSearchResponse:
    lat: float | None = None
    lng: float | None = None
    locality: str | None = None
    district: str | None = None
    street: str | None = None
    house: str | None = None

    @staticmethod
    def kinds():
        return ["locality", "district", "street", "house"]

    def __str__(self) -> str:
        return ", ".join([getattr(self, x) for x in self.kinds() if getattr(self, x) is not None])
