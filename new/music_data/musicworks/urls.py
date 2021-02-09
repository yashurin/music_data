from django.conf.urls import url
from django.urls import path
from musicworks import views


urlpatterns = [
	path('', views.default),
	url(r'^musicworks/$', views.music_works_list),
	url(r'^(?P<iswc>\w+)/$', views.music_work),
]
