#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

MONGODB_URI = 'mongodb+srv://user_01:mCpvS3ThcK9hKfv@cluster0-lcunt.gcp.mongodb.net'


def insert_mongodb(data):
    conn = MongoClient(MONGODB_URI)
    db = conn.rent_house
    collection = db.rent591
    collection.insert_one(data)


def get_region_total_rows(region, row=0, data=[]):
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
        data.append({
            'post_id': h['post_id'],
            'title': h['address_img_title']
        })

    row += len(houses)
    records = int(response['records'].replace(',', ''))
    if row < records:
        get_region_total_rows(region, row=row, data=data)
    return data


def main():
    data = get_region_total_rows(25)

    return


if __name__ == '__main__':
    main()
