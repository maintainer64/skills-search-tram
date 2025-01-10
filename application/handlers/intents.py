from dataclasses import dataclass

from application.handlers.states import Event
from application.services.search_schedule_service import TransportType


def intents_confirm(event: Event) -> bool:
    request = event.get("request")
    if not isinstance(request, dict):
        return False
    nlu = request.get("nlu")
    if not isinstance(nlu, dict):
        return False
    intents = nlu.get("intents")
    if not isinstance(intents, dict):
        return False
    return "CONFIRM" in intents or "YANDEX.CONFIRM" in intents


def intents_reject(event) -> bool:
    request = event.get("request")
    if not isinstance(request, dict):
        return False
    nlu = request.get("nlu")
    if not isinstance(nlu, dict):
        return False
    intents = nlu.get("intents")
    if not isinstance(intents, dict):
        return False
    return "REJECT" in intents or "YANDEX.REJECT" in intents


@dataclass
class IntentGeo:
    country: str = ""
    city: str = ""
    street: str = ""
    house_number: str = ""
    airport: str = ""

    def __str__(self):
        return f"{self.country} {self.city} {self.street} {self.house_number} {self.airport}"


def intents_geo(event: Event) -> list[IntentGeo]:
    parsed: list[IntentGeo] = []
    request = event.get("request")
    if not isinstance(request, dict):
        return parsed
    nlu = request.get("nlu")
    if not isinstance(nlu, dict):
        return parsed
    entities = nlu.get("entities")
    if not isinstance(entities, list):
        return parsed
    for entity in entities:
        if not isinstance(entity, dict):
            continue
        entity_type = entity.get("type")
        if entity_type != "YANDEX.GEO":
            continue
        entity_value = entity.get("value")
        if not isinstance(entity_value, dict):
            continue
        parsed.append(IntentGeo(**entity_value))
    return parsed


def intents_int(event: Event) -> list[int]:
    parsed: list[int] = []
    request = event.get("request")
    if not isinstance(request, dict):
        return parsed
    nlu = request.get("nlu")
    if not isinstance(nlu, dict):
        return parsed
    entities = nlu.get("entities")
    if not isinstance(entities, list):
        return parsed
    for entity in entities:
        if not isinstance(entity, dict):
            continue
        entity_type = entity.get("type")
        if entity_type != "YANDEX.NUMBER":
            continue
        entity_value = entity.get("value")
        if not isinstance(entity_value, int):
            continue
        parsed.append(entity_value)
    return parsed


def intents_transport(event: Event) -> TransportType | None:
    request = event.get("request")
    if not isinstance(request, dict):
        return None
    text = request.get("original_utterance")
    if not isinstance(text, str):
        return None
    text = text.lower()
    if "тобу" in text:
        return TransportType.Bus
    if "трол" in text:
        return TransportType.Trolley
    if "трам" in text:
        return TransportType.Tram
    return None
