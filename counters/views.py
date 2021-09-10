from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Counter, Entry

import json


@login_required
def list_counters(request):
	counters = []
	all_counters = Counter.objects.filter(user=request.user)
	for counter in all_counters:
		entries = Entry.objects.filter(counter=counter)
		counters.append({ 'name': counter.name, 'value': len(entries) })
	context = { 'counters': counters }
	return render(request, 'counters/index.html', context)

@login_required
def view_counter(request, counter):
	counter, created = Counter.objects.get_or_create(user=request.user, name=counter)
	entries = Entry.objects.filter(counter=counter)
	context = { 'counter': counter, 'total': len(entries), 'labels': [], 'data': []}

	dates = {}
	for entry in entries:
		date = entry.created.strftime('%Y-%m-%d')
		if date not in dates:
			dates[date] = 0
		dates[date] += 1

	for day, value in dates.items():
		context['data'].append(value)
		context['labels'].append(day)

	context['data'] = json.dumps(context['data'])
	context['labels'] = json.dumps(context['labels'])

	print(context['data'])
	print(context['labels'])

	return render(request, 'counters/view.html', context)

@login_required
def increment_counter(request, counter):
	counter, created = Counter.objects.get_or_create(user=request.user, name=counter)
	Entry(counter=counter).save()
	entries = Entry.objects.filter(counter=counter)
	return HttpResponse(len(entries))

@login_required
def delete_counter(request, counter):

	try:
		counter = Counter.objects.get(user=request.user, name=counter)
		counter.delete()

	except Counter.DoesNotExist:
		pass

	return HttpResponse()
