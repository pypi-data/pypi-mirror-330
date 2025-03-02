from datetime import datetime
from typing import Callable

from samgis_core.utilities.type_hints import LlistFloat, DictStrInt
from samgis_web.io_package.geo_helpers import get_vectorized_raster_as_geojson
from samgis_web.io_package.raster_helpers import write_raster_tiff, write_raster_png
from samgis_web.io_package.tms2geotiff import download_extent
from samgis_web.utilities.constants import DEFAULT_URL_TILES

from samgis_lisa import app_logger
from samgis_lisa.utilities.constants import LISA_INFERENCE_FN


msg_write_tmp_on_disk = "found option to write images and geojson output..."


def load_model_and_inference_fn(
        inference_function_name_key: str, inference_decorator: Callable = None, device_map="auto", device="cuda"
    ):
    """
    If missing, instantiate the inference function as reference the inference_function_name_key
    using the global object models_dict

    Args:
        inference_function_name_key: machine learning model name
        inference_decorator: inference decorator like ZeroGPU (e.g. spaces.GPU)
        device_map (`str` or `Dict[str, Union[int, str, torch.device]]` or `int` or `torch.device`, *optional*):
            A map that specifies where each submodule should go. It doesn't need to be refined to each
            parameter/buffer name, once a given module name is inside, every submodule of it will be sent to the
            same device. If we only pass the device (*e.g.*, `"cpu"`, `"cuda:1"`, `"mps"`, or a GPU ordinal rank
            like `1`) on which the model will be allocated, the device map will map the entire model to this
            device. Passing `device_map = 0` means put the whole model on GPU 0.
            In this specific case 'device_map' should avoid a CUDA init RuntimeError when during model loading on
            ZeroGPU huggingface hardware
        device: device useful with 'device_map'. In this specific case 'device_map' should avoid a CUDA init
            RuntimeError when during model loading on ZeroGPU huggingface hardware
    """
    from lisa_on_cuda.utils import app_helpers
    from samgis_lisa.prediction_api.global_models import models_dict

    if models_dict[inference_function_name_key]["inference"] is None:
        msg = f"missing inference function {inference_function_name_key}, "
        msg += "instantiating it now"
        if inference_decorator:
            msg += f" using the inference decorator {inference_decorator.__name__}"
        msg += "..."
        app_logger.info(msg)
        parsed_args = app_helpers.parse_args([])
        inference_fn = app_helpers.get_inference_model_by_args(
            parsed_args,
            internal_logger0=app_logger,
            inference_decorator=inference_decorator,
            device_map=device_map,
            device=device
        )
        models_dict[inference_function_name_key]["inference"] = inference_fn


def lisa_predict(
        bbox: LlistFloat,
        prompt: str,
        zoom: float,
        inference_function_name_key: str = LISA_INFERENCE_FN,
        source: str = DEFAULT_URL_TILES,
        source_name: str = None,
        inference_decorator: Callable = None,
        device_map="auto",
        device="cuda",
) -> DictStrInt:
    """
    Return predictions as a geojson from a geo-referenced image using the given input prompt.

    1. if necessary instantiate a segment anything machine learning instance model
    2. download a geo-referenced raster image delimited by the coordinates bounding box (bbox)
    3. get a prediction image from the segment anything instance model using the input prompt
    4. get a geo-referenced geojson from the prediction image

    Args:
        bbox: coordinates bounding box
        prompt: machine learning input prompt
        zoom: Level of detail
        inference_function_name_key: machine learning model name
        source: xyz
        source_name: name of tile provider
        inference_decorator: inference decorator like ZeroGPU (spaces.GPU)
        device_map (`str` or `Dict[str, Union[int, str, torch.device]]` or `int` or `torch.device`, *optional*):
            A map that specifies where each submodule should go. It doesn't need to be refined to each
            parameter/buffer name, once a given module name is inside, every submodule of it will be sent to the
            same device. If we only pass the device (*e.g.*, `"cpu"`, `"cuda:1"`, `"mps"`, or a GPU ordinal rank
            like `1`) on which the model will be allocated, the device map will map the entire model to this
            device. Passing `device_map = 0` means put the whole model on GPU 0.
            In this specific case 'device_map' should avoid a CUDA init RuntimeError when during model loading on
            ZeroGPU huggingface hardware
        device: device useful with 'device_map'. In this specific case 'device_map' should avoid a CUDA init
            RuntimeError when during model loading on ZeroGPU huggingface hardware

    Returns:
        dict containing the output geojson, the geojson shapes number and a machine learning textual output string
    """
    from os import getenv
    from samgis_lisa.prediction_api.global_models import models_dict

    if source_name is None:
        source_name = str(source)

    msg_start = "start lisa inference"
    if inference_decorator:
        msg_start += f", using the inference decorator {inference_decorator.__name__}"
    msg_start += "..."
    app_logger.info(msg_start)
    app_logger.debug(f"type(source):{type(source)}, source:{source},")
    app_logger.debug(f"type(source_name):{type(source_name)}, source_name:{source_name}.")

    load_model_and_inference_fn(
        inference_function_name_key, inference_decorator=inference_decorator, device_map=device_map, device=device
    )
    app_logger.debug(f"using a '{inference_function_name_key}' instance model...")
    inference_fn = models_dict[inference_function_name_key]["inference"]
    app_logger.info(f"loaded inference function '{inference_fn.__name__}'.")

    pt0, pt1 = bbox
    app_logger.info(f"tile_source: {source}: downloading geo-referenced raster with bbox {bbox}, zoom {zoom}.")
    img, transform = download_extent(w=pt1[1], s=pt1[0], e=pt0[1], n=pt0[0], zoom=zoom, source=source)
    app_logger.info(
        f"img type {type(img)} with shape/size:{img.size}, transform type: {type(transform)}, transform:{transform}.")
    folder_write_tmp_on_disk = getenv("WRITE_TMP_ON_DISK", "")
    prefix = f"w{pt1[1]},s{pt1[0]},e{pt0[1]},n{pt0[0]}_"
    if bool(folder_write_tmp_on_disk):
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        app_logger.info(msg_write_tmp_on_disk + f"with coords {prefix}, shape:{img.shape}, {len(img.shape)}.")
        if img.shape and len(img.shape) == 2:
            write_raster_tiff(img, transform, f"{source_name}_{prefix}_{now}_", "raw_tiff", folder_write_tmp_on_disk)
        if img.shape and len(img.shape) == 3 and img.shape[2] == 3:
            write_raster_png(img, transform, f"{source_name}_{prefix}_{now}_", "raw_img", folder_write_tmp_on_disk)
    else:
        app_logger.info("keep all temp data in memory...")

    app_logger.info(f"lisa_zero, source_name:{source_name}, source_name type:{type(source_name)}.")
    app_logger.info(f"lisa_zero, prompt type:{type(prompt)}.")
    app_logger.info(f"lisa_zero, prompt:{prompt}.")
    prompt_str = str(prompt)
    app_logger.info(f"lisa_zero, img type:{type(img)}.")
    embedding_key = f"{source_name}_z{zoom}_{prefix}"
    _, mask, output_string = inference_fn(input_str=prompt_str, input_image=img, embedding_key=embedding_key)
    app_logger.info(f"lisa_zero, output_string type:{type(output_string)}.")
    app_logger.info(f"lisa_zero, mask_output type:{type(mask)}.")
    app_logger.info(f"created output_string '{output_string}', preparing conversion to geojson...")
    return {
        "output_string": output_string,
        **get_vectorized_raster_as_geojson(mask, transform)
    }
