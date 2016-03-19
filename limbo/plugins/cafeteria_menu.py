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


def get_page(target_url, get_post = 1):
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


def menu(target_menu_time, loc):
    """
    Get KAIST cafeteria menu and return it
    :param target_menu_time: Morning/Lunch/Dinner by 1/2/3 respectively
    :param loc: 0: 동측, 1: 서측, 2: 문지
    :return:
    """

    cafeteria_menu_url_template = 'http://m.kaist.ac.kr/_prog/fodlst/index.php' \
                                  '?site_dvs_cd=kr&menu_dvs_cd=050303&dvs_cd=fclt' \
                                  '&dvs_cd=%s&stt_dt=%s-%s-%s&site_dvs=mobile'
    cafeteria_menu_url_template_dic = {
        0: 'east1',
        1: 'west',
        2: 'icc'
    }
    location_name_dic = {
        0: '동측',
        1: '서측',
        2: '문지'
    }

    today_date = datetime.datetime.now().strftime("%Y-%m-%d").split('-')
    target_url = cafeteria_menu_url_template % (cafeteria_menu_url_template_dic[loc],
                                                today_date[0], today_date[1], today_date[2])
    target_page = get_page(target_url)

    try:
        target_menu_result = re.search(r'<tbody>(?:.*?)<td[^>]*?>(.+?)</td>(?:.*?)<td[^>]*?>(.+?)</td>'
                                       r'(?:.*?)<td[^>]*?>(.+?)</td>',
                                       target_page,
                                       re.DOTALL | re.IGNORECASE | re.UNICODE)
        target_menu = target_menu_result.group(target_menu_time)

        target_menu = target_menu.replace('<br />', '')
        target_menu = target_menu.replace('&lt;', '<')
        target_menu = target_menu.replace('&gt;', '>')
        target_menu = target_menu.replace('&quot;', '"')

        target_menu = target_menu.strip()

        # Send a message to #general channel
        target_script = {
            1: '***오늘 %s 아침 메뉴***' % (location_name_dic[loc]),
            2: '***오늘 %s 점심 메뉴***' % (location_name_dic[loc]),
            3: '***오늘 %s 저녁 메뉴***' % (location_name_dic[loc])
        }[target_menu_time]

        return target_script + "\n" + target_menu
    except AttributeError:
        # No menu in the page
        return ':crying_cat_face: 메뉴 정보가 없어요. :crying_cat_face:'


def on_message(msg, server):
    """
    Print KAIST cafeteria menu
    :param msg:
    :param server:
    :return:
    """
    is_food_channel = msg.get("channel") == u'C030P72AH'

    if not is_food_channel:
        return None

    text = msg.get("text", "")

    east_match = re.findall(unicode('동측\?'), text, re.UNICODE)
    if east_match:
        loc = 0
    else:
        west_match = re.findall(unicode('서측\?'), text, re.UNICODE)
        if west_match:
            loc = 1
        else:
            moonji_match = re.findall(unicode('문지\?'), text, re.UNICODE)
            if moonji_match:
                loc = 2
            else:
                return None

    time_now_hour = int(datetime.datetime.now().strftime("%H"))

    if time_now_hour < 10:
        # morning
        return menu(1, loc)
    elif time_now_hour < 14:
        # lunch
        return menu(2, loc)
    elif time_now_hour < 19:
        # dinner
        return menu(3, loc)
    else:
        return "내일 ㄱㄱ"


