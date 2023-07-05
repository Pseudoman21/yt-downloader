from django.urls import path
from . import views

urlpatterns = [
    path('', views.download_youtube_video, name='download_youtube_video'),
]
