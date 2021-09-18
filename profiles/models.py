from django import forms
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from timezone_field import TimeZoneField


class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	timezone = TimeZoneField()

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()
