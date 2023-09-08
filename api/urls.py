from django.urls import path
from . import views

urlpatterns = [
    path('test', views.index, name='test'),
    path('shell', views.Shells.as_view(), name='Shell')
]
