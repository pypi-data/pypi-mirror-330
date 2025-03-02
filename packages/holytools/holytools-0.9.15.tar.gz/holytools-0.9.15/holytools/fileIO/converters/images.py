from __future__ import annotations

import base64
from enum import Enum
from io import BytesIO

import PIL.Image as ImgHandler
from PIL import Image


class ImageConverter:
    PNG_MODES = ['L', 'LA', 'RGB', 'RGBA', 'P']
    JPG_MODES = ['L', 'RGB', 'CMYK']

    @classmethod
    def convert_format(cls, image: Image, target_format : ImageFormat) -> Image:
        if not image.format:
            raise TypeError(f'Given image {image} has no format')
        if not image.format.lower() in ImageFormat.get_all_formats():
            raise TypeError(f'Given image {image} has unsupported format: {image.format}')
        if not target_format in ImageFormat.get_all_formats():
            raise TypeError(f'Conversion to format {target_format} is not supported')
        if not ImageConverter._is_valid(image=image):
            raise TypeError(f'Image mode {image.mode} is invalid for format {image.format}')

        new_format = target_format.value.upper()
        if new_format in ['JPG', 'JPEG'] and not image.mode in cls.JPG_MODES:
            image = ImageConverter.to_rgb(image)
        if new_format == 'PNG' and not image.mode in cls.PNG_MODES:
            image = ImageConverter.to_rgba(image)
        else:
            image = image

        return ImageConverter._reload_as_fmt(image=image, target_format=target_format.value)

    @staticmethod
    def to_rgb(img : Image):
        new_img = ImgHandler.new('RGB', img.size, (255, 255, 255))
        rgb_content = img.convert('RGB')
        new_img.paste(rgb_content, mask=img.split()[-1])

        return ImageConverter._reload_as_fmt(new_img, target_format=img.format)

    @staticmethod
    def to_rgba(img):
        new_img = img.convert('RGBA')
        return ImageConverter._reload_as_fmt(new_img, target_format=img.format)

    @classmethod
    def _is_valid(cls, image: Image) -> bool:
        if not image.format.lower() in ImageFormat.get_all_formats():
            raise TypeError(f'Image format {image.format} is not supported')

        if image.format.upper() == 'PNG':
            return image.mode in cls.PNG_MODES
        elif image.format.upper() in ['JPEG', 'JPG']:
            return image.mode in cls.JPG_MODES
        return False

    @staticmethod
    def _reload_as_fmt(image : Image, target_format : str):
        buffer = BytesIO()
        image.save(buffer, format=target_format)
        buffer.seek(0)
        return ImgHandler.open(buffer)

    # --------------------------------------------------------------
    # serialization

    @staticmethod
    def as_bytes(image: Image) -> bytes:
        if image.format is None:
            raise TypeError(f'Given image {image} has no format')

        buffer = BytesIO()
        image.save(buffer, format=image.format)
        img_bytes = buffer.getvalue()
        return img_bytes

    @staticmethod
    def from_bytes(img_bytes : bytes) -> Image:
        buffer = BytesIO(img_bytes)
        image = ImgHandler.open(buffer)
        return image

    @staticmethod
    def from_base64_str(s : str) -> Image:
        if "base64," in s:
            s = s.split("base64,")[-1]
        image_data = base64.b64decode(s)
        image = ImgHandler.open(BytesIO(image_data))
        return image

    @staticmethod
    def to_base64_str(image: Image) -> str:
        byte_content = ImageConverter.as_bytes(image=image)
        base64_content = base64.b64encode(byte_content).decode('utf-8')
        return base64_content


class ImageFormat(Enum):
    PNG = 'PNG'
    JPG = 'JPG'
    JPEG = 'JPEG'

    @classmethod
    def get_all_formats(cls) -> list[ImageFormat]:
        return [member for member in cls]

    def __eq__(self, other):
        if isinstance(other,str):
            return self.value.upper() == other.upper()
        elif isinstance(other, ImageFormat):
            return self.value == other.value
        return False

    def __str__(self):
        return self.value