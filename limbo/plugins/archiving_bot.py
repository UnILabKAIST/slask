# -*- coding: utf-8 -*-
__author__ = 'NoSyu'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import re
import datetime
import time
import random
import sys
#import HTMLParser
import importlib
import os
import re
import sys
import time
import traceback
import datetime
import MySQLdb
import json


def db_connect():
    from config import config

    db = MySQLdb.connect(db=config['DBName'], user=config['User_Name'], passwd=config['Password'],
                         host=config['Hostname'], port = config['portnumber'], charset='utf8')

    db.query("set character_set_connection=utf8;")
    db.query("set character_set_server=utf8;")
    db.query("set character_set_client=utf8;")
    db.query("set character_set_results=utf8;")
    db.query("set character_set_database=utf8;")

    return db

def insert_msg_into_db(each_msg):
    """

    :return:
    """
    channel_id = each_msg.get('channel')

    table_name = 'channel_%s' % channel_id.lower()
    insert_msg_template = 'insert ignore into ' + table_name + ' (ts, user, text) values (%s, %s, %s);'
    timestamp_one = datetime.datetime.fromtimestamp(int(float(each_msg.get('ts')))).strftime('%Y-%m-%d %H:%M:%S')

    db = db_connect()
    cursor = db.cursor()

    try:
        cursor.execute(insert_msg_template, (timestamp_one, each_msg.get('user'), each_msg.get('text')))
    except KeyError:
        # Bot
        cursor.execute(insert_msg_template, (timestamp_one, each_msg.get('username'), each_msg.get('text')))

    db.commit()

    db.close()


def on_message(msg, server):
    """
    Insert msg into MySQL DB
    :param msg:
    :param server:
    :return:
    """
    #print msg
    #msg.get("channel")
    # try:
    #     insert_msg_into_db(msg)
    # except:
    #     pass

    return None



