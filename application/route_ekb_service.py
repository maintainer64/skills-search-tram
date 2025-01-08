import logging
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

from dacite import from_dict
from typing_extensions import Self

from haversine import haversine, Unit

from application.intents import TransportType
from application.route_ekb_api import EKBTransportAPI

logger = logging.getLogger(__name__)


def _is_number(number: str) -> bool:
    try:
        int(number)
        return True
    except Exception:
        return False


@dataclass(kw_only=True)
class RouteItem:
    mr_id: str
    mr_num: str
    mr_title: str
    mr_title_en: str

    def fits(self, transport_number: str) -> bool:
        return (
            transport_number == self.mr_num or not _is_number(self.mr_num) and self.mr_num.startswith(transport_number)
        )

    def __hash__(self) -> int:
        return hash(self.mr_id)

    def __eq__(self, other) -> bool:
        if not isinstance(other, RouteItem):
            return NotImplemented
        return self.mr_id == other.mr_id


@dataclass(kw_only=True)
class TransportRoutes:
    tt_id: str
    tt_title: str
    tt_title_en: str
    routes: list[RouteItem]


@dataclass(kw_only=True)
class StopItem:
    st_id: str | int
    st_lat: str | float
    st_long: str | float
    st_title: str
    st_title_en: str
    distance_km: float | None = None

    def set_distance(self, lat: float, lng: float) -> Self:
        self.distance_km = haversine(
            point1=(float(self.st_lat), float(self.st_long)),
            point2=(float(lat), float(lng)),
            unit=Unit.KILOMETERS,
        )
        return self

    def __hash__(self) -> int:
        return hash(self.st_id)

    def __eq__(self, other) -> bool:
        if not isinstance(other, StopItem):
            return NotImplemented
        return self.st_id == other.st_id


@dataclass(kw_only=True, eq=True)
class ArrivalRoute:
    firststation_title: str
    firststation_title_en: str
    laststation_title: str
    laststation_title_en: str
    mr_id: str
    rc_kkp: str
    rl_racetype: str
    tc_arrivetime: str
    tc_systime: str
    tt_id: str
    u_inv: str

    @property
    def time(self) -> tuple[int, int]:
        try:
            hour, minutes = self.tc_arrivetime.split(":")
            return int(hour), int(minutes)
        except Exception:
            return -1, 0

    def get_time(self) -> float:
        hour, minutes = self.time
        return float(int(hour) * 60 + int(minutes))

    def __gt__(self, other: Self) -> bool:
        return self.get_time() > other.get_time()


@dataclass(kw_only=True, eq=True)
class SearchServiceTime:
    hour: int
    minute: int

    def text(self) -> str:
        now = datetime.now(tz=timezone(offset=timedelta(hours=5)))
        current_time = now.hour * 60 + now.minute
        minutes = (self.hour * 60 + self.minute) - current_time
        if 0 < minutes < 30:
            return f"через {minutes} минут"
        return f"в {self.hour} часов {self.minute} минут"


@dataclass(kw_only=True, eq=True)
class SearchServiceStation:
    last_station_title: str
    times: list[SearchServiceTime]

    def text(self) -> str:
        if not self.times:
            return ""
        times = ". Затем ".join([x.text() for x in self.times])
        return f"До станции {self.last_station_title} прибудет {times}."


@dataclass(kw_only=True, eq=True)
class SearchServiceStations:
    stations: list[SearchServiceStation]

    def text(self) -> str:
        if not self.stations:
            return "Не нашла подходящих маршрутов"
        return ".".join([x.text() for x in self.stations])


def ekb_transport_service(
    transport_number: int,
    transport_type: TransportType | None,
    geo_lat: float,
    geo_lon: float,
) -> SearchServiceStations:
    """
    Поиск подходящего маршрута и остановки
    :param transport_number: Номер транспорта маршрута
    :param transport_type: Тип транспорта
    :param geo_lat: Точка дома где искать
    :param geo_lon: Точка дома где искать
    :return: Список маршрутов
    """
    client = EKBTransportAPI()
    trans_type_response = client.get_trans_type_tree()
    routes = get_best_transport_type(
        trans_type=trans_type_response["result"],
        transport_number=str(transport_number),
        transport_type=transport_type,
    )
    routes = list(set(routes))
    logger.info(f"Нашли подходящий транспорт {len(routes)}")
    stops: list[StopItem] = []
    for route in routes:
        route_response = client.get_route(mr_id=route.mr_id)
        stops.extend(
            get_best_stop(
                route_response=route_response["result"]["races"],
                geo_lat=geo_lat,
                geo_lon=geo_lon,
                limit=2,
            )
        )
    stops = list(set(stops))
    logger.info(f"Нашли подходящие остановки {len(stops)}")
    arrivals: list[ArrivalRoute] = []
    for stop in stops:
        arrivals.extend(
            get_best_arrival(
                arrival_response=client.get_stop_arrive(st_id=str(stop.st_id))["result"],
                routes=routes,
                limit=2,
            )
        )
    logger.info(f"Нашли подходящие прибытия на остановки {len(arrivals)}")
    # Собираем по маршрутам
    stations: dict[str, SearchServiceStation] = dict()
    for arrival in arrivals:
        if arrival.laststation_title not in stations:
            stations[arrival.laststation_title] = SearchServiceStation(
                last_station_title=arrival.laststation_title,
                times=[],
            )
        hour, minute = arrival.time
        stations[arrival.laststation_title].times.append(
            SearchServiceTime(
                hour=hour,
                minute=minute,
            )
        )
    return SearchServiceStations(stations=list(stations.values()))


def get_best_transport_type(
    trans_type: list[dict],
    transport_number: str,
    transport_type: TransportType | None = None,
) -> list[RouteItem]:
    """
    Поиск подходящих маршрутов по запросу
    :param trans_type: Ответ от сервера
    :param transport_number: Номер транспортной ветки
    :param transport_type: Тип транспорта или None - все
    :return:
    """
    routes: list[RouteItem] = []
    transport_types: list[TransportRoutes] = [from_dict(data_class=TransportRoutes, data=data) for data in trans_type]
    for type_ in transport_types:
        if transport_type is not None and transport_type.name != type_.tt_title_en:
            continue
        for route in type_.routes:
            if not route.fits(transport_number):
                continue
            routes.append(route)
    return routes


def get_best_stop(
    route_response: list[dict],
    geo_lat: float,
    geo_lon: float,
    limit: int = 2,
    max_distance: float = 10,
) -> list[StopItem]:
    """
    Поиск подходящих остановок от ближайшей точки
    :param route_response: Ответ от сервера
    :param geo_lat: Номер транспортной ветки
    :param geo_lon: Тип транспорта или None - все
    :param limit: Кол-во остановок
    :param max_distance: Макимальная дистанция в километрах
    :return:
    """
    stops: list[StopItem] = []
    for route in route_response:
        for stop_raw in route["stopList"]:
            stop = from_dict(data_class=StopItem, data=stop_raw).set_distance(
                lat=geo_lat,
                lng=geo_lon,
            )
            stops.append(stop)
    stops = list(set(stops))
    stops = sorted(
        filter(lambda x: x.distance_km is None or x.distance_km <= max_distance, stops),
        key=lambda x: (x.distance_km or 99999),
        reverse=False,
    )
    return stops[:limit]


def get_best_arrival(
    arrival_response: list[dict],
    routes: list[RouteItem],
    limit: int = 2,
) -> list[ArrivalRoute]:
    """
    Поиск подходящих остановок от ближайшей точки
    :param arrival_response: Ответ от сервера
    :param routes: Номер транспортной ветки
    :param limit: Кол-во подходящего транспорта
    :return:
    """
    now = datetime.now(tz=timezone(offset=timedelta(hours=5)))
    current_time = float(now.hour * 60 + now.minute)
    route_ids = {route.mr_id for route in routes}
    arrivals: list[ArrivalRoute] = []
    for arrival_raw in arrival_response:
        arrival = from_dict(data_class=ArrivalRoute, data=arrival_raw)
        if arrival.mr_id not in route_ids:
            continue
        arrivals.append(arrival)
    arrivals = sorted(
        filter(lambda x: x.get_time() > current_time, arrivals),
        key=lambda x: x.get_time(),
        reverse=False,
    )
    return arrivals[:limit]
