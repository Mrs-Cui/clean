# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
import hashlib
import json
import logging
import os
import sys
import traceback
import pymysql
import subprocess
from django.shortcuts import render
from django.views.generic.list import ListView, View
from django.views.generic.detail import DetailView
from django.http.response import HttpResponse
from pymysql.err import IntegrityError
from region_ec2_manager.db_operator import RegionOp, UserOp, Ec2Op, AutoScalingOp
from account.util import CheckSession

from install import main

root = logging.getLogger('root')
info = logging.getLogger('django')


class RegionListView(ListView):

    template_name = 'region_ec2_manager/region_list.html'
    
    @CheckSession
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            status, region_list = 0, []
            op = RegionOp()
            try:
                region_list = op.get_region_list()
            except Exception as e:
                status = 1
                root.error('获取region list失败, error: [{0}]'.format(traceback.format_exc()))
            return HttpResponse(json.dumps({'region_list': region_list, 'status': status}))
        else:
            self.object_list = []
            return self.render_to_response({'status': 0})

    @CheckSession
    def post(self, request, *args, **kwargs):
        op = RegionOp()
        status = 0
        try:
            data = json.loads(request.body)
            params = data['params']
            filters = data['filters']
            op.update_region(params, filters)
        except Exception as e:
            status = 1
            root.error('更新region 信息失败, error: [{0}]'.format(traceback.format_exc()))
        return HttpResponse(json.dumps({'status': status}))


class RegionDetailView(DetailView):
    pass


class UserDetailView(DetailView):
    pass


class UserListView(ListView):
    template_name = 'region_ec2_manager/user_list.html'

    @CheckSession
    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        op = UserOp()
        status, user_list = 0, []
        try:
            user_list = op.get_user_list(params)
        except Exception as e:
            status = 1
            root.error('获取user list失败, error: [{0}]'.format(traceback.format_exc()))
        self.object_list = user_list
        return self.render_to_response({'status': status, 'user_list': user_list})

    @CheckSession
    def post(self, request, *args, **kwargs):
        status = 0
        op = UserOp()
        try:
            data = json.loads(request.body)
            params = data['params']
            filters = data.get('filters')
            if filters:
                op.update_user_info(params, filters)
            else:
                op.insert_user(params)
        except IntegrityError as e:
            status = 2
        except Exception as e:
            status = 1
            root.error('更新user 信息失败, error: [{0}]'.format(traceback.format_exc()))
        return HttpResponse(json.dumps({'status': status}))


class Ec2MapUserListView(ListView):

    @CheckSession
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        params = data['params']
        filters = data.get('filters', {})
        status = 0
        op = Ec2Op()
        try:
            if filters:
                op.update_ec2_and_user(params, filters)
            else:
                op.insert_ec2_and_user(params)
        except Exception as e:
            status = 1
            root.error('更新　ec2 and user出错, error: [{0}]'.format(traceback.format_exc()))
        return HttpResponse(json.dumps({'status': status}))

    @CheckSession
    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        op = Ec2Op()
        results, status = [], 0
        try:
            results = op.get_ec2_user_list(params)
        except Exception as e:
            status = 1
            root.error('获取已分配用户列表失败, error: [{0}]'.format(traceback.format_exc()))
        return HttpResponse(json.dumps({'status': status, 'user_list': results}))



class Ec2ListView(ListView):

    template_name = 'region_ec2_manager/ec2_list.html'

    def init_data(self):
        op = UserOp()
        user_list = op.get_user_list({'is_enable': 1})
        login_names = [item['login_name'] for item in user_list]

        op = RegionOp()
        region_list = op.get_region_list({'enable': 1})
        region_names = [item['region_name'] for item in region_list]
        op = Ec2Op()
        autoscalings = op.get_autoscaling()
        return {
            'login_names': login_names, 'region_names': region_names, 'autoscalings': autoscalings
        }

    @CheckSession
    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        ec2_list = []
        if params:
            op = Ec2Op()
            status = 0
            try:
                if 'login_name' in params:
                    ec2_list = op.get_ec2_and_user(copy.copy(params))
                else:
                    ec2_list = op.get_ec2_list(params)
            except Exception as e:
                status = 1
                root.error('获取ec2 list信息失败, error: [{0}]'.format(traceback.format_exc()))
            if request.is_ajax():
                return HttpResponse(json.dumps({'ec2_list': ec2_list, 'status': status}))
            else:
                init_data = self.init_data()
                init_data.update({'ec2_list': json.dumps(ec2_list), 'params': json.dumps(params)})
                self.object_list = ec2_list
                return self.render_to_response(init_data)
        else:
            init_data = self.init_data()
            init_data.update({'ec2_list': json.dumps(ec2_list)})
            self.object_list = ec2_list
            return self.render_to_response(init_data)

    @CheckSession
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        params = data['params']
        filters = data.get('filters', {})
        status = 0
        op = Ec2Op()
        try:
            if filters:
                op.update_ec2(params, filters)
            else:
                pass
        except Exception as e:
            status = 1
            root.error('更新ec2 info 出错, error: [{0}]'.format(traceback.format_exc()))
        return HttpResponse(json.dumps({'status': status}))


class FileView(View):

    BASE_PATH = '/opt/www/static'

    def init_file_path(self, file_path):
        if not os.path.exists(file_path):
            os.system('cd {0} && mkdir -p {1}'.format(self.BASE_PATH, file_path))
        return file_path

    @CheckSession
    def post(self, request, *args, **kwargs):
        file_type = request.POST.get('type')
        file_path = ''
        try:
            if file_type == 'pem':
                public_ip = request.POST.get('public_ipv4')
                md5 = hashlib.md5()
                md5.update(public_ip.encode('utf-8'))
                ip_str = md5.hexdigest()
                login_name = request.POST.get('login_name')
                file_path = self.init_file_path(os.path.join(login_name, ip_str))
                file_ob = request.FILES.get('file')
                file_name = file_ob.name
                file_path = os.path.join(file_path, file_name)
                with open(os.path.join(self.BASE_PATH, file_path), 'w+') as file:
                    for item in file_ob.chunks():
                        file.write(str(item, encoding='utf-8'))
        except Exception as e:
            root.error(traceback.format_exc())
        return HttpResponse(json.dumps({'status': 0, 'file_path': file_path}))


class DeployScriptView(View):

    @CheckSession
    def post(self, request, *args, **kwargs):
        status = 0
        try:
            data = json.loads(request.body)
            file_path = os.path.join(FileView.BASE_PATH, data['file_path'])
            file = open('logs/install_log.log', 'a+')
            sys.stdout = file
            main.install_lbe_manager_agent(data['public_ipv4'], data['login_name'], file_path)
            file.close()
        except Exception as e:
            status = 1
            root.error('脚本部署失败, error: [{0}]'.format(traceback.format_exc()))
        return HttpResponse(json.dumps({'status': status}))


class AutoScalingMapUserListView(View):

    @CheckSession
    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        status = 0
        login_names = []
        try:
            op = AutoScalingOp()
            login_names = op.get_login_name(params)
            op = UserOp()
            user_names = op.get_user_list({'is_enable': 1})
            user_names = [item['login_name'] for item in user_names]
            login_names = list(set(user_names) - set(login_names))
        except Exception as e:
            status = 1
            root.error('获取autoscaling 未分配用户失败, error: [{0}]'.format(traceback.format_exc()))
        return HttpResponse(json.dumps({'status': status, 'user_list': login_names}))

    @CheckSession
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        op = AutoScalingOp()
        status = 0
        params = data['params']
        filters = data.get('filters', {})
        data = {}
        try:
            if not filters:
                op.insert_autoscaling_map_user(params)
                data['login_names'] = op.get_login_name()
            else:
                op.update_autoscaling_map_user(params, filters)
        except Exception as e:
            status = 1
            root.error('autoscaling权限配置失败, error: [{0}]'.format(traceback.format_exc()))
        data['status'] = status
        return HttpResponse(json.dumps(data))


class AutoScalingListView(ListView):

    template_name = 'region_ec2_manager/autoscaling_list.html'

    @CheckSession
    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        op = AutoScalingOp()
        status = 0
        if params:
            autoscalings = []
            try:
                autoscalings = op.get_autoscaling_map_user_list(params)
            except Exception as e:
                root.error('数据查询失败, error: [{0}]'.format(traceback.format_exc()))
                status = 0
            return HttpResponse(json.dumps({'autoscaling_list': autoscalings, 'status': status}))
        else:
            login_names = op.get_login_name()
            autoscalings = op.get_autoscaling_list()
            self.object_list = []
            return self.render_to_response({'login_names': login_names, 'autoscaling_list': autoscalings})