#!/usr/bin/python3
# -*- coding: utf-8 -*-

''' 
* File Modification Time 
''' 

from ftplib import FTP
from datetime import datetime
import configparser
import os
import logging
import logging.config

out_error= -2
file_name_conf_log = 'chek_oms_export.log.conf'
file_name_conf_conn = 'chek_oms_export.conf'
date_format = '%Y.%m.%d %H:%M:%S'


logging.config.fileConfig(os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name_conf_log))
logger = logging.getLogger("chek_oms_export")


def get_data_ftp_file(ftp_file_path, ftp_host, ftp_user, ftp_password):
    try:
        ftp = FTP(ftp_host, ftp_user, ftp_password)
        timestamp = ftp.voidcmd("MDTM {}".format(ftp_file_path))
        return datetime.strptime(timestamp[4:], "%Y%m%d%H%M%S")
    except Exception as err:
        logger.critical("File Modification Time (MDTM) - {}".format(str(err)))
        return out_error

def main():
    Config = configparser.ConfigParser()
    Config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name_conf_conn))
    ftp_file_path = Config.get('CONNECT', 'path')
    ftp_host = Config.get('CONNECT', 'host')
    ftp_user = Config.get('CONNECT', 'user')
    ftp_password = Config.get('CONNECT', 'password')
    
    ftp_out = get_data_ftp_file(ftp_file_path, ftp_host, ftp_user, ftp_password)
    date_now = datetime.now()
    if type(ftp_out) == type(date_now):
        delta_time = date_now.day - ftp_out.day
        print(delta_time)
        logger.info("File Modification Time (MDTM) - {}".format(ftp_out.strftime(date_format)))
    else:
        print(out_error)


if __name__ == '__main__':
    exit(main())
