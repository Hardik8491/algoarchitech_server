from django.urls import path
from . import views

urlpatterns = [
    path('commodities/', views.commodities_view, name='commodities'),
    path('users/', views.users_view, name='users'),
]
