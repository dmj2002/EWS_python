from django.urls import path

from predict import views

urlPatterns = [
    path('training/', views.train),
    path('prediction/', views.predict),
]