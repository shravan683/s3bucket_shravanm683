
from django.urls import path
from .views import S3Uploader

urlpatterns = [
    path('upload/', S3Uploader.as_view(), name='s3-upload'),
]
