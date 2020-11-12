#! /usr/bin/env python

from django.contrib.auth.backends import ModelBackend, RemoteUserBackend

from account.models import UserAccount


class LoginModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = UserAccount.objects.filter(username=username, password=password).first()
        return user