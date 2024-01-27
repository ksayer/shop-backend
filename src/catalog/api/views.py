from django.db.models import Prefetch
from rest_framework import generics

from catalog.api.serializers import GroupListSerializer, ModelListSerializer
from catalog.models import Group, Model, Category


class ModelListApiView(generics.ListAPIView):
    queryset = Model.objects.for_catalog()
    serializer_class = ModelListSerializer
    filterset_fields = {
        'category__slug': ['in'],
        'category__group__slug': ['in'],
        'modifications__products__property__power__id': ['in'],
        'modifications__products__property__size__id': ['in'],
        'modifications__products__property__beam__id': ['in'],
        'modifications__products__property__beam_angle__id': ['in'],
        'modifications__products__property__color_index__id': ['in'],
        'modifications__products__property__color_temperature__id': ['in'],
        'modifications__products__property__body_color__id': ['in'],
        'modifications__products__property__frame_color__id': ['in'],
        'modifications__products__property__cover_color__id': ['in'],
        'modifications__products__property__dimming__id': ['in'],
        'modifications__products__property__protection__id': ['in'],
        'category__group__active': ['exact'],
    }


class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.annotate_filters().prefetch_related(
        Prefetch('categories', Category.objects.annotate_filters())
    ).order_by('ordering')
    serializer_class = GroupListSerializer
    filterset_fields = {"active": ['exact'], "slug": ['in']}
