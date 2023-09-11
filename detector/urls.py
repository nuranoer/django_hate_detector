from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post_to_twitter/', views.post_to_twitter, name='post_to_twitter'),
]
