from django.urls import path, include
from . import views

urlpatterns = [
	path('panel/', views.panel, name='panel'),
	path('onetime/', views.onetime, name='onetime'),
]