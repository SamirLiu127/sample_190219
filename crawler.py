#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient

URI = 'mongodb+srv://user_01:mCpvS3ThcK9hKfv@cluster0-lcunt.gcp.mongodb.net'
uri = 'mongodb://user_01:mCpvS3ThcK9hKfv@cluster0-lcunt.gcp.mongodb.net/test?retryWrites=true'


def main():
    conn = MongoClient(URI)
    db = conn.rent_house
    collection = db.rent591
    collection.insert_one({'test': 123, 'test2': 432})

    return


if __name__ == '__main__':
    main()
