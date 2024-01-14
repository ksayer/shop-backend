from rest_framework import generics

from catalog.api.serializers import ModelListSerializer
from catalog.models import Model


class ModelListApiView(generics.ListAPIView):
    queryset = Model.objects.for_catalog()
    serializer_class = ModelListSerializer
