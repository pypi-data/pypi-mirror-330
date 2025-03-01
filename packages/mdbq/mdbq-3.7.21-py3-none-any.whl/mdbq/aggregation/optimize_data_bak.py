# -*- coding: UTF-8 –*-
from mdbq.mysql import mysql
from mdbq.config import default
import subprocess
import psutil
import time
import platform
import logging
"""
对指定数据库所有冗余数据进行清理
"""
targe_host, hostname, local =  default.return_default_host()
m_engine, username, password, host, port = default.get_mysql_engine(platform='Windows', hostname=hostname, sql='mysql', local=local, config_file=None)
if not username:
    logger.info(f'找不到主机：')

logger = logging.getLogger(__name__)


def op_data(db_name_lists, days: int = 63, is_mongo=True, is_mysql=True):
    # Mysql
    if is_mysql:
        s = mysql.OptimizeDatas(username=username, password=password, host=host, port=port)
        s.db_name_lists = db_name_lists
        s.days = days
        s.optimize_list()


if __name__ == '__main__':
    op_data(db_name_lists=['聚合数据'], days=10, is_mongo=True, is_mysql=True)
