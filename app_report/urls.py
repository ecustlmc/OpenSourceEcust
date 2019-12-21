from django.urls import path
from app_report import views

urlpatterns = [
    path('index/',views.index),
    path('register/',views.register),
    path('login/',views._login),
    path('logout/',views._logout),
    path('changepassword/',views.changepassword),
    path('comment/',views.ajax_comment),
    path('like/',views.ajax_like),
    path('view/',views.reportview),
    path('new/',views.reportnew)
]