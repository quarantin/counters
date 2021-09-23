from django.http import HttpResponse
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Counter, Record, RecordForm

import json


@method_decorator(login_required, name='dispatch')
class CounterListView(ListView):

	model = Counter
	paginage_by = 20

	def get_queryset(self):
		queryset = Counter.objects.filter(user=self.request.user)
		for counter in queryset:
			records = Record.objects.filter(counter=counter)
			counter.records = len(records)
		return queryset

@method_decorator(login_required, name='dispatch')
class RecordListView(ListView):

	model = Record
	paginate_by = 20

	def get_queryset(self):
		self.counter = get_object_or_404(Counter, user=self.request.user, name=self.kwargs['counter'])
		return Record.objects.filter(counter=self.counter).order_by('created')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['counter'] = self.counter
		context['total'] = len(self.object_list)
		return context

@method_decorator(login_required, name='dispatch')
class CounterUpdateView(UpdateView):

	model = Counter
	fields = [ 'name', 'unit_price', 'currency' ]

	def get_object(self):
		return get_object_or_404(Counter, user=self.request.user, name=self.kwargs['slug'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['counter'] = get_object_or_404(Counter, user=self.request.user, name=self.kwargs['slug'])
		return context

	def get_success_url(self):
		return '/counters/' + self.object.name + '/'

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
		obj, created = Counter.objects.get_or_create(user=self.request.user, name=self.kwargs['slug'])
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		records = Record.objects.filter(counter=self.object).order_by('created')

		record = records.last()
		if record:
			context['latest_record_date'] = record.created

		context['total'] = len(records)
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

		return context


# Counters API

@login_required
def increment_counter(request, counter):
	counter, created = Counter.objects.get_or_create(user=request.user, name=counter)
	Record(counter=counter).save()
	records = Record.objects.filter(counter=counter)
	return HttpResponse(len(records))

@login_required
def delete_counter(request, counter):

	try:
		counter = Counter.objects.get(user=request.user, name=counter)
		counter.delete()

	except Counter.DoesNotExist:
		return HttpResponse('No such counter')

	return HttpResponse('OK')

@login_required
def delete_record(request, counter, record):

	try:
		counter = Counter.objects.get(user=request.user, name=counter)
		record = Record.objects.get(counter=counter, pk=record)
		record.delete()

	except Counter.DoesNotExist:
		return HttpResponse('No such counter')

	except Record.DoesNotExist:
		return HttpResponse('No such record')

	return HttpResponse('OK')
