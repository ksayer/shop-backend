from rest_framework import generics

from catalog.api.serializers import ModelListSerializer, GroupListSerializer
from catalog.models import Model, Group


class ModelListApiView(generics.ListAPIView):
    queryset = Model.objects.for_catalog()
    serializer_class = ModelListSerializer


class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.prefetch_related('categories')
    serializer_class = GroupListSerializer
