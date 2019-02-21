#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

MONGODB_URI = 'mongodb+srv://user_01:mCpvS3ThcK9hKfv@cluster0-lcunt.gcp.mongodb.net'


def get_mongodb_collection():
    """

    :return: mongodb collection
    """
    conn = MongoClient(MONGODB_URI)
    db = conn.rent_house
    return db.rent591


def update_region_house(region, row=0):
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

    houses_data = []
    for h in houses:
        data = {
            'post_id': h['post_id'],
            'title': h['address_img_title'],
            'region_name': h['regionname'],
            'section_name': h['sectionname'],
            'kind_name_img': h['kind_name_img'],  # 現況
            'price': h['price'],
            'linkman': h['linkman'],
            'nick_name': h['nick_name'],
        }
        data.update(get_house_info(h['post_id']))
        houses_data.append(data)
    collection.insert_many(houses_data)

    row += len(houses)
    records = int(response['records'].replace(',', ''))
    if row < records:
        update_region_house(region, row=row)
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
    try:
        info = {
            'phone_number': soup.select_one('.dialPhoneNum').get('data-value', ''),
            'house_kind': soup.select('.attr li')[2].text.split('\xa0').pop()
        }
    except IndexError:
        print(url)
        info = {
            'phone_number': soup.select_one('.dialPhoneNum').get('data-value', ''),
            'house_kind': 'unknown'
        }
    except:
        print(url)
        info = {
            'phone_number': 'unknown',
            'house_kind': 'unknown'
        }
    return info


if __name__ == '__main__':
    collection = get_mongodb_collection()
    # update_region_house(25)
    update_region_house(1)
    update_region_house(3)
    # https://rent.591.com.tw/rent-detail-5912594.html
