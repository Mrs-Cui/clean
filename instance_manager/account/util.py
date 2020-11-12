#! /usr/bin/env python
import json
from functools import update_wrapper, wraps
from abc import abstractmethod
from django.shortcuts import redirect
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from django.utils.http import urlunquote_plus, _urlsplit
import types

class Base(object):

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class CheckSession(Base):
    
    def __init__(self, func):
        wraps(func)(self)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        request = args[1]
        hash_key = request.session.session_key
        if request.session.exists(hash_key):
            response = self.__wrapped__(*args, **kwargs)
            if isinstance(response, TemplateResponse):
                context_data = response.context_data
                context_data['account'] = {'username': request.user.username}
            return response
        else:
            if request.is_ajax():
                return HttpResponse(json.dumps({'status': 2, 'index': '/login'}))
            else:
                referer = request.headers.get('Referer')
                if referer:
                    split = _urlsplit(referer)
                    return redirect(split)
                else:
                    return redirect('login')


def csrf_failure(request, *args, **kwargs):
    if request.is_ajax():
        return HttpResponse(json.dumps({'status': 2, 'index': '/login'}))
    else:
        referer = request.headers.get('Referer')
        if referer:
            split = _urlsplit(referer)
            return redirect(split)
        else:
            return redirect('login')