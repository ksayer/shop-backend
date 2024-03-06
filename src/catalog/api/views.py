from django.db.models import Prefetch
from rest_framework import generics

from catalog.api.serializers import (
    GroupListSerializer,
    ModelListSerializer,
    ModelRetrieveSerializer,
)
from catalog.models import (
    Banner,
    Category,
    Gallery,
    Group,
    Model,
    Modification,
    Product,
)


class ModelListApiView(generics.ListAPIView):
    queryset = Model.objects.for_catalog().order_by('ordering')
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


class ModelRetrieveApiView(generics.RetrieveAPIView):
    queryset = (
        Model.objects.annotate_prices()
        .select_related('category__group')
        .prefetch_related(
            Prefetch('banners', Banner.objects.select_related('image')),
            Prefetch('gallery', Gallery.objects.select_related('image')),
            Prefetch(
                'modifications',
                Modification.objects.prefetch_related(
                    Prefetch(
                        'products',
                        Product.objects.select_related(
                            'scheme',
                            'image',
                            'property__power',
                            'property__beam',
                            'property__color_index',
                            'property__color_temperature',
                            'property__body_color',
                            'property__frame_color',
                            'property__cover_color',
                            'property__dimming',
                            'property__beam_angle',
                            'property__protection',
                            'property__size',
                        ),
                    )
                ),
            ),
        )
    )
    serializer_class = ModelRetrieveSerializer
    lookup_field = 'slug'


class GroupListAPIView(generics.ListAPIView):
    queryset = (
        Group.objects.annotate_filters()
        .prefetch_related(Prefetch('categories', Category.objects.annotate_filters()))
        .order_by('ordering')
    )
    serializer_class = GroupListSerializer
    filterset_fields = {"active": ['exact'], "slug": ['in']}
