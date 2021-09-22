from django import forms
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tempus_dominus.widgets import DateTimePicker

from datetime import datetime


class Counter(models.Model):

	CURRENCY_DOLLAR = 'dollar'
	CURRENCY_EURO   = 'euro'
	CURRENCY_POUND  = 'pound'

	CURRENCY_CHOICES=(
		(CURRENCY_DOLLAR, '$'),
		(CURRENCY_EURO,   '€'),
		(CURRENCY_POUND,  '£'),
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=64)
	unit_price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
	currency = models.CharField(choices=CURRENCY_CHOICES, default=CURRENCY_DOLLAR, max_length=8)
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
