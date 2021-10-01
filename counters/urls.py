from django.urls import path

from . import views

urlpatterns = [
	path('', views.CounterListView.as_view()),
	path('new/<str:counter>/', views.new_counter),
	path('<int:counter>/', views.CounterDetailView.as_view()),
	path('<int:counter>/config/', views.CounterUpdateView.as_view()),
	path('<int:counter>/increment/', views.increment_counter),
	path('<int:counter>/list/', views.RecordListView.as_view()),
	path('<int:counter>/delete/', views.delete_counter),
	path('<int:counter>/delete/<int:record>/', views.delete_record),
	path('<int:counter>/edit/<int:pk>/', views.RecordUpdateView.as_view()),
	path('shared/<str:shared_token>/', views.subscribe_counter),
]
