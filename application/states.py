import enum
from dataclasses import dataclass
from typing import Any

Event = dict[str, Any]


class States(str, enum.Enum):
    NONE = "none"
    SET_ADDRESS = "set_address"
    COMPLETE_ADDRESS = "complete_address"


@dataclass()
class ApplicationState:
    state: States = States.NONE
    geo_lat: float | None = None
    geo_lon: float | None = None
    geo_address: str | None = None

    def dict(self) -> dict[str, Any]:
        return {
            "state": self.state.value,
            "geo_lat": self.geo_lat,
            "geo_lon": self.geo_lon,
            "geo_address": self.geo_address,
        }


def get_application_state(event: Event) -> ApplicationState:
    state = event.get("state")
    if not isinstance(state, dict):
        return ApplicationState()
    application = state.get("application")
    if not isinstance(application, dict):
        return ApplicationState()
    return ApplicationState(
        state=States(application.get("state", States.NONE.value)),
        geo_lat=application.get("geo_lat"),
        geo_lon=application.get("geo_lon"),
        geo_address=application.get("geo_address"),
    )


def session_is_new(event: Event) -> bool:
    session = event.get("session")
    if not isinstance(session, dict):
        return False
    return session.get("new") is True


def get_text_from_event(event: Event) -> str | None:
    request = event.get("request")
    if not isinstance(request, dict):
        return None
    return request.get("original_utterance")
