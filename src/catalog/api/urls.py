from django.urls import path

from catalog.api.views import GroupListAPIView, ModelListApiView

urlpatterns = [
    path('groups/', GroupListAPIView.as_view(), name='group_list_api'),
    path('models/', ModelListApiView.as_view(), name='model_list_api'),
]
