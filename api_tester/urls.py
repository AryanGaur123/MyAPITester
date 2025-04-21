from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('request/<int:request_id>/', views.request_detail, name='request_detail'),
    path('clear-history/', views.clear_history, name='clear_history'),
]
