from django.utils import timezone

from .models import Profile

import pytz


class TimezoneMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):

		if request.user.is_anonymous:
			timezone.deactivate()

		else:
			profile, created = Profile.objects.get_or_create(user=request.user)
			timezone.activate(profile.timezone or pytz.timezone('Europe/London'))

		return self.get_response(request)
