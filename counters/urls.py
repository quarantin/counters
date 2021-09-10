from django.urls import path

from . import views

urlpatterns = [
	path('', views.list_counters),
	path('<str:counter>/', views.view_counter),
	path('<str:counter>/add/', views.increment_counter),
	path('<str:counter>/delete/', views.delete_counter),
]
