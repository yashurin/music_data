from django.conf.urls import url, include
from django.urls import path

urlpatterns = [
    url(r'^', include('musicworks.urls')),
]
