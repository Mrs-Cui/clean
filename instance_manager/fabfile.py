#!/usr/bin/env python
# encoding: utf-8

"""该文件要放在项目根目录下, 而且要在项目目录下执行
部署项目:
fab -R pro deploy_instance_manager  正式服
"""

from fabric.api import env, local, run, put, cd, settings, roles, execute, get, hide, lcd
import sys
import os

# 操作一致的服务器可以放在一组,同一组的执行同一套操作
env.roledefs = {
    'pro': ['ubuntu@13.251.1.219'],
}

env.key_filename = ["/data/cui/cache/pem/ec2_manager.pem",]


REMOTE_DIST_DIR = '/opt/www/instance_manager'  # 统一的项目路径
# env.gateway = "ubuntu@52.80.128.226:22"

INSTALL_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def pack():
    """把项目打为tar包"""
    # 删除本地 pyc 文件
    local('find . -name "*.pyc"  | xargs rm -f')

    # 打包文件列表
    tar_files = ['*']
    # 忽略打包文件列
    tar_exfiles = ['*.tar.gz', 'fabfile.py', '*.pem', 'venv', 'logs', 'db',]  # , 'templates'
    excludes = ' '.join(['--exclude="%s"' % e for e in tar_exfiles])
    includes = ' '.join(tar_files)
    # 删除本地旧包
    local('rm -f instance_manager.tar.gz')
    # 生成新包
    local('tar -czvf instance_manager.tar.gz %s %s' % (excludes, includes))
    local('rm -f install.tar.gz')
    with lcd(INSTALL_PATH):
        local('tar -czvf install.tar.gz install/*')
        local('mv install.tar.gz website/instance_manager')


def deploy_instance_manager():
    """部署项目"""

    pack()
    # 删除远程服务器的临时文件
    remote_tmp_tar = '/tmp/instance_manager.tar.gz'
    remote_install_tar = '/tmp/install.tar.gz'
    run('rm -f %s' % remote_tmp_tar)
    run('rm -f /tmp/install.tar.gz')
    # 上传tar文件至远程服务器
    put('instance_manager.tar.gz', remote_tmp_tar)
    put('install.tar.gz', remote_install_tar)

    # 解压
    with settings(warn_only=True):
        run('mkdir -p %s' % REMOTE_DIST_DIR)
    with cd(REMOTE_DIST_DIR):
        run('sudo tar -xzvf %s' % remote_tmp_tar)
        run('sudo rm -rf install')
        run('sudo tar -zxvf %s' % remote_install_tar)

    # 设定新目录 ubuntu 权限
    run('sudo chown -R ubuntu:ubuntu %s' % REMOTE_DIST_DIR)
    #
    run('sudo supervisorctl restart instance_manager')

    # 设定static目录 权限
    # run('chmod 775  %s' % REMOTE_DIST_DIR + '/static')
