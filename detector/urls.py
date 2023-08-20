from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post-to-twitter/', views.post_to_twitter, name='post_to_twitter'),
]
