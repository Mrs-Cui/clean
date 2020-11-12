#! /usr/bin/env python

from region_ec2_manager.models import Region, User, Ec2MapUser, Ec2, FeedBackFinal, AutoScalingMapUser

from django.db import transaction
from django.db.models import Max, DateTimeField, F, ExpressionWrapper, IntegerField, Q
from pymysql.err import IntegrityError

from datetime import datetime


class Base(object):
    pass


class RegionOp(Base):

    def get_region_list(self, params=None):
        if not params:
            region_list = Region.objects.values('region_name', 'endpoint', 'enable', 'description').all()
        else:
            region_list = Region.objects.values('region_name', 'endpoint', 'enable', 'description').filter(**params)
        if region_list:
            region_list = [item for item in region_list]
        else:
            region_list = []
        return region_list

    def update_region(self, params, filters):
        result = Region.objects.filter(**filters).update(**params)


class UserOp(Base):

    def get_user_list(self, params=None):
        if not params:
            user_list = User.objects.values('login_name', 'username', 'is_enable')
        else:
            user_list = User.objects.values('login_name', 'username', 'is_enable').filter(**params)
        if user_list:
            user_list = [item for item in user_list]
        else:
            user_list = []
        return user_list

    def update_user_info(self, params, filters):
        result = User.objects.filter(**filters).update(**params)

    def insert_user(self, params):
        with transaction.atomic():

            user_info = User.objects.filter(login_name=params['login_name']).first()
            if user_info:
                raise IntegrityError
            else:
                user = User(**params)
                user.save()


class Ec2Op(Base):

    DIFF_TIME = 10 * 60

    def get_autoscaling(self, params=None):
        if params:
            autoscalings = Ec2.objects.values('autoscaling').filter(**params).distinct()
        else:
            autoscalings = Ec2.objects.values('autoscaling').distinct()
        if autoscalings:
            autoscalings = [item['autoscaling'] for item in autoscalings if item['autoscaling']]
        else:
            autoscalings = []
        return autoscalings

    def get_ec2_list(self, params=None):
        if params:
            ec2_list = Ec2.objects.values().filter(**params)
        else:
            ec2_list = Ec2.objects.values().all()
        if ec2_list:
            tmp = []
            instance_id = []
            for item in ec2_list:
                del item['update_time']
                tmp.append(item)
                item['status'] = 2
                instance_id.append(item['instance_id'])
            ec2_list = tmp
            instance_status = self.get_feedback_final(instance_id)
            for item in ec2_list:
                if instance_status.get(item['instance_id']):
                    item['status'] = instance_status[item['instance_id']]

        else:
            ec2_list = []
        return ec2_list

    def get_feedback_final(self, instance_ids):
        feedback_infos = FeedBackFinal.objects.values('instance_id').filter(instance_id__in=instance_ids).annotate(
            diff_time=Max('update_time', output_field=DateTimeField())
        ).all()
        data = {}
        for item in feedback_infos:
            data[item['instance_id']] = 0 if datetime.utcnow().timestamp() - item['diff_time'].timestamp() <= self.DIFF_TIME else 1
        return data

    def get_ec2_and_user(self, params):
        with transaction.atomic():
            query_set = Ec2MapUser.objects.values('instance_id', 'sudo_permission', 'login_name', 'is_enable').filter(
                login_name=params['login_name'])
            autoscalings = AutoScalingMapUser.objects.values('autoscaling_group_name', 'login_name', 'is_enable', 'sudo_permission').filter(
                login_name=params['login_name']).all()
            del params['login_name']
            if autoscalings:
                autoscalings = [item for item in autoscalings]
                autoscalings = {item['autoscaling_group_name']: item for item in autoscalings}
                autoscaling_group_name = list(autoscalings.keys())
            else:
                autoscaling_group_name, autoscalings = [], {}
            if query_set:
                query_set = {item['instance_id']: item for item in query_set}
                instance_ids = list(query_set.keys())
                instance_status = self.get_feedback_final(instance_ids)
                ec2_list = Ec2.objects.values().filter(Q(instance_id__in=instance_ids) | Q(autoscaling__in=autoscaling_group_name), **params).all()
                data = []
                for item in ec2_list:
                    del item['update_time']
                    if item['instance_id'] in query_set:
                        item.update(query_set[item['instance_id']])
                    else:
                        if item['autoscaling'] in autoscalings:
                            item.update(autoscalings[item['autoscaling']])
                    if item['instance_id'] in instance_status:
                        item['status'] = instance_status[item['instance_id']]
                    else:
                        item['status'] = 2
                    data.append(item)
            else:
                data = []
        return data

    def update_ec2(self, params, filters):
        result = Ec2.objects.filter(**filters).update(**params)

    def update_ec2_and_user(self, params, filters):
        result = Ec2MapUser.objects.filter(**filters).update(**params)

    def get_ec2_user_list(self, params):
        result = Ec2MapUser.objects.values('login_name').filter(**params, is_enable=1)
        if result:
            result = [item['login_name'] for item in result]
        else:
            result = []
        return result

    def insert_ec2_and_user(self, params):
        with transaction.atomic():
            info = Ec2MapUser.objects.filter(instance_id=params['instance_id'], login_name=params['login_name']).first()
            if info:
                for key, value in params:
                    setattr(info, key, value)
            else:
                info = Ec2MapUser(**params)
            info.save()


class AutoScalingOp(Base):

    def get_autoscaling_list(self, params=None):
        if params:
            autoscalings = Ec2.objects.values('autoscaling', 'region_name').filter(**params, autoscaling__isnull=False).distinct()
        else:
            autoscalings = Ec2.objects.values('autoscaling', 'region_name').filter(autoscaling__isnull=False).distinct()
        autoscalings = [item for item in autoscalings]
        return autoscalings

    def get_login_name(self, params=None):
        if params:
            login_names = AutoScalingMapUser.objects.values('login_name').filter(**params).distinct()
        else:
            login_names = AutoScalingMapUser.objects.values('login_name').distinct()
        login_names = [item['login_name'] for item in login_names]
        return login_names

    def get_autoscaling_map_user_list(self, params=None):
        if params:
            autoscalings = AutoScalingMapUser.objects.values('autoscaling_group_name', 'login_name', 'is_enable',
                                                             'sudo_permission').filter(**params)
        else:
            autoscalings = AutoScalingMapUser.objects.values('autoscaling_group_name', 'login_name', 'is_enable', 'sudo_permission')
        autoscalings = [item for item in autoscalings]
        for item in autoscalings:
            item['autoscaling'] = item['autoscaling_group_name']
        return autoscalings

    def insert_autoscaling_map_user(self, params):
        with transaction.atomic():
            autoscaling = AutoScalingMapUser.objects.filter(login_name=params['login_name'],
                                                          autoscaling_group_name=params[
                                                              'autoscaling_group_name']).first()
            if autoscaling:
                for key, value in params.items():
                    setattr(autoscaling, key, value)
            else:
                autoscaling = AutoScalingMapUser(**params)
            autoscaling.save()

    def update_autoscaling_map_user(self, params, filters):
        AutoScalingMapUser.objects.filter(**filters).update(**params)

class UserAccountOp(Base):
    pass
