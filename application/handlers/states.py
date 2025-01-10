import enum
from typing import Any

from pydantic import BaseModel

Event = dict[str, Any]


class States(str, enum.Enum):
    NONE = "none"
    SET_ADDRESS = "set_address"
    COMPLETE_ADDRESS = "complete_address"


class ApplicationState(BaseModel):
    state: States = States.NONE
    geo_lat: float | None = None
    geo_lon: float | None = None
    geo_address: str | None = None
    geo_city_code: str | None = None

    def complete_address(self) -> bool:
        return bool(self.geo_lat is not None and self.geo_lon is not None and self.geo_address and self.geo_city_code)

    def reset_address(self):
        self.geo_lat = None
        self.geo_lon = None
        self.geo_address = None
        self.geo_city_code = None


def get_application_state(event: Event) -> ApplicationState:
    state = event.get("state")
    if not isinstance(state, dict):
        return ApplicationState()
    application = state.get("application")
    if not isinstance(application, dict):
        return ApplicationState()
    return ApplicationState.model_validate(application)


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
