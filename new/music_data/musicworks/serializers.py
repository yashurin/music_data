from rest_framework import serializers
from musicworks.models import MusicWork


class MusicWorkSerializer(serializers.Serializer):
	pk = serializers.IntegerField(read_only=True)
	title = serializers.CharField(max_length=200)
	contributors = serializers.ListField(child=serializers.CharField(max_length=70))
	iswc = serializers.CharField(max_length=11)

	def create(self, music_data):
		return MusicWork.objects.create(music_data)

	def update(self, instance, music_data):
		instance.title = music_data.get('title', instance.title)
		instance.contributors = music_data.get('contributors', instance.contributors)
		instance.iswc = music_data.get('iswc', instance.iswc)
		instance.save()
		return instance
		
