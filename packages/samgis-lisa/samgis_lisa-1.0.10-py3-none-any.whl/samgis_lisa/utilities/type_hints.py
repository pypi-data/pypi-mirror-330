"""custom type hints"""
from pydantic import BaseModel
from samgis_web.utilities.type_hints import RawBBox


class StringPromptApiRequestBody(BaseModel):
    """Input lambda request validator type (not yet parsed)"""
    id: str = ""
    bbox: RawBBox
    string_prompt: str
    zoom: int | float
    source_type: str = "OpenStreetMap.Mapnik"
    debug: bool = False
