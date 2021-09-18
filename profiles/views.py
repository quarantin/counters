from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Profile

class ProfileUpdateView(SuccessMessageMixin, UpdateView):
	model = Profile
	fields = [ 'timezone' ]
	success_url = '/accounts/profile/'
	success_message = "Your settings have been saved successfully"

	def get_object(self):
		obj, created = Profile.objects.get_or_create(user=self.request.user)
		return obj
