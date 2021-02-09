from django.contrib.postgres.fields import ArrayField
from django.db import models


class MusicWork(models.Model):
	title = models.CharField(max_length=200, blank=True, default='')
	contributors = ArrayField(models.CharField(max_length=70), blank=True)
	iswc = models.CharField(max_length=11, blank=True, default='')


