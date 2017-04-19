import sys
import requests
import re
import time
import random
import sys
import codecs
from bs4 import BeautifulSoup

FOOD = 0
DELIVERY = 1


def get_page(target_url, get_post = 0):
    try:
        if 0 == get_post:
            response_one = requests.get(target_url)
        else:
            response_one = requests.post(target_url)

        if 200 == response_one.status_code:
            response_one.encoding = 'utf-8'
            return response_one.text
        else:
            return False
    except:
        print("Unexpected error:", sys.exc_info()[0])
        time.sleep(60 + random.random())
        return get_page(target_url, get_post)

        
def get_restaurants_list_from_bablabs(target_url):
    page = get_page(target_url)
    soup = BeautifulSoup(page, "lxml")
    rests = soup.findAll("div", {"class": "card-content store-item"})

    return ["\n".join([x.strip() for x in rest.stripped_strings]) for rest in rests]


def random_menu(menu_type):
    if menu_type == FOOD:
        # menu_list = codecs.open('./data/menu_list.txt', 'r', 'utf-8').readlines()
        target_url = "https://bds.bablabs.com/restaurants?campus_id=JEnfpqCUuR&type=local"
    elif menu_type == DELIVERY:
        # menu_list = codecs.open('./data/delivery_list.txt', 'r', 'utf-8').readlines()
        target_url = "https://bds.bablabs.com/restaurants?campus_id=JEnfpqCUuR&type=delivery"

    menu_list = get_restaurants_list_from_bablabs(target_url)

    return random.choice(menu_list).strip()


def on_message(msg, server):
    text = msg.get("text", "")
    
    menu_match1 = re.findall('점심\?', text)
    menu_match2 = re.findall('저녁\?', text)
    dilivery_match = re.findall('배달\?', text)

    is_food_channel = msg.get("channel") == u'C030P72AH'

    if not is_food_channel:
        return
            
    if menu_match1 or menu_match2:
        return random_menu(FOOD)
    elif dilivery_match:
        return random_menu(DELIVERY)


if __name__ == "__main__":
    print(random_menu(FOOD))
    print(random_menu(DELIVERY))
