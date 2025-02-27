import base64
import io
import re
from typing import Any, Union

import PIL
from PIL.Image import Image

from enum import Enum


class Task(Enum):
    TEXT_GENERATION = "text_generation"
    IMAGE_TEXT_TO_TEXT = "image_text_to_text"

    TEXT_TO_IMAGE = "text_to_image"

    TEXT_TO_EMBEDDING = "text_embedding"
    IMAGE_TEXT_TO_EMBEDDING = "image_text_embedding"

    AUDIO_TO_TEXT = "audio_to_text"


def encode_image(image_input: Union[str, bytes, Image]) -> str:
    """
    Encodes an image into a base64 string with PNG encoding.

    Args:
        image_input (Union[str, bytes, Image.Image]): The image to encode. Can be a file path (str),
        raw image bytes (bytes), or a PIL Image object.

    Returns:
        str: Base64-encoded PNG image string.
    """
    if isinstance(image_input, Image):
        image = image_input
    elif isinstance(image_input, bytes):
        image = PIL.Image.open(io.BytesIO(image_input))
    elif isinstance(image_input, str):
        with open(image_input, "rb") as image_file:
            image = PIL.Image.open(image_file)
    else:
        raise TypeError("Unsupported input type. Must be str (file path), bytes, or PIL.Image.Image.")

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    png_bytes = buffered.getvalue()
    return base64.b64encode(png_bytes).decode("utf-8")


def is_url(path: str) -> bool:
    url_pattern = re.compile(r"^[a-zA-Z][a-zA-Z\d+\-.]*://")
    return bool(url_pattern.match(path))


def contains_image(inputs: Any) -> bool:
    """
    Determines if the input contains an image.

    This function checks for the presence of an image within the given input, considering three scenarios:
    1. The input is an image instance.
    2. The input is a list, and one or more elements in the list contain an image.
    3. The input is a dictionary, and one or more values in the dictionary contain an image (commonly for chat-based inputs).
    """
    if isinstance(inputs, list):
        return any(contains_image(item) for item in inputs)
    elif isinstance(inputs, dict):
        return any(contains_image(value) for value in inputs.values())
    elif isinstance(inputs, Image):
        return True
    return False


def inline_defs(schema):
    if "$defs" in schema:
        defs = schema.pop("$defs")
        resolved = set()

        while True:
            remaining_refs = False

            for key, value in defs.items():
                ref_path = f"#/$defs/{key}"
                if ref_path not in resolved:
                    replace_refs(schema, ref_path, value)
                    replace_refs(defs, ref_path, value)
                    resolved.add(ref_path)
                    remaining_refs = True

            if not remaining_refs:
                break

    return schema


def replace_refs(obj, ref_path, definition):
    if isinstance(obj, dict):
        for key, value in list(obj.items()):
            if key == "$ref" and value == ref_path:
                obj.clear()
                obj.update(definition)
            else:
                replace_refs(value, ref_path, definition)
    elif isinstance(obj, list):
        for item in obj:
            replace_refs(item, ref_path, definition)
