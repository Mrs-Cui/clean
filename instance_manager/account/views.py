import json

from django.shortcuts import render

# Create your views here.


from django.views.generic import DetailView, View, UpdateView, ListView
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher, CryptPasswordHasher, make_password

# from account.aes import AESCipher
from account.models import UserAccount

# AES = AESCipher('zakzak_admin_key')


class LoginView(ListView):
    
    template_name = 'region_ec2_manager/region_list.html'

    # @csrf_protect
    def get(self, request, *args, **kwargs):

        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        user = authenticate(request, username=data['username'], password=data['password'])
        status = 0
        index = '/region_list'
        if user:
            login(request, user)
            self.object_list = []
        else:
            status = 1
        return HttpResponse(json.dumps({'status': status, 'index': index}))


class UserAddView(View):

    def post(self, request, *args, **kwargs):
        pass
    


