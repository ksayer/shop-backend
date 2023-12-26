from django.urls import path

from content.api.views import ContentBlockListAPIView

urlpatterns = [
    path('content_blocks/', ContentBlockListAPIView.as_view(), name='content_block_api')
]
