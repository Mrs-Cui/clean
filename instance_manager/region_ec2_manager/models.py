# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.


class Region(models.Model):

    region_name = models.CharField('Region Name', max_length=128)
    endpoint = models.CharField('End Point', max_length=256)
    description = models.TextField()
    enable = models.IntegerField('是否正在使用')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(default=datetime.utcnow())

    class Meta:
        db_table = 'region'
        unique_together = ['region_name']
        permissions = [('region_list_display', 'Region List Display'),
                       ('region_detail_update', 'Region Detail Update')]


class User(models.Model):
    login_name = models.CharField('Login Name', max_length=64)
    username = models.CharField('User Name', max_length=64)
    is_enable = models.IntegerField('Is Enable')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'
        unique_together = ['login_name']
        permissions = [('user_insert', 'User Insert'), ('user_list', 'User List')]


class Ec2(models.Model):
    instance_id = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    instance_type = models.CharField(max_length=64)
    az = models.CharField(max_length=128)
    instance_state = models.CharField(max_length=128)
    public_ipv4 = models.CharField(max_length=128)
    private_ip = models.CharField(max_length=128)
    autoscaling = models.CharField(max_length=128)
    region_name = models.CharField(max_length=128)
    enable = models.IntegerField(default=0)
    update_time = models.DateTimeField(default=datetime.utcnow())

    class Meta:
        db_table = 'ec2'
        unique_together = ['instance_id']


class Ec2MapUser(models.Model):
    instance_id = models.CharField(max_length=32)
    login_name = models.CharField('Login Name', max_length=64)
    sudo_permission = models.IntegerField(default=0)
    is_enable = models.IntegerField(default=0, db_column='enable')

    class Meta:
        db_table = 'ec2_and_user'
        unique_together = ['instance_id', 'login_name']
        permissions = [('ec2_map_user_display', 'Ec2 Map User Display'),
                       ('ec2_map_user_insert', 'Ec2 Map User Display'),
                       ('ec2_map_user_update', 'Ec2 Map User Update')]


class AutoScalingMapUser(models.Model):

    autoscaling_group_name = models.CharField(max_length=64, db_column='auto_scaling_group_name')
    login_name = models.CharField(max_length=32)
    sudo_permission = models.IntegerField(default=0)
    is_enable = models.IntegerField(default=0, db_column='enable')
    class Meta:
        db_table = 'autoscaling_and_user'


class FeedBackFinal(models.Model):
    instance_id = models.CharField(max_length=32)
    info = models.TextField()
    update_time = models.DateTimeField()

    class Meta:
        db_table = 'feedback_final'

