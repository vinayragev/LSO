from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .lib import db
from .function import http_resp,input_POST,pre
import json
import re
from .shop import shop
from .product import product
from bson import json_util, ObjectId
from datetime import datetime,timedelta
from pymongo import MongoClient

db = db()

class order :
    def list(request,select={}):
        post = input_POST(request)
        find = {"deleted_at":0}
        if 'skip' in post and post['skip'] != '':
            skip = int(post['skip'])
        else:
            skip = 0
        find = {}
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        find['user'] = {"$ne":[]}
        find['shop'] = {'$ne':[]}
        if 'order_status' in post:
            find['order_status'] = int( post['order_status'])
        if 'start_date' in post:
            start_date = post['start_date'].split('-')
            find['created_at'] = {"$gte": datetime(year=int(start_date[0]),month=int(start_date[1]),day=int(start_date[2]))}
        if 'end_date' in post:
            end_date = post['end_date'].split('-')
            find['created_at'] = {"$lte": datetime(year=int(end_date[0]),month=int(end_date[1]),day=int(end_date[2]))}
        lookup = [
          {
              "from": "shop",
              "localField": "shop_id",
              "foreignField": "_id",
              "as": "shop",
              "pipeline": [
                {"$match": {"user_id":request.user.id}},
              ],
          },{
              "from": "option",
              "localField": "order_status",
              "foreignField": "option_value",
              "as": "status",
              "pipeline": [
                {"$match": {"select_name":"order_status"}},
              ],
          },{
              "from": "user",
              "localField": "user_id",
              "foreignField": "user_id",
              "as": "user",
          },
        ]
        response = db.pipeline(request=request,table='order',skip=int(post['skip']),lookup=lookup,find=find,sort={"created_at":-1})
        response['success'] = True
        FORM_TEXT = db.find(request=request,table='label',find={'page_name':'order_list'})
        option = db.find(request=request,table='option',find={'page_name':'order_form'})
        response['option'] = option['option']
        response['LANG_TEXT'] = list(FORM_TEXT['label'])[0]['label']
        return http_resp(response)

    def change_status(request):
        post = input_POST(request)
        db.update(request=request,table='order',find={"_id":ObjectId(post['order_id'])},update={"order_status":int(post["order_status"])})
        return http_resp({"success":True,'message':"Order Status Changed"})

    def view(request,select={}):
        post = input_POST(request)
        find = {}
        find['_id'] = ObjectId(post['order_id'])
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        lookup = [
          {
            "from": "cart",
            "localField": "_id",
            "foreignField": "order_id",
            "as": "cart",
            "pipeline": [
              {
                "$lookup": {
                  "from": "product",
                  "localField": "product_id",
                  "foreignField": "_id",
                  "as": "product",
                  "pipeline": [
                    {
                        "$lookup": {
                          "from": "option",
                          "localField": "product_qty_type",
                          "foreignField": "option_value",
                          "as": "qty_type",
                          "pipeline": [
                            {
                              "$match": {
                                "select_name":
                                  "product_qty_type",
                              },
                            },
                          ],
                        },
                      }
                  ],
                },
              },
              {
                "$lookup": {
                  "from": "product_photo",
                  "localField": "product_id",
                  "foreignField": "product_id",
                  "as": "product_photo",
                  "pipeline": [
                    {
                      "$limit": 1,
                    },
                  ],
                },
              },
              {
                "$lookup": {
                  "from": "product_price",
                  "localField": "product_price_id",
                  "foreignField": "_id",
                  "as": "product_price",
                },
              },
            ],
          },{
              "from": "shop",
              "localField": "shop_id",
              "foreignField": "_id",
              "as": "shop",
          },{
              "from": "user",
              "localField": "user_id",
              "foreignField": "user_id",
              "as": "user",
          },
          {
              "from": "option",
              "localField": "order_status",
              "foreignField": "option_value",
              "as": "order_status",
              "pipeline": [
                  {"$match": {"select_name":"order_status"}},
              ],
            },
        ]
        response = db.pipeline(request=request,table='order',lookup=lookup,find=find)
        option = db.find(request=request,table='option',find={'page_name':'order_form'})
        response['option'] = option['option']
        FORM_TEXT = db.find(request=request,table='label',find={'page_name':'order_list'})
        response['LANG_TEXT'] = list(FORM_TEXT['label'])[0]['label']
        return http_resp(response)

