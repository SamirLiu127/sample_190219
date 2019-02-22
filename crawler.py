#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

MONGODB_URI = 'mongodb+srv://user_01:mCpvS3ThcK9hKfv@cluster0-lcunt.gcp.mongodb.net'
sys.setrecursionlimit(3000)


def get_mongodb_collection():
    """

    :return: mongodb collection
    """
    conn = MongoClient(MONGODB_URI)
    db = conn.rent_house
    return db.house591


def update_region_house(region, row=0, houses_data=[]):
    """
    Update region house to mongodb
    :param region: region code, 台北市:1 新北市:3
    :param row: default 0
    :return: None
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Cookie': f'urlJumpIp={region}'
    }
    url = f'https://rent.591.com.tw/home/search/rsList?firstRow={row}'
    res = requests.get(url=url, headers=headers)
    response = res.json()
    houses = response['data']['data']

    for h in houses:
        data = {
            'post_id': h['post_id'],  # 物件ID
            'title': h['address_img_title'],  # 物件標題
            'region_name': h['region_name'],  # 縣市
            'section_name': h['section_name'],  # 區
            'street_name': h['street_name'],  # 路
            'alley_name': h['alley_name'],  # 巷
            'lane_name': h['lane_name'],  # 弄
            'addr_number_name': h['addr_number_name'],  # 號
            'floorInfo': h['floorInfo'],  # 樓
            'floor': h['floor'],  # 總樓層
            'layout': h['layout'],  # 格局
            'kind_name': h['kind_name'],  # 現況
            'icon_name': h['icon_name'],
            'price': h['price'],
            'unit': h['unit'],
            'linkman': h['linkman'],  # 聯絡人
            'nick_name': h['nick_name'],  # 聯絡人身份
            'update_time': h['ltime']
        }
        data.update(get_house_info(h['post_id']))
        houses_data.append(data)
    if len(houses_data) >= 300:
        COLLECTION.insert_many(houses_data)
        houses_data = []

    row += len(houses)
    records = int(response['records'].replace(',', ''))
    if row < records:
        update_region_house(region, row=row, houses_data=houses_data)
    try:
        COLLECTION.insert_many(houses_data)
    except BulkWriteError as exc:
        print(exc.details)
    return


def get_house_info(post_id):
    """

    :param post_id: house id
    :return: phone_number & house_kind
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }
    url = f'https://rent.591.com.tw/rent-detail-{post_id}.html'
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text.encode('utf-8'), "html.parser")

    house_kind_tag = soup.find('li', text=re.compile('型態'))
    house_kind = house_kind_tag.text.split('\xa0').pop() if house_kind_tag else ''

    phone_number_tag = soup.select_one('.dialPhoneNum')
    phone_number = phone_number_tag['data-value'] if phone_number_tag else ''

    gender_title_tag = soup.find('div', text=re.compile('性別要求'))
    gender = gender_title_tag.next_sibling.em.text if gender_title_tag else ''

    house_info_tag = soup.select_one('.houseIntro')
    house_info = house_info_tag.text if house_info_tag else ''
    return {
        'phone_number': phone_number,  # 聯絡人電話
        'house_kind': house_kind,  # 型態
        'gender': gender,  # 性別要求
        'house_info': house_info  # 屋況說明
    }


if __name__ == '__main__':
    COLLECTION = get_mongodb_collection()
    # update_region_house(25)
    update_region_house(1)
    print('region 1 Done!!')
    update_region_house(3)
    print('region 3 Done!!')
    # https://rent.591.com.tw/rent-detail-5912594.html

    # https://rent.591.com.tw/rent-detail-7287067.html
    # https://rent.591.com.tw/rent-detail-5890212.html
