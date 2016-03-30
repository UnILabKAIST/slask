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
# import MySQLdb
import json
import sqlite3


def db_connect(database_filename="archived_slack_msg.sqlite3"):
    return sqlite3.connect(database_filename)


def create_table(cursor, table_name):
    sql_template = """
    CREATE TABLE IF NOT EXISTS '{}' (
        'ts' timestamp NOT NULL,
        'user' char(12) NOT NULL,
        'text' text NOT NULL,
        PRIMARY KEY ('ts')
        )
    """
    cursor.execute(sql_template.format(table_name))


def insert_msg_into_db(each_msg):
    """

    :return:
    """
    channel_id = each_msg.get('channel')

    table_name = 'channel_%s' % channel_id.lower()
    insert_msg_template = 'insert or ignore into ' + table_name + ' (ts, user, text) values (?, ?, ?);'
    timestamp_one = datetime.datetime.fromtimestamp(int(float(each_msg.get('ts')))).strftime('%Y-%m-%d %H:%M:%S')

    db = db_connect()
    cursor = db.cursor()

    # check existence of table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(table_name))
    if cursor.rowcount < 1:
        create_table(cursor, table_name)

    try:
        cursor.execute(insert_msg_template, (timestamp_one, each_msg.get('user'), each_msg.get('text')))
    except KeyError:
        # Bot
        cursor.execute(insert_msg_template, (timestamp_one, each_msg.get('username'), each_msg.get('text')))

    db.commit()

    db.close()


def on_message(msg, server):
    """
    Insert msg into DB
    :param msg:
    :param server:
    :return:
    """
    # print(msg)
    try:
        insert_msg_into_db(msg)
    except:
        print("Error:\tarchiving_bot")
        print traceback.format_exc()

    return None



