from django.utils import timezone
from django.http import HttpResponse, Http404
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Counter, CounterSubscription, CounterSubscriptionForm, Record, RecordForm

import json


def is_allowed(user, counter):

	if user == counter.user:
		return True

	subscriptions = CounterSubscription.objects.filter(user=user, counter=counter)
	if len(subscriptions) > 0:
		return True

	return False

@method_decorator(login_required, name='dispatch')
class CounterListView(ListView):

	model = Counter
	paginage_by = 20

	def get_queryset(self):
		queryset1 = Counter.objects.filter(user=self.request.user)
		for counter in queryset1:
			records = Record.objects.filter(counter=counter)
			counter.records = len(records)
		subscriptions = CounterSubscription.objects.filter(user=self.request.user).values('counter')
		counters = [ x['counter'] for x in subscriptions ]
		queryset2 = Counter.objects.filter(shared=True, id__in=counters)
		for counter in queryset2:
			records = Record.objects.filter(counter=counter)
			counter.records = len(records)
		return queryset1|queryset2

@method_decorator(login_required, name='dispatch')
class RecordListView(ListView):

	model = Record
	paginate_by = 20

	def get_queryset(self):
		self.counter = get_object_or_404(Counter, user=self.request.user, pk=self.kwargs['counter'])
		return Record.objects.filter(counter=self.counter).order_by('created')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['counter'] = self.counter
		context['total'] = len(self.object_list)
		return context

@method_decorator(login_required, name='dispatch')
class CounterUpdateView(UpdateView):

	model = Counter
	fields = [ 'name', 'unit_price', 'currency', 'shared' ]

	def get_object(self):
		return get_object_or_404(Counter, user=self.request.user, pk=self.kwargs['counter'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['counter'] = get_object_or_404(Counter, user=self.request.user, pk=self.kwargs['counter'])
		if self.object.shared:
			context['shared_url'] = self.object.get_shared_url(self.request)
		return context

	def get_success_url(self):
		return '/counters/' + str(self.object.pk) + '/'

@method_decorator(login_required, name='dispatch')
class RecordUpdateView(UpdateView):

	model = Record
	fields = [ 'created' ]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['counter'] = get_object_or_404(Counter, user=self.request.user, pk=self.object.counter_id)
		return context

@method_decorator(login_required, name='dispatch')
class CounterDetailView(DetailView):

	model = Counter

	def get_object(self):
		return get_object_or_404(Counter, pk=self.kwargs['counter'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		records = Record.objects.filter(counter=self.object).order_by('created')

		record = records.last()
		if record:
			context['latest_record_date'] = record.created

		context['total'] = len(records)
		if self.object.unit_price:
			context['total_price'] = len(records) * self.object.unit_price
		context['labels'] = []
		context['data'] = []

		dates = {}
		for record in records:
			date = record.created.strftime('%Y-%m-%d')
			if date not in dates:
				dates[date] = 0
			dates[date] += 1

		for day, value in dates.items():
			context['data'].append(value)
			context['labels'].append(day)

		context['data'] = json.dumps(context['data'])
		context['labels'] = json.dumps(context['labels'])
		context['is_owner'] = self.request.user == self.object.user

		return context


# Counters API

@csrf_exempt
@login_required
def new_counter(request, counter):
	counter, created = Counter.objects.get_or_create(name=counter, user=request.user)
	return HttpResponse('OK')


@login_required
def increment_counter(request, counter):
	counter = get_object_or_404(Counter, pk=counter)
	if is_allowed(request.user, counter):
		Record(counter=counter, user=request.user).save()
		records = Record.objects.filter(counter=counter)
		return HttpResponse('OK')

	return HttpResponse('KO', status_code=403)

@login_required
def delete_counter(request, counter):

	counter = get_object_or_404(Counter, pk=counter)
	if is_allowed(request.user, counter):
		try:
			counter.delete()

		except Counter.DoesNotExist:
			return HttpResponse('No such counter')

		return HttpResponse('OK')

	return HttpResponse('KO', status_code=403)

@login_required
def delete_record(request, counter, record):

	counter = get_object_or_404(Counter, pk=counter)
	if is_allowed(request.user, counter):
		try:
			record = Record.objects.get(counter=counter, pk=record)
			record.delete()

		except Counter.DoesNotExist:
			return HttpResponse('No such counter')

		except Record.DoesNotExist:
			return HttpResponse('No such record')

		return HttpResponse('OK')

	return HttpResponse('KO', status_code=403)

@login_required
def subscribe_counter(request, shared_token):

	counter = get_object_or_404(Counter, shared_token=shared_token)
	if request.method == 'POST':

		form = CounterSubscriptionForm(request.POST)
		if form.is_valid() and form.cleaned_data['subscribed']:
			CounterSubscription.objects.get_or_create(user=request.user, counter=counter, defaults={ 'created': timezone.now() })

	else:
		form = CounterSubscriptionForm()

	context = {
		'form': form,
	}

	return render(request, 'counters/subscribe.html', context)
