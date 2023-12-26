from django.db import models
from filer.fields.image import FilerImageField


class ImagePreset(models.Model):
    class DeviceType(models.TextChoices):
        DESKTOP = 'desktop'
        MOBILE = 'mobile'

    internal_name = models.CharField(max_length=64)
    type = models.CharField(
        max_length=7,
        choices=DeviceType.choices,
    )
    max_width = models.PositiveSmallIntegerField()
    max_height = models.PositiveSmallIntegerField()
    quality = models.PositiveSmallIntegerField(default=80)

    def __str__(self):
        return f'{self.id}: {self.type}'

    class Meta:
        db_table = 'image_preset'


class AdaptiveImageSetting(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    desktop = models.OneToOneField(
        ImagePreset,
        on_delete=models.CASCADE,
        related_name='desk_image',
    )
    mobile = models.OneToOneField(
        ImagePreset,
        on_delete=models.CASCADE,
        related_name='mob_image',
    )
    is_image_compress = models.BooleanField(
        verbose_name='compress images?',
        default=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'adaptive_image_setting'


class AdaptiveImage(models.Model):
    original = FilerImageField(
        on_delete=models.CASCADE,
        related_name='original_images',
    )
    desktop = FilerImageField(
        on_delete=models.CASCADE,
        related_name='desktop_images',
        blank=True,
        null=True,
    )
    mobile = FilerImageField(
        on_delete=models.CASCADE,
        related_name='mobile_images',
        blank=True,
        null=True,
    )
    is_compressed = models.BooleanField(
        verbose_name='compressed?',
        default=False,
    )
    setting = models.ForeignKey(
        AdaptiveImageSetting,
        on_delete=models.PROTECT,
        related_name='images',
    )

    def __str__(self):
        return self.original.original_filename

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.is_compressed:
            from adaptive_images.tasks import compress_and_save_images_task

            compress_and_save_images_task.apply_async((self.id,), countdown=2)

    class Meta:
        db_table = 'adaptive_image'
