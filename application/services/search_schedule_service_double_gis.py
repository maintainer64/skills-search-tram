import logging
from collections import defaultdict
from dataclasses import dataclass
import math
from datetime import datetime
from functools import partial
from typing import Literal

from application.clients.doublegis.routings.client import DoubleGisSearchSchedule
from application.clients.doublegis.routings.models import (
    SearchScheduleRequests,
    SearchScheduleRequest,
    SearchScheduleDeparture,
)
from application.clients.doublegis.suggests.client import DoubleGisSuggests
from application.clients.doublegis.suggests.models import DoubleGisSuggestRequests
from application.services.search_schedule_service import (
    SearchScheduleServiceABC,
    TransportType,
    SearchServiceStations,
    SearchServiceStation,
    SearchServiceTime,
)

from haversine import haversine, Unit

logger = logging.getLogger(__name__)


@dataclass
class RouteSearcher:
    platform_id: str
    route_id: str
    direction_type: str
    distance_km: float
    first_station: bool
    last_station: bool
    index: int = 0

    def set_index(self, index):
        self.index = index

    def group_by(self) -> str:
        return f"{self.route_id}_{self.direction_type}"

    @staticmethod
    def filter(self: "RouteSearcher", distance_km_max: float) -> bool:
        if self.direction_type == "forward" and self.last_station:
            return False
        if self.direction_type == "backward" and self.first_station:
            return False
        return self.distance_km <= distance_km_max

    @staticmethod
    def sort(self: "RouteSearcher") -> tuple[float, int]:
        return self.distance_km, self.index

    @staticmethod
    def unique(self: list["RouteSearcher"]) -> list["RouteSearcher"]:
        groups: set[str] = set()
        unique_list: list["RouteSearcher"] = []
        for item in self:
            if item.group_by() not in groups:
                groups.add(item.group_by())
                unique_list.append(item)
        return unique_list


@dataclass
class ScheduleSearcher:
    direction_id: str
    route_id: str
    precise_time: str
    start_time: float
    to_platform_name: str
    type: Literal["precise", "periodic"] | None = None
    index: int = 0

    def set_index(self, index):
        self.index = index

    def parse_precise_time(self) -> tuple[int, int] | None:
        try:
            [hour, minute] = list(map(int, self.precise_time.split(":")))
            assert 0 <= hour <= 23
            assert 0 <= minute <= 59
            return hour, minute
        except Exception:
            return None

    def group_by(self) -> str:
        return f"{self.direction_id}_{self.route_id}"

    @staticmethod
    def filter(self: "ScheduleSearcher") -> bool:
        now = int(datetime.now().timestamp())
        return self.type == "precise" and self.start_time >= now and self.parse_precise_time() is not None

    @staticmethod
    def sort(self: "ScheduleSearcher") -> tuple[float, int]:
        return self.start_time, self.index

    @staticmethod
    def groups(self: list["ScheduleSearcher"], items: int) -> list["ScheduleSearcher"]:
        """
        Группировка списка по параметру group_by
        :param self: Список расписание
        :param items: Максимальное кол-во по каждому group_by
        :return:
        """
        groups: dict[str, int] = defaultdict(lambda: 0)
        unique_list: list["ScheduleSearcher"] = []
        for item in self:
            groups[item.group_by()] += 1
            if groups[item.group_by()] <= items:
                unique_list.append(item)
        return unique_list


class SearchScheduleServiceDoubleGis(SearchScheduleServiceABC):
    def __init__(
        self,
        search_schedule: DoubleGisSearchSchedule,
        suggestion: DoubleGisSuggests,
    ):
        self.search_schedule = search_schedule
        self.suggestion = suggestion

    async def get_transport(
        self,
        transport_query: str,
        transport_type: TransportType | None,
        lat: float,
        lon: float,
        city_code: str,
    ) -> SearchServiceStations:
        transport = await self.suggestion.suggests_transport(
            params=DoubleGisSuggestRequests(
                lat=lat,
                lon=lon,
                search=f"{transport_query} {transport_type.value if transport_type else ''}",
            )
        )
        if not transport.result:
            return SearchServiceStations()
        # Получили все подходящие ветки транспорта
        routes = [item for item in transport.result.items if item.type == "route"]
        routes_search = [
            RouteSearcher(
                platform_id=platform.id or "",
                route_id=route.id or "",
                direction_type=direction.type or "",
                distance_km=(
                    haversine(
                        (lat, lon),
                        platform.geometry.point(),
                        unit=Unit.KILOMETERS,
                    )
                    if platform.geometry
                    else math.inf
                ),
                first_station=platform_index == 0,
                last_station=platform_index + 1 == len(direction.platforms),
            )
            for route in routes
            for direction in route.directions
            for platform_index, platform in enumerate(direction.platforms)
        ]
        [route.set_index(index) for index, route in enumerate(routes_search)]
        # Отфильтровали список
        # Соритируем в поисках подходящей остановки
        routes_search = sorted(
            filter(partial(RouteSearcher.filter, distance_km_max=10.0), routes_search),
            key=RouteSearcher.sort,
            reverse=False,
        )
        logger.debug(f"Список подходящих остановок для маршрута {transport_query=} {len(routes_search)=}")
        # Группируем список
        routes_search = RouteSearcher.unique(routes_search)
        logger.debug(f"Сгруппировали список подходящих остановок для маршрута {transport_query=} {len(routes_search)=}")
        if not routes_search:
            return SearchServiceStations()
        schedules = await self.search_schedule.search_schedule(
            params=SearchScheduleRequests(
                requests=[
                    SearchScheduleRequest(
                        type="full_day_platform",
                        request=SearchScheduleDeparture(
                            platforms=list({route.platform_id for route in routes_search}),
                            routes=list({route.route_id for route in routes_search}),
                        ),
                        project=city_code,
                    )
                ]
            )
        )
        schedules_search = [
            ScheduleSearcher(
                direction_id=schedule.direction_id or "",
                route_id=schedule.route_id or "",
                precise_time=schedule.schedule.precise_time or "",
                start_time=schedule.schedule.start_time or 0.00,
                type=schedule.schedule.type,
                to_platform_name=schedule.to_platform_name or "",
            )
            for response in (schedules.responses or [])
            for schedule in (response.schedules or [])
            if schedule.schedule is not None
        ]
        [schedule.set_index(index) for index, schedule in enumerate(schedules_search)]
        # Отфильтровали список
        # Соритируем в поисках подходящей остановки
        schedules_search = sorted(
            filter(ScheduleSearcher.filter, schedules_search),
            key=ScheduleSearcher.sort,
            reverse=False,
        )
        logger.debug(f"Список подходящего транспорта для маршрута {transport_query=} {len(schedules_search)=}")
        # Группируем список
        schedules_search = ScheduleSearcher.groups(schedules_search, items=2)
        logger.debug(
            f"Сгруппировали список подходящего транспорта для маршрута {transport_query=} {len(schedules_search)=}"
        )
        stations_result: dict[str, SearchServiceStation] = defaultdict(SearchServiceStation)
        # Для каждого направления конечной станции создаём матрицу подходящих маршрутов
        for schedule_search in schedules_search:
            stations_result[schedule_search.to_platform_name].last_station_title = schedule_search.to_platform_name
            precise = schedule_search.parse_precise_time() or (0, 0)
            stations_result[schedule_search.to_platform_name].times.append(
                SearchServiceTime(
                    hour=precise[0],
                    minute=precise[1],
                )
            )

        return SearchServiceStations(stations=list(stations_result.values()))
