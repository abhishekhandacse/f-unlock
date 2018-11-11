from django.urls import path, include
from . import views

urlpatterns = [
	path('panel/', views.panel, name='panel'),
	path('onetime/', views.onetime, name='onetime'),
	path('funlock/', views.funlock, name='funlock'),
	path('panel/grant/<int:id>', views.grant, name='grant'),
	path('panel/grant/', views.grant, name='grant'),
]