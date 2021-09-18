from django.views.generic.base import RedirectView


class HomeRedirectView(RedirectView):
	permanent = True
	query_string = True

	def get_redirect_url(self, *args, **kwargs):
		redirect_url = '/counters/'
		if self.request.user.is_anonymous:
			redirect_url = '/accounts/login/?next=' + redirect_url
		return redirect_url
