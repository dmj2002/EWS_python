from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('training/', views.train),
    path('prediction/', views.predict),
]