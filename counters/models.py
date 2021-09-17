from django import forms
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tempus_dominus.widgets import DateTimePicker

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

class RecordForm(forms.ModelForm):
	created = forms.DateTimeField(
		widget=DateTimePicker(
			options={
				'userCurrent': True,
				'collaps': False,
			},
			attrs={
				'append': 'fa fa-calender',
				'icon_toggle': True,
			}
		),
	)

	class Meta:
		model = Record
		fields = [ 'created' ]
