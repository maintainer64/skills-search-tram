from typing import Literal
from dataclasses import field
from datetime import datetime

from pydantic import BaseModel


class SearchScheduleDeparture(BaseModel):
    departure_time: int = field(default_factory=lambda: int(datetime.now().timestamp()))
    platforms: list[str] | None = None
    routes: list[str] | None = None
    direction_id: str | None = None


class SearchScheduleRequest(BaseModel):
    type: Literal["full_day_platform", "interval_trip"] = "full_day_platform"
    project: str = ""
    request: SearchScheduleDeparture = field(default_factory=SearchScheduleDeparture)


class SearchScheduleRequests(BaseModel):
    requests: list[SearchScheduleRequest] = field(default_factory=list)


class SearchScheduleResponseWorkHours(BaseModel):
    start_time: int | None = None
    finish_time: int | None = None


class SearchScheduleResponseSchedule(BaseModel):
    period: int | None = None
    forecast: bool | None = None
    start_time: int | None = None
    precise_time: str | None = None
    type: Literal["precise", "periodic"] | None = None
    work_hours: SearchScheduleResponseWorkHours | None = None


class SearchScheduleResponseSchedules(BaseModel):
    direction_id: str | None = None
    route_id: str | None = None
    schedule: SearchScheduleResponseSchedule | None = None
    to_platform_name: str | None = None


class SearchScheduleResponse(BaseModel):
    status: str
    direction_id: str | None = None
    period: int | None = None
    route_id: str | None = None
    work_hours: SearchScheduleResponseWorkHours | None = None
    schedules: list[SearchScheduleResponseSchedules] | None = None


class SearchScheduleResponses(BaseModel):
    responses: list[SearchScheduleResponse] = field(default_factory=list)
    message: str | None = None
    type: str | None = None
    status: str | None = None
