from django.urls import path

from catalog.api.views import ModelListApiView

urlpatterns = [
    path('models/', ModelListApiView.as_view(), name='model_list_api')
]
