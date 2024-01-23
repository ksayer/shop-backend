from rest_framework import generics

from catalog.api.serializers import GroupListSerializer, ModelListSerializer
from catalog.models import Group, Model


class ModelListApiView(generics.ListAPIView):
    queryset = Model.objects.for_catalog()
    serializer_class = ModelListSerializer
    filterset_fields = {
        'category__slug': ['in'],
        'category__group__slug': ['in'],
        'products__properties__group_id': ['in'],
    }


class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.annotate_filters().prefetch_related('categories').order_by('ordering')
    serializer_class = GroupListSerializer
    filterset_fields = {"active": ['exact'], "slug": ['in']}
