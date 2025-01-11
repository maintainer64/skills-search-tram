import enum
from typing import Any

from pydantic import BaseModel

from application.services.address_to_geo_service_abs import GeoPoint

Event = dict[str, Any]


class States(str, enum.Enum):
    NONE = "none"
    SET_ADDRESS = "set_address"
    COMPLETE_ADDRESS = "complete_address"


class ApplicationState(BaseModel):
    state: States = States.NONE
    geo_point: GeoPoint | None = None


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
    return request.get("command")
