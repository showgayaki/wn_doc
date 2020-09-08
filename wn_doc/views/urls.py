from __future__ import absolute_import
from __future__ import unicode_literals
from django.urls import path
from .index import index
from .sub import sub
from .repository import repository


urlpatterns = [
    path('', index, name='index'),
    path('<str:page>/', sub, name='sub'),
    path('repositories/<path:directory>/', repository, name='repository'),
]
