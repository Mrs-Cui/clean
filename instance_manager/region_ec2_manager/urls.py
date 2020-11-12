#! /usr/bin/env python

from django.urls import path, include, re_path

from region_ec2_manager import views

urlpatterns = [
    re_path(r'^region_list/$', views.RegionListView.as_view(), name='region_list'),
    re_path(r'^ec2_list/$', views.Ec2ListView.as_view(), name='ec2_list'),
    re_path(r'^region_detail/$', views.RegionDetailView.as_view(), name='region_detail'),
    re_path(r'^user_list/$', views.UserListView.as_view(), name='user_list'),
    re_path(r'^user_detail/$', views.UserDetailView.as_view(), name='user_detail'),
    re_path(r'^ec2_map_user_list/$', views.Ec2MapUserListView.as_view(), name='ec2_map_user_list'),
    re_path(r'^file/$', views.FileView.as_view(), name='file'),
    re_path(r'^deploy_script/$', views.DeployScriptView.as_view(), name='deploy_script'),
    re_path(r'^autoscaling_map_user_list/$', views.AutoScalingMapUserListView.as_view(), name='autoscaling_map_user_list'),
    re_path(r'^autoscaling_list/$', views.AutoScalingListView.as_view(), name='autoscaling_list')
]
