from pydantic import BaseModel, Field


class DoubleGisSuggestRequests(BaseModel):
    lat: float | None = None
    lon: float | None = None
    search: str | None = None


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
    type: str | None = None  # example: forward, backward


class DoubleGisSuggestionItem(BaseModel):
    directions: list[DoubleGisSuggestionDirectionItem] = Field(default_factory=list)
    from_name: str | None = None
    id: str | None = None
    name: str | None = None
    subtype: str | None = None  # example: bus
    to_name: str | None = None
    type: str | None = None  # example: route


class DoubleGisSuggestResponseResult(BaseModel):
    items: list[DoubleGisSuggestionItem] = Field(default_factory=list)
    total: int = 0


class DoubleGisSuggestResponse(BaseModel):
    result: DoubleGisSuggestResponseResult | None = None
