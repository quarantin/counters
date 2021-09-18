from django.shortcuts import render
from django.views.generic.edit import UpdateView

from .models import Profile

class ProfileUpdateView(UpdateView):
	model = Profile
	fields = [ 'timezone' ]
	success_url = '/accounts/profile/'

	def get_object(self):
		obj, created = Profile.objects.get_or_create(user=self.request.user)
		return obj
