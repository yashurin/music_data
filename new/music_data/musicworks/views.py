from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.renderers import JSONRenderer
from musicworks.models import MusicWork
from musicworks.serializers import MusicWorkSerializer


DEFAULT_RESPONSE = (
	'<h2>Welcome to the Music Works Demo Application.<br>',
	'To list all available music works, use ',
	'<a href="http://localhost:8000/musicworks/">http://localhost:8000/musicworks/</a><br>',
	'To get detais for a music work with a iswc code, use an URL like<br>',
	'<a href="http://localhost:8000/T9214745718/">http://localhost:8000/T9214745718/</a> <br>',
	'where T9214745718 is a iswc code.</h2>'
)

ERROR_RESPONSE = {
	'Error': 'There is no such music work in the database.'
}
	

class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
@require_http_methods(['GET'])
def default(request):
	return HttpResponse(DEFAULT_RESPONSE)


@csrf_exempt
@require_http_methods(['GET'])
def music_works_list(request):
	music_works = MusicWork.objects.all()
	music_works_serializer = MusicWorkSerializer(music_works, many=True)
	return JSONResponse(music_works_serializer.data)


@csrf_exempt
@require_http_methods(['GET'])
def music_work(request, iswc):
	try:
		music_work = MusicWork.objects.get(iswc=iswc)
		music_work_serializer = MusicWorkSerializer(music_work)
		return JSONResponse(music_work_serializer.data)		
	except MusicWork.DoesNotExist:
		return JSONResponse(ERROR_RESPONSE)

