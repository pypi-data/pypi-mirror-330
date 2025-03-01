# -*- coding: UTF-8 –*-
import os
import sys
import json
import socket
import logging
from mdbq.mysql import mysql

support_path = os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])), 'support')
logger = logging.getLogger(__name__)


def return_default_host():
    targe_host = socket.gethostname()
    hostname = 'xigua_lx'  # 正常情况下 spider_tg 只会在 xigua_lx 或者 xigua1 运行，且都指向主库
    local = 'remoto'

    if targe_host == 'xigua_lx':
        local = 'local'  # 直接指向局域网地址
    elif targe_host in ['localhost.localdomain', 'xigua1']:
        targe_host = 'xigua1'  # 修正 Linux 系统用户名
        local = 'local'  # 直接指向局域网地址
    elif targe_host == 'MacBookPro':
        local = 'local'  # 直接指向局域网地址
    return targe_host, hostname, local


def get_mysql_engine(platform='Windows', hostname='xigua_lx', sql='mysql', local='remoto', config_file=None):
    if not config_file:
        config_file = os.path.join(support_path, 'my_config.txt')
    if not os.path.isfile(config_file):
        print(f'缺少配置文件，无法读取配置文件： {config_file}')
        return None

    if socket.gethostname() == 'xigua_lx':
        local = 'local'

    with open(config_file, 'r', encoding='utf-8') as f:
        conf = json.load(f)
    conf_data = conf[platform][hostname][sql][local]
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    _engine = mysql.MysqlUpload(username=username, password=password, host=host, port=port, charset='utf8mb4')
    return _engine, username, password, host, port


def write_back_bak(datas):
    """ 将数据写回本地 """
    if not os.path.isdir(support_path):
        print(f'缺少配置文件，无法读取配置文件： {file}')
        return
    file = os.path.join(support_path, 'my_config.txt')
    with open(file, 'w+', encoding='utf-8') as f:
        json.dump(datas, f, ensure_ascii=False, sort_keys=False, indent=4)



if __name__ == '__main__':
    pass
