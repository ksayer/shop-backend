from celery import shared_task

from adaptive_images.services import process_adaptive_image


@shared_task
def compress_and_save_images_task(id: int):
    from .models import AdaptiveImage

    image_instance = AdaptiveImage.objects.get(id=id)
    process_adaptive_image(image_instance)
