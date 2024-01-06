from rest_framework import generics

from content.api.serializers import ContentBlockSerializer
from content.models import ContentBlock


class ContentBlockListAPIView(generics.ListAPIView):
    queryset = ContentBlock.objects.prefetch_related('banners__buttons')
    serializer_class = ContentBlockSerializer
    filterset_fields = ['page__slug']
