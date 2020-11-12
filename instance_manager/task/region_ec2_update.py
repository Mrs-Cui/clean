#! /usr/bin/env python

import boto3
import sys

class InstanceItem(object):
    pass


class Base(object):

    def __init__(self, client, **kwargs):
        self.client = boto3.client(client, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.client


class Ec2Client(Base):

    def get_region(self):
        regions = self.client.describe_regions()
        return regions

    def get_ec2_instance(self, **kwargs):
        instances = self.client.describe_instances(**kwargs)
        return instances[0]


class Boto3Client(object):

    def __init__(self, client, **kwargs):
        self.client = self.client_map[client](client, **kwargs)

    def __new__(cls, *args, **kwargs):
        current_model = sys.modules[cls.__module__]
        print(current_model.__dict__)
        instance = super(Boto3Client, cls).__new__(cls)
        instance.client_map = {}
        for key, value in current_model.__dict__.items():
            try:
                if issubclass(value, Base):
                    instance.client_map[key.strip('Client').lower()] = value
            except TypeError as e:
                continue
        return instance

def main():
    boto = Boto3Client('ec2', region_name='eu-central-1')
    instances = boto.client.get_ec2_instance()
    # regions = boto.client.get_region()

if __name__ == '__main__':
    main()
    from gevent.pool import Pool, PoolFull
