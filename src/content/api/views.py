from django.db.models import Prefetch
from rest_framework import generics

from content.api.serializers import ContentBlockSerializer
from content.models import Banner, ContentBlock, ModelCard


class ContentBlockListAPIView(generics.ListAPIView):
    queryset = ContentBlock.objects.prefetch_related(
        Prefetch('banners', Banner.objects.select_related('image').prefetch_related('buttons')),
        Prefetch('model_cards', ModelCard.objects.select_related('model__image')),
    )

    serializer_class = ContentBlockSerializer
    filterset_fields = ['page__slug']
