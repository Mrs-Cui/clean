#! /usr/env/bin python

from django.urls import re_path, include

from account.views import LoginView, UserAddView
urlpatterns = [
    re_path(r'^login/', LoginView.as_view(), name='login'),
    re_path(r'^add/$', UserAddView.as_view(), name='add_user')
]