from django.urls import path

from catalog.api.views import GroupListAPIView, ModelListApiView, ModelRetrieveApiView

app_name = 'catalog'

urlpatterns = [
    path('groups/', GroupListAPIView.as_view(), name='group_list_api'),
    path('models/', ModelListApiView.as_view(), name='model_list_api'),
    path('models/<slug:slug>/', ModelRetrieveApiView.as_view(), name='model_retrieve_api'),
]
