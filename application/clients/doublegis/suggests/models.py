from pydantic import BaseModel, Field


class DoubleGisSuggestRequests(BaseModel):
    lat: float | None = None
    lon: float | None = None
    search: str | None = None


# Suggest Route
class DoubleGisSuggestionGeometry(BaseModel):
    centroid: str | None = None
    selection: str | None = None

    @staticmethod
    def parse_point(point: str | None) -> tuple[float, float] | None:
        try:
            lon, lat = point.removeprefix("POINT(").removesuffix(")").split(" ")  # type: ignore[union-attr]
            return float(lat), float(lon)
        except Exception:
            return None

    def point(self) -> tuple[float, float]:
        """
        Returns the point of the suggestion
        :return: geometry latitude, longitude
        """
        for point in (self.centroid, self.selection):
            parsed = self.parse_point(point)
            if parsed is not None:
                return parsed
        return 0, 0


class DoubleGisSuggestionPlatformItem(BaseModel):
    geometry: DoubleGisSuggestionGeometry | None = None
    id: str | None = None
    name: str | None = None
    station_id: str | None = None


class DoubleGisSuggestionDirectionItem(BaseModel):
    geometry: DoubleGisSuggestionGeometry | None = None
    id: str | None = None
    platforms: list[DoubleGisSuggestionPlatformItem] = Field(default_factory=list)
    type: str | None = Field(None, examples=["forward", "backward"])


class DoubleGisSuggestionItem(BaseModel):
    directions: list[DoubleGisSuggestionDirectionItem] = Field(default_factory=list)
    from_name: str | None = None
    id: str | None = None
    name: str | None = None
    subtype: str | None = Field(None, examples=["bus"])
    to_name: str | None = None
    type: str | None = Field(None, examples=["route"])


class DoubleGisSuggestResponseResult(BaseModel):
    items: list[DoubleGisSuggestionItem] = Field(default_factory=list)
    total: int = 0


class DoubleGisSuggestResponse(BaseModel):
    result: DoubleGisSuggestResponseResult | None = None


# Suggest Buildings


class DoubleGisSuggestionBuildingPoint(BaseModel):
    lat: float | None = None
    lon: float | None = None


class DoubleGisSuggestionBuildingItem(BaseModel):
    address_name: str | None = None
    full_address_name: str | None = None
    full_name: str | None = None
    id: str | None = None
    name: str | None = None
    point: DoubleGisSuggestionBuildingPoint | None = None
    type: str | None = Field(None, examples=["building"])

    def get_address_name(self) -> str:
        return self.full_address_name or self.full_name or self.address_name or self.name or ""

    def get_point(self) -> tuple[float, float] | None:
        """
        Получаем проект города (код 2ГИС) для получения расписания
        :return: Получаем последний (-1) код
        """
        if self.point and self.point.lat and self.point.lon:
            return self.point.lat, self.point.lon
        return None


class DoubleGisSuggestBuildingResponseResult(BaseModel):
    items: list[DoubleGisSuggestionBuildingItem] = Field(default_factory=list)
    total: int = 0


class DoubleGisSuggestBuildingResponse(BaseModel):
    result: DoubleGisSuggestBuildingResponseResult | None = None


# Suggest Region
class DoubleGisSuggestionRegionTimezone(BaseModel):
    name: str | None = Field(None, examples=["Asia/Yekaterinburg"])
    offset: int | None = Field(None, examples=["300"])


class DoubleGisSuggestionRegionItem(BaseModel):
    code: str | None = Field(None, examples=["perm"])
    id: str | None = Field(None, examples=["16"])
    name: str | None = Field(None, examples=["Пермь"])
    time_zone: DoubleGisSuggestionRegionTimezone | None = Field(None, examples=["Пермь"])
    type: str | None = Field(None, examples=["region"])
    uri_code: str | None = Field(None, examples=["perm"])

    def get_utc_offset(self) -> int | None:
        return self.time_zone.offset if self.time_zone else None

    def get_project_code(self) -> str | None:
        return self.uri_code or self.code


class DoubleGisSuggestRegionResponseResult(BaseModel):
    items: list[DoubleGisSuggestionRegionItem] = Field(default_factory=list)
    total: int = 0


class DoubleGisSuggestRegionResponse(BaseModel):
    result: DoubleGisSuggestRegionResponseResult | None = None
