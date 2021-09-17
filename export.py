from counters.models import *

for counter in Counter.objects.all():
	print('COUNTER|%s|%s|%s|%s' % (counter.pk, counter.user.pk, counter.name, counter.created))
	for record in Record.objects.filter(counter=counter):
		print('RECORD|%s|%s' % (counter.pk, record.created))
