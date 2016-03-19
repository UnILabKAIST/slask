# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import re
import time
import random
import sys
import codecs

FOOD = 0
DELIVERY = 1

def get_page(target_url, get_post = 1):
    #print datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "Getting web page\t", target_url

    # check the web page is in HDD or not
    # wait
    #time.sleep(3 + random.random())

    try:
        if 1 == get_post:
            response_one = requests.get(target_url)
        else:
            response_one = requests.post(target_url)

        if 200 == response_one.status_code:
            response_one.encoding = 'utf-8'
            return response_one.text
        else:
            return False
    except:
        print "Unexpected error:", sys.exc_info()[0]
        time.sleep(60 + random.random())
        return get_page(target_url, get_post)


def random_menu(menu_type):
    if menu_type == FOOD:
        menu_list = codecs.open('./data/menu_list.txt', 'r', 'utf-8').readlines()
    elif menu_type == DELIVERY:
        menu_list = codecs.open('./data/delivery_list.txt', 'r', 'utf-8').readlines()

    return random.choice(menu_list).strip() + u"?"


def on_message(msg, server):
    text = msg.get("text", "")
    
    menu_match1 = re.findall(unicode('점심\?'), text, re.UNICODE)
    menu_match2 = re.findall(unicode('저녁\?'), text, re.UNICODE)
    dilivery_match = re.findall(unicode('배달\?'), text, re.UNICODE)

    is_food_channel = msg.get("channel") == u'C030P72AH'

    if not is_food_channel:
        return
            
    if menu_match1 or menu_match2:
        return random_menu(FOOD)
    elif dilivery_match:
        return random_menu(DELIVERY)
