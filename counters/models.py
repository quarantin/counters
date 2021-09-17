from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from datetime import datetime


class Counter(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=64)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name

class Record(models.Model):
	counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
	created = models.DateTimeField(default=timezone.now)
