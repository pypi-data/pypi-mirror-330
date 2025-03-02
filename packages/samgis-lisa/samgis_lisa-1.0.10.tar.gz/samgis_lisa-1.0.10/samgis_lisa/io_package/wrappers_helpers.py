"""lambda helper functions"""
from typing import Dict

from lisa_on_cuda.utils.app_helpers import get_cleaned_input
from samgis_web.web.web_helpers import get_url_tile, get_source_name

from samgis_lisa import app_logger
from samgis_lisa.utilities.type_hints import StringPromptApiRequestBody


def get_parsed_bbox_points_with_string_prompt(request_input: StringPromptApiRequestBody) -> Dict:
    """
        Parse the raw input request into bbox, prompt string and zoom

        Args:
            request_input: input dict

        Returns:
            dict with bounding box, prompt string and zoom
        """

    app_logger.info(f"try to parsing input request: {type(request_input)}, {request_input}...")
    if isinstance(request_input, str):
        app_logger.info(f"string/json input, parsing it to {type(StringPromptApiRequestBody)}...")
        request_input = StringPromptApiRequestBody.model_validate_json(request_input)
        app_logger.info(f"parsed input, now of type {type(request_input)}...")

    bbox = request_input.bbox
    app_logger.debug(f"request bbox: {type(bbox)}, value:{bbox}.")
    ne = bbox.ne
    sw = bbox.sw
    app_logger.debug(f"request ne: {type(ne)}, value:{ne}.")
    app_logger.debug(f"request sw: {type(sw)}, value:{sw}.")
    ne_latlng = [float(ne.lat), float(ne.lng)]
    sw_latlng = [float(sw.lat), float(sw.lng)]
    new_zoom = int(request_input.zoom)
    cleaned_prompt = get_cleaned_input(request_input.string_prompt)

    app_logger.debug(f"bbox => {bbox}.")
    app_logger.debug(f'request_input-prompt cleaned => {cleaned_prompt}.')

    app_logger.info("unpacking elaborated request...")
    return {
        "bbox": [ne_latlng, sw_latlng],
        "prompt": cleaned_prompt,
        "zoom": new_zoom,
        "source": get_url_tile(request_input.source_type),
        "source_name": get_source_name(request_input.source_type)
    }
