"""
    The Image class contains the functions to convert image to bytes and vice versa.
"""

import bz2
import io
import numpy as np

from PIL import Image, ImageOps
from enum import Enum


class ContentType(str, Enum):
    """Reponse content type"""
    PNG = "image/png"
    JPEG = "image/jpeg"
    
class ImageMetaData():
    """Image Meta Data"""
    def __init__(self, format: str, mode: str, width: int, height: int):
        self.format = format
        self.mode = mode
        self.width = width
        self.height = height
    
    
def extract_meta_data_from_image_bytes(image: bytes) -> ImageMetaData:
    """Extract meta data from image bytes

    Args:
        image (bytes)

    Returns:
        ImageMetaData
    """
    img = Image.open(io.BytesIO(image))
    return ImageMetaData(img.format, img.mode, img.width, img.height)


def byte_to_pillow(image: Image) -> Image:
    """Convert bytes to Pillow Image

    Args:
        image (Image)

    Returns:
        Image
    """
    image = Image.open(io.BytesIO(image)).convert("RGBA").convert("RGB")
    return ImageOps.exif_transpose(image)

def bytes_to_base64(image: bytes) -> str:
    """Convert bytes to base64

    Args:
        image (bytes)

    Returns:
        str
    """
    return io.BytesIO(image).read().decode("utf-8").encode("base64")


def pillow_to_image(image: Image, image_type: str = "PNG") -> io.BytesIO:
    """Convert Pillow Image to bytes

    Args:
        image (Image)
        image_type (str, optional) Defaults to "PNG".

    Returns:
        io.BytesIO
    """
    if type(image) is np.ndarray:
        image = Image.fromarray(image)
    buf = io.BytesIO()
    image.save(buf, image_type.upper())
    buf.seek(0)
    return buf


def compress(image, image_type: str = "PNG") -> bytes:
    """Compress Pillow Image to bytes

    Args:
        image (_type_)
        image_type (str, optional): Defaults to "PNG".

    Returns:
        bytes
    """
    return bz2.compress(pillow_to_image(image, image_type).read())


def decompress(image: Image) -> Image:
    """Decompress bytes to Pillow Image

    Args:
        image (Image)

    Returns:
        Image
    """
    return byte_to_pillow(bz2.decompress(image))


def decompress_to_byte(image: Image) -> bytes:
    """Decompress bytes to Pillow Image

    Args:
        image (Image)

    Returns:
        bytes
    """
    return bz2.decompress(image)


def resize_image(image: bytes, width: int = 512, height: int = 512) -> Image:
    """Resize image

    Args:
        image (bytes)
        width (int, optional): Defaults to 512.
        height (int, optional): Defaults to 512.

    Returns:
        Image
    """
    img = Image.open(io.BytesIO(image), mode='r').convert("RGBA").convert("RGB")
    img = img.resize((width, height))
    return img
