"""
https://yandex.ru/maps-api/products/geocoder-api
"""

import requests

from application.clients.geocoder.models import GeocoderSearchResponse
from application.config import API_GEOCODE_YANDEX


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
