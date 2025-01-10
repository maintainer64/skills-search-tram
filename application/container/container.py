from application.clients.doublegis.routings.client import DoubleGisSearchSchedule
from application.clients.doublegis.suggests.client import DoubleGisSuggests
from application.config import API_DOUBLE_GIS_WEB, API_DOUBLE_GIS_SERVICE


class DI:
    def __init__(self):
        self.double_gis_schedule = DoubleGisSearchSchedule(security_key=API_DOUBLE_GIS_WEB)
        self.double_gis_suggests = DoubleGisSuggests(security_key=API_DOUBLE_GIS_SERVICE)
