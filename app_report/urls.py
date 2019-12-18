from django.urls import path
from app_report import views

urlpatterns = [
    path('index/',views.index),
    path('register/',views.register),
    path('login/',views._login)
]