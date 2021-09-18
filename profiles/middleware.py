from django.utils import timezone

from .models import Profile


class TimezoneMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		profile = Profile.objects.get(user=request.user)
		if profile.timezone:
			timezone.activate(profile.timezone)
		else:
			timezone.deactivate()
		return self.get_response(request)
