from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from enum import Enum

from pydantic import BaseModel

from .language import language_minutes, language_hours


class TransportType(str, Enum):
    Bus = "Автобус"
    Tram = "Трамвай"
    Trolley = "Троллейбус"


class SearchServiceTime(BaseModel):
    hour: int
    minute: int

    def text(self) -> str:
        now = datetime.now(tz=timezone(offset=timedelta(hours=5)))
        current_time = now.hour * 60 + now.minute
        minutes = (self.hour * 60 + self.minute) - current_time
        if 0 < minutes < 30:
            return f"через {minutes} {language_minutes(minutes)}"
        return f"в {self.hour} {language_hours(self.hour)} {self.minute} {language_minutes(self.minute)}"


class SearchServiceStation(BaseModel):
    last_station_title: str = ""
    times: list[SearchServiceTime] = []

    def text(self) -> str:
        if not self.times:
            return ""
        times = ". Затем ".join([x.text() for x in self.times])
        return f"До станции {self.last_station_title} прибудет {times}."


class SearchServiceStations(BaseModel):
    stations: list[SearchServiceStation] = []

    def text(self) -> str:
        if not self.stations:
            return "Не нашла подходящих маршрутов"
        return ".".join([x.text() for x in self.stations])


class SearchScheduleServiceABC(ABC):
    @abstractmethod
    async def get_transport(
        self,
        transport_query: str,
        transport_type: TransportType | None,
        lat: float,
        lon: float,
        city_code: str,
    ) -> SearchServiceStations:
        """
        Поиск подходящего маршрута и остановки
        :param transport_query: Номер транспорта маршрута
        :param transport_type: Тип транспорта
        :param lat: Точка дома где искать
        :param lon: Точка дома где искать
        :param city_code: Проект маршрутов в 2ГИС
        :return: Список маршрутов
        """
        ...

