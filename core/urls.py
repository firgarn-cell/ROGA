from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('apply/', views.create_application_view, name='apply'),
    path('logout/', views.logout_view, name='logout'),
]