from counters.models import *

fin = open('db.txt', 'r')
lines = fin.readlines()
fin.close()

for line in lines:

	tokens = line.split('|')
	if tokens[0] == 'COUNTER':

		pk      = tokens[1]
		user_id = tokens[2]
		name    = tokens[3]
		created = tokens[4]

		Counter(pk=pk, user_id=user_id, name=name, created=created).save()

	elif tokens[0] == 'RECORD':

		counter_id = tokens[1]
		created    = tokens[2]

		Record(counter_id=counter_id, created=created).save()
