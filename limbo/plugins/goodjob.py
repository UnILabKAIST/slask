# -*- coding: utf-8 -*-
__author__ = 'NoSyu'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random

def on_message(msg, server):
    """
    Print KAIST cafeteria menu
    :param msg:
    :param server:
    :return:
    """
    text = msg.get("text", "")

    response_list = [
        'ㄱㅅㄱㅅ',
        '기본이죠.',
        ':grinning:',
        ':smile_cat:'
   ]

    if ('잘했어' in text or 'good job' in text) and 'nosyubot' in text:
        random.shuffle(response_list)
        return response_list[0]



