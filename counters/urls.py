from django.urls import path

from . import views

urlpatterns = [
	path('', views.CounterListView.as_view()),
	path('<str:slug>/', views.CounterDetailView.as_view()),
	path('<str:slug>/config/', views.CounterUpdateView.as_view()),
	path('<str:counter>/increment/', views.increment_counter),
	path('<str:counter>/list/', views.RecordListView.as_view()),
	path('<str:counter>/delete/', views.delete_counter),
	path('<str:counter>/delete/<int:record>/', views.delete_record),
	path('<str:counter>/edit/<int:pk>/', views.RecordUpdateView.as_view()),
]
