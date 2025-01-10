from application.clients.doublegis.routings.client import DoubleGisSearchSchedule
from application.clients.doublegis.suggests.client import DoubleGisSuggests
from application.config import API_DOUBLE_GIS_WEB, API_DOUBLE_GIS_SERVICE
from application.handlers.handlers import YandexHandler
from application.services.address_to_geo_service_double_gis import AddressToGeoServiceDoubleGis
from application.services.search_schedule_service_double_gis import SearchScheduleServiceDoubleGis


class DI:
    def __init__(self):
        self.double_gis_schedule = DoubleGisSearchSchedule(security_key=API_DOUBLE_GIS_WEB)
        self.double_gis_suggests = DoubleGisSuggests(security_key=API_DOUBLE_GIS_SERVICE)
        self.address_to_geo_double_gis = AddressToGeoServiceDoubleGis()
        self.search_schedule_double_gis = SearchScheduleServiceDoubleGis(
            search_schedule=self.double_gis_schedule,
            suggestion=self.double_gis_suggests,
        )

    def yandex_handler(self) -> YandexHandler:
        return YandexHandler(
            address_to_geo=self.address_to_geo_double_gis,
            search_schedule=self.search_schedule_double_gis,
        )
