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


def eastmenu(target_menu_time):
    east_cafeteria_menu_url_template = 'http://m.kaist.ac.kr/_prog/fodlst/index.php?site_dvs_cd=kr&menu_dvs_cd=050303&dvs_cd=fclt&dvs_cd=east1&stt_dt=%s-%s-%s&site_dvs=mobile'

    today_date = datetime.datetime.now().strftime("%Y-%m-%d").split('-')

    target_url = east_cafeteria_menu_url_template % (today_date[0], today_date[1], today_date[2])

    target_page = get_page(target_url)

    get_menu_pattern = re.compile(r'<tbody>(?:.*?)<td[^>]*?>(.+?)</td>(?:.*?)<td[^>]*?>(.+?)</td>(?:.*?)<td[^>]*?>(.+?)</td>', re.DOTALL | re.IGNORECASE | re.UNICODE)

    target_menu_result = get_menu_pattern.search(target_page)

    target_menu = target_menu_result.group(target_menu_time)

    target_menu = target_menu.replace('<br />', '')
    target_menu = target_menu.replace('&lt;', '<')
    target_menu = target_menu.replace('&gt;', '>')

    target_menu = target_menu.strip()

    # Send a message to #general channel
    target_script = {1:'***오늘 동측 아침 메뉴***',
    2: '***오늘 동측 점심 메뉴***',
    3: '***오늘 동측 저녁 메뉴***'}[target_menu_time]

    return target_script + "\n" + target_menu


def on_message(msg, server):
    text = msg.get("text", "")
    
    match = re.findall(ur'\ub3d9\uce21\?', text, re.UNICODE)
    is_food_channel = msg.get("channel") == u'C030P72AH'
    if not match or not is_food_channel:
        return

    time_now = int(datetime.datetime.now().strftime("%H"))

    if time_now < 10:
        # morning
        return eastmenu(1)
    elif time_now < 14:
        # lunch
        return eastmenu(2)
    elif time_now < 19:
        # dinner
        return eastmenu(3)
    else:
        return "내일 ㄱㄱ"


