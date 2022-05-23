#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：xushaohui time:2022/5/20

import pymysql
import configparser
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from table_checksum_html import html_data
import datetime

def mysql_conn(USER, PASSWORD, IP, PORT=3306, dbname='mysql'):
    db = pymysql.connect(user=USER, passwd=PASSWORD, host=IP, port=int(PORT), charset="UTF8", db=dbname,
                         client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,
                         autocommit=True)
    con = db.cursor()
    return con


def install_pt_tool():
    com_yum = """sudo yum install -y https://repo.percona.com/yum/percona-release-latest.noarch.rpm"""
    stat,output = subprocess.getstatusoutput(com_yum)
    if stat !=0:
        print(output)
    com_install = """sudo yum install -y percona-toolkit"""
    stat, output = subprocess.getstatusoutput(com_install)
    if stat !=0:
        print(output)

def table_checmsum(user,password,host,port):
    com_check = """pt-table-checksum -h%s  \
                    --user=%s \
                    --password='%s' \
                    --port=%s \
                    --replicate=repl_checksum.checksum --no-check-binlog-format \
                    --no-check-replication-filters --ignore-databases mysql \
                    --truncate-replicate-table \
                    --quiet""" % (host,user,password,port)
    stat, output = subprocess.getstatusoutput(com_check)
    print(output)

def table_checmsum_info(user,password,host):
    sql = """SELECT 
                db, tbl, this_cnt, master_cnt,chunk_time,ts
            FROM
                repl_checksum.checksum
            WHERE
                (master_cnt <> this_cnt
                    OR master_crc <> this_crc
                    OR ISNULL(master_crc) <> ISNULL(this_crc));"""


    data = []
    try:
        db_connect = mysql_conn(user, password,host.split(':')[0], host.split(':')[1])
        db_connect.execute(sql)
        for row in db_connect.fetchall():
            w = ['<td>' + str(rows) + '</td>' for rows in row]
            w = " ".join(map(str, w))
            data.append('<tr>' + str(w[::]) + '</tr>')
    except Exception as e:
        print(e)
    return data

def check_master(user,password,host):
    master = ''
    slave = []
    for instance in host.split(','):
        ip = instance.split(':')[0]
        port = instance.split(':')[1]

        sql = """select host from information_schema.processlist where command like '%Binlog Dump%';"""
        try:
            db_connect = mysql_conn(user, password, ip, port)
            db_connect.execute(sql)

            if (db_connect.fetchall()):
                master = ip + ':' + port
            else:
                slave.append(ip + ':' + port)

        except Exception as e:
            print(e)
    return master,slave

def email_date_format(host,data):

    if data:
        email_date = """
         <div>
            <h2>%s table_checksum_info</h2>
            <table class='mytable'>
              <tr>
                <th>database</th>
                <th>table_name</th>
                <th>this_cnt</th>
                <th>master_cnt</th>
                <th>chunk_time</th>
                <th>ts</th>
              </tr>
              %s
            </table>
        </div><br/>
        """ % (host,"".join(map(str,data)))

        return email_date

def table_sync(user,password,host,port):
    #print sync sql
    com_sync = """pt-table-sync --print \
                --replicate=repl_checksum.checksum \
                h=%s,u=%s,p='%s',P=%s
                """ % (host,user,password,port)
    stat,output = subprocess.getstatusoutput(com_sync)
    print(output)

    #execute sync
    com_sync_exec = """pt-table-sync --execute \
                    --replicate=repl_checksum.checksum \
                    h=%s,u=%s,p='%s',P=%s
                    """ % (host, user, password, port)
    stat, output = subprocess.getstatusoutput(com_sync_exec)
    print(output)

def sendmail(send,password,recei,html_body,cluster):
    # print(html_body)
    now = datetime.datetime.now()
    yesterday = now + datetime.timedelta(days=-1)
    yesterday = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    message = MIMEText(html_body, 'html', 'utf-8')
    message['From'] = Header("DBA", 'utf-8')
    subject = '(%s) %s table checksum INFO(主从数据检测)' % (yesterday,cluster)
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL('smtp.mxhichina.com', 465)
        smtpObj.login(send, password)
        smtpObj.sendmail(send, recei, message.as_string())
        print ("email is send sucess")
    except smtplib.SMTPException as err:
        print (err)


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read("host.ini")
    # install_pt_tool()

    for cluster in config.sections():
        if cluster !='send_email' and cluster !='recei_email':
            cluster_info = dict(config.items(cluster))
            host = cluster_info.get('host')
            user = cluster_info.get('user')
            password = cluster_info.get('password')

            master,slave =  check_master(user,password,host)
            table_checmsum(user,password,master.split(':')[0],master.split(':')[1])
            repl_checksum_data = []
            for host in slave:
                if table_checmsum_info(user,password,host):
                    repl_checksum_data.append(email_date_format(host,table_checmsum_info(user,password,host)))

            if repl_checksum_data :
                send_mail = dict(config.items('send_email'))
                recei_email = dict(config.items('recei_email'))
                sendmail(send_mail.get('user'),send_mail.get('password'),recei_email.get('email'),html_data(repl_checksum_data),cluster)
                table_sync(user,password,master.split(':')[0],master.split(':')[1])

