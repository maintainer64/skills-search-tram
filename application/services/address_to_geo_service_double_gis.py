from application.clients.doublegis.suggests.client import DoubleGisSuggests
from application.clients.doublegis.suggests.models import DoubleGisSuggestRequests
from application.services.address_to_geo_service_abs import AddressToGeoServiceABC, GeoPoint


class AddressToGeoServiceDoubleGis(AddressToGeoServiceABC):
    def __init__(
        self,
        suggestion: DoubleGisSuggests,
    ):
        self.suggestion = suggestion

    async def get_by_address(self, address: str) -> GeoPoint | None:
        response = await self.suggestion.suggests_building(params=DoubleGisSuggestRequests(search=address))
        if not response.result:
            return None
        for item in response.result.items:
            point = item.get_point()
            address = item.get_address_name()
            if not (item.id and point and address and item.type == "building"):
                continue
            response_region = await self.suggestion.region_by_branch_id(branch_id=item.id)
            if not response_region.result or not response_region.result.items:
                continue
            region = response_region.result.items[0]
            return GeoPoint(
                lat=point[0],
                lon=point[1],
                address=address,
                time_zone_offset=region.get_utc_offset() or 0,
                code=region.get_project_code() or "",
            )
        return None
