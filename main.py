#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_pymongo import PyMongo


app = Flask(__name__)
swagger = Swagger(app, template_file='api.yaml')
app.config['MONGO_URI'] = "mongodb+srv://user_reader:8d8iNPusNaPgXfw@cluster0-lcunt.gcp.mongodb.net/rent_house"
mongo = PyMongo(app)


@app.route("/")
def home_page():
    return '<a href="/apidocs">Swagger API Document</>'


@app.route("/search")
def search():
    region = request.args.get('region', '')
    gender = request.args.get('gender', '')
    owner_name = request.args.get('owner_name', '')
    owner_gender = request.args.get('owner_gender', '')
    owner_self = request.args.get('owner_self', '')
    owner_phone = request.args.get('owner_phone', '')

    query = {}
    if region:
        query.update(get_region(region))
    if gender:
        query.update(get_gender(gender))
    if owner_name or owner_gender:
        query.update(get_owner(owner_name, owner_gender))
    if owner_self:
        query.update(get_owner_self(owner_self))
    if owner_phone:
        query.update(get_owner_phone(owner_phone))

    print(query)
    response = mongo.db.rent591.find(query)
    output = []
    for doc in response:
        del doc['_id']
        output.append(doc)
    return jsonify(output)


def get_region(num):
    data = {
        '1': '台北市',
        '3': '新北市'
    }
    return {"region_name": data.get(num, "台北市")}

def get_gender(gender):
    data = {
        '0': ["女生", "", "男女生皆可"],
        '1': ["男生", "", "男女生皆可"]
    }
    return {"gender": {"$in": data[gender]}}

def get_owner(owner_name, owner_gender):
    gender_data = {
        '0': "小姐",
        '1': "先生"
    }
    name = "^" + owner_name if owner_name else ".*"
    gender = gender_data[owner_gender] + "$" if owner_gender else ".*"
    return {"linkman": {"$regex": name + gender}}

def get_owner_self(owner_self):
    data = {
        '0': "^((?!屋主).)*$",
        '1': "^屋主.*"
    }
    return {"nick_name": {"$regex": data[owner_self]}}

def get_owner_phone(phone):
    return {"phone_number": {"$regex": f"^{phone}.*"}}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
