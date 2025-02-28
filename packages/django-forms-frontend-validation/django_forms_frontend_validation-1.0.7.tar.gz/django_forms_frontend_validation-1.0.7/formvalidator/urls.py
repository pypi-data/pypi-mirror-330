from django.urls import path
from django.conf import settings

from . import views

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path('demo/sample-form/', views.sample, name='sample-form'),
        path('demo/sample-form2/', views.sample2, name='sample-form2'),
    ]
