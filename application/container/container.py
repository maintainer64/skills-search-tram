from application.clients.doublegis.routings.client import DoubleGisSearchSchedule
from application.clients.doublegis.suggests.client import DoubleGisSuggests
from application.clients.doublegis.webapi.client import DoubleGisWebApiConfigParser
from application.config import API_DOUBLE_GIS_WEB, API_DOUBLE_GIS_SERVICE
from application.handlers.handlers import YandexHandler
from application.services.address_to_geo_service_double_gis import AddressToGeoServiceDoubleGis
from application.services.search_schedule_service_double_gis import SearchScheduleServiceDoubleGis


class DI:
    def __init__(self):
        verify_ssl = False
        timeout = 3.0
        self.double_gis_schedule = DoubleGisSearchSchedule(
            verify_ssl=verify_ssl,
            security_key=API_DOUBLE_GIS_WEB,
            timeout=timeout,
            config_parser=DoubleGisWebApiConfigParser(
                verify_ssl=verify_ssl,
                timeout=timeout,
            ),
        )
        self.double_gis_suggests = DoubleGisSuggests(
            security_key=API_DOUBLE_GIS_SERVICE,
            verify_ssl=verify_ssl,
            timeout=timeout,
        )
        self.address_to_geo_double_gis = AddressToGeoServiceDoubleGis(
            suggestion=self.double_gis_suggests,
        )
        self.search_schedule_double_gis = SearchScheduleServiceDoubleGis(
            search_schedule=self.double_gis_schedule,
            suggestion=self.double_gis_suggests,
        )

    def yandex_handler(self) -> YandexHandler:
        return YandexHandler(
            address_to_geo=self.address_to_geo_double_gis,
            search_schedule=self.search_schedule_double_gis,
        )
