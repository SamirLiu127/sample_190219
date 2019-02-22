#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config.update(
    MONGO_URI="mongodb+srv://cluster0-lcunt.gcp.mongodb.net/rent_house",
    MONGO_USERNAME="user_01",
    MONGO_PASSWORD='mCpvS3ThcK9hKfv'
)
mongo = PyMongo(app)


@app.route("/")
def home_page():
    response = mongo.db.house591.find({
        "linkman": "\u5433"
    })
    print(response)
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
