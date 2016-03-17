# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = 'NoSyu'

from glob import glob
import importlib
import os
import re
from slackclient import SlackClient
import sys
import time
import traceback
import datetime
import MySQLdb
import json

from config import config

def run_hook(hook, data, server):
    responses = []
    for hook in hooks.get(hook, []):
        h = hook(data, server)
        if h: responses.append(h)

    return responses

def handle_message(client, event):
    # ignore bot messages and edits
    subtype = event.get("subtype", "")
    if subtype == "bot_message" or subtype == "message_changed": return

    botname = sc.server.login_data["self"]["name"]
    try:
        msguser = client.server.users.get(event["user"])
    except KeyError:
        print("event {0} has no user".format(event))
        return

    if msguser["name"] == botname or msguser["name"].lower() == "slackbot":
        return

    text = "\n".join(run_hook("message", event, {"client": client, "config": config, "hooks": hooks}))

    if text:
        client.rtm_send_message(event["channel"], text)



def db_connect():
    db = MySQLdb.connect(db=config['DBName'], user=config['User_Name'], passwd=config['Password'],
                         host=config['Hostname'], port = config['portnumber'], charset='utf8')

    db.query("set character_set_connection=utf8;")
    db.query("set character_set_server=utf8;")
    db.query("set character_set_client=utf8;")
    db.query("set character_set_results=utf8;")
    db.query("set character_set_database=utf8;")

    return db



def get_msg_insert_db(channel_id):
    """

    :return:
    """
    # Get history
    db = db_connect()
    cursor = db.cursor()
    resp1 = sc.api_call('channels.history', channel=channel_id, count=1000)
    msg_list = json.loads(resp1)['messages']
    table_name = 'channel_%s' % channel_id.lower()
    insert_msg_template = 'insert ignore into ' + table_name + ' (ts, user, text) values (%s, %s, %s);'

    for each_msg in msg_list:
        print(each_msg)
        timestamp_one = datetime.datetime.fromtimestamp(int(float(each_msg['ts']))).strftime('%Y-%m-%d %H:%M:%S')

        try:
            #target_sql = insert_msg_template % (table_name, timestamp_one, each_msg['user'], each_msg['text'])
            #print(target_sql)
            cursor.execute(insert_msg_template, (timestamp_one, each_msg['user'], each_msg['text']))
        except KeyError:
            # Bot
            cursor.execute(insert_msg_template, (timestamp_one, each_msg['username'], each_msg['text']))

    db.commit()

    db.close()


if __name__=="__main__":
    sc = SlackClient(config["token"])
    if sc.rtm_connect():

        # Get channel list
        create_table_template = 'CREATE TABLE IF NOT EXISTS `channel_%s` (`ts` timestamp NOT NULL, `user` char(12) NOT NULL, `text` text NOT NULL, PRIMARY KEY (`ts`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;'

        resp1 = sc.api_call('channels.list')
        channels_list = json.loads(resp1)['channels']

        for each_ele in channels_list:
            # Create Table
            #print(create_table_template % each_ele['id'].lower())

            # Insert msg to table
            print("%s\t%s" % (each_ele['id'], each_ele['name']))
            get_msg_insert_db(each_ele['id'])

        #print(channels_list.get('channels'))
        #print(resp1)


        #get_msg_insert_db('C03D64LER')
        #get_msg_insert_db('C024RFZ8L')


        #response = sc.api_call('channels.info', channel='C03D64LER')
        #print(response)


        """
        users = sc.server.users
        while True:
            events = sc.rtm_read()
            for event in events:
                #print "got {0}".format(event.get("type", event))
                handler = event_handlers.get(event.get("type"))
                if handler:
                    handler(sc, event)
            time.sleep(1)
    else:
        print("Connection Failed, invalid token <{0}>?".format(config["token"]))
        """