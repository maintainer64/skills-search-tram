from application.services.address_to_geo_service_abs import AddressToGeoServiceABC, GeoPoint


class AddressToGeoServiceDoubleGis(AddressToGeoServiceABC):
    async def get_by_address(self, address: str) -> GeoPoint:
        return GeoPoint(
            lat=10.01,
            lon=10.02,
            address="Москва",
            city_alias_code="moscow",
        )
