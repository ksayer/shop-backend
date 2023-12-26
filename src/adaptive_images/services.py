import os.path
from io import BytesIO

import requests
from django.contrib.auth import get_user_model
from django.core.files import File
from filer.models.imagemodels import Image as FilerImage
from PIL import Image

from .models import AdaptiveImage
from .models.models import ImagePreset

LOWER_THRESHOLD_IMAGE_SIZE = 32076
User = get_user_model()


def get_image_properties(instance: AdaptiveImage, type: str) -> dict:
    img_preset = getattr(instance.setting, type)
    img_properties = {
        'max_width': img_preset.max_width,
        'max_height': img_preset.max_height,
        'quality': img_preset.quality,
    }
    return img_properties


def resize_image(img: Image, scale: float) -> Image:
    new_img_width = int(img.size[0] * scale)
    new_img_height = int(img.size[1] * scale)
    new_size = (new_img_width, new_img_height)
    return img.resize(new_size, Image.LANCZOS)


def get_resized_image_by_biggest_side(img, max_width: int, max_height: int) -> Image:
    if img.size[0] > max_width and img.size[1] > max_height:
        w_diff = max_width / img.size[0]
        h_diff = max_height / img.size[1]
        difference = w_diff if w_diff < h_diff else h_diff
        return resize_image(img, difference)
    if img.size[0] > max_width:
        difference = max_width / img.size[0]
        return resize_image(img, difference)
    if img.size[1] > max_height:
        difference = max_height / img.size[1]
        return resize_image(img, difference)
    return img


def save_resized_image(
    resized_img: Image, filename: str, path: str, quality: int, type: str
) -> tuple:
    _, img_format = os.path.splitext(path)
    if img_format == '.jpg':
        img_format = '.jpeg'
    binary_image = BytesIO()
    resized_img.save(
        binary_image,
        img_format[1:],
        quality=quality,
    )
    name, frmt = os.path.splitext(filename)
    name = f'{name}_{type}'
    resized_img_filename = name + frmt
    return binary_image, resized_img_filename


def get_processed_image(
    source_image: FilerImage,
    type: str,
    max_width: int,
    max_height: int,
    quality: int,
    **kwargs,
) -> FilerImage | None:
    if os.path.isfile(source_image.path):
        path = source_image.path
        image = Image.open(source_image.path)
    elif source_image.url:
        path = source_image.url
        image = Image.open(requests.get(source_image.url, stream=True).raw)
    else:
        return None

    resized_image = get_resized_image_by_biggest_side(image, max_width, max_height)
    if source_image.path.endswith('.png') and source_image.size > LOWER_THRESHOLD_IMAGE_SIZE:
        resized_image = resized_image.quantize(method=2)

    binary_image, resized_image_filename = save_resized_image(
        resized_image, source_image.original_filename, path, quality, type
    )

    owner = User.objects.get(id=source_image.owner_id)
    image_file_obj = File(binary_image, name=resized_image_filename)
    adapted_image = FilerImage.objects.create(
        owner=owner, original_filename=resized_image_filename, file=image_file_obj
    )
    return adapted_image


def process_adaptive_image(instance: AdaptiveImage) -> None:
    for type_key, value in ImagePreset.DeviceType.choices:
        properties = get_image_properties(
            instance,
            type_key,
        )
        image_field = get_processed_image(instance.original, type_key, **properties)
        setattr(instance, type_key, image_field)
    instance.is_compressed = True
    instance.save()
