"""
https://yandex.ru/maps-api/products/geocoder-api
"""

from dataclasses import dataclass

import requests

from .config import API_GEOCODE_YANDEX


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


def geocoder_search(address: str) -> GeocoderSearchResponse:
    result = GeocoderSearchResponse()
    response = requests.get(
        "https://geocode-maps.yandex.ru/1.x/",
        params={  # type: ignore[arg-type]
            "geocode": address,
            "results": 1,
            "lang": "ru_RU",
            "format": "json",
            "kind": "house",
            "apikey": API_GEOCODE_YANDEX,
        },
    )
    payload = response.json()
    for o in payload["response"]["GeoObjectCollection"]["featureMember"]:
        if o["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["kind"].lower() != "house":
            continue
        lng, lat = map(float, o["GeoObject"]["Point"]["pos"].split(" "))
        result.lat, result.lng = lat, lng
        components = o["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]
        for component in components:
            if component["kind"] in GeocoderSearchResponse.kinds():
                setattr(result, component["kind"], component["name"])
    return result
