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
	shared = models.BooleanField(default=False)
	shared_token = models.CharField(max_length=128, default='')
	max_value = models.DecimalField(default=-1, max_digits=12, decimal_places=2)
	min_value = models.DecimalField(default=0, max_digits=12, decimal_places=2)
	increment = models.DecimalField(default=1, max_digits=12, decimal_places=2)
	incrementable = models.BooleanField(default=True)
	decrementable = models.BooleanField(default=False)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.shared:
			self.shared_token = ''
		elif not self.shared_token:
			self.shared_token = self.generate_shared_token()

		super(Counter, self).save(*args, **kwargs)

	def generate_shared_token(self):
		import string
		import random
		letters = string.ascii_letters + string.digits
		while True:
			shared_token = ''.join(random.choice(letters) for i in range(10))
			try:
				Counter.objects.get(shared_token=shared_token)
			except:
				return shared_token

	def get_shared_url(self, request):
		if self.shared:
			server_name = request.META['SERVER_NAME']
			server_port = request.META['SERVER_PORT'] and ':' + request.META['SERVER_PORT'] or ''
			return request.scheme + '://' + server_name + server_port + '/counters/shared/' + self.shared_token + '/'

class CounterSubscription(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
	created = models.DateTimeField(default=timezone.now)

class Record(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
	increment = models.DecimalField(default=1, max_digits=12, decimal_places=2)
	created = models.DateTimeField(default=timezone.now)

class CounterSubscriptionForm(forms.ModelForm):

	subscribed = forms.BooleanField();

	class Meta:
		model = CounterSubscription
		exclude = ('user', 'counter', 'created',)

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
