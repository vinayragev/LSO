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
from pymongo import MongoClient

db = db()

class query :
    def change_status(request):
        post = input_POST(request)
        find = {"_id":ObjectId(post['query_id'])}
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        db.update(request=request,table='query',find=find,update={"query_status":int(post["query_status"])})
        return http_resp({"success":True,'message':"Order Status Changed"})

    def list(request,select={}):
        post = input_POST(request)
        find = {"deleted_at":0}
        if 'skip' in post and post['skip'] != '':
            skip = int(post['skip'])
        else:
            skip = 0
        find = {}
        find['shop'] = {'$ne':[]}
        if 'start_date' in post and 'end_date' in post:
            start_date = int(post['start_date'].replace('-',''))
            end_date = int(post['end_date'].replace('-',''))
            find['order_date'] = {"$lte": end_date,"$gte": start_date}
        elif 'start_date' in post:
            start_date = int(post['start_date'].replace('-',''))
            find['order_date'] = {"$lte": end_date}
        elif 'end_date' in post:
            start_date = int(post['end_date'].replace('-',''))
            find['order_date'] = {"$gt": start_date}
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        lookup = [
          {
              "from": "shop",
              "localField": "shop_id",
              "foreignField": "_id",
              "as": "shop",
          },{
              "from": "product",
              "localField": "product_id",
              "foreignField": "_id",
              "as": "product",
          },{
              "from": "option",
              "localField": "query_status",
              "foreignField": "option_value",
              "as": "query_status",
              "pipeline": [
                {"$match": {"select_name":"query_status"}},
              ],
          },{
              "from": "user",
              "localField": "user_id",
              "foreignField": "user_id",
              "as": "user",
          },
        ]
        if request.user.is_superuser == False:
            lookup[0]['pipeline'] = [{"$match":{"user_id":request.user.id}}]
        response = db.pipeline(request=request,table='query',skip=int(post['skip']),lookup=lookup,find=find)
        response['success'] = True
        FORM_TEXT = db.find(request=request,table='label',find={'page_name':'query_list'})
        option = db.find(request=request,table='option',find={'page_name':'query'})
        response['option'] = option['option']
        response['LANG_TEXT'] = list(FORM_TEXT['label'])[0]['label']
        return http_resp(response)

    def replay(request,select={}):
        post = input_POST(request)
        db.insert(request=request,table='message',insert={"query_id":ObjectId(post['query_id']),"query":post['replay']})
        lookup = [                    
            {
                "from": "user",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "user",
            }
        ]
        find = {"query_id":ObjectId(post['query_id'])}
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        response = db.pipeline(request=request,table='message',lookup=lookup,find=find,sort={"created_at":-1})
        response['success'] = True
        return http_resp(response)

    def view(request,select={}):
        post = input_POST(request)
        find = {}
        find['_id'] = ObjectId(post['query_id'])
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        lookup = [
          {
              "from": "shop",
              "localField": "shop_id",
              "foreignField": "_id",
              "as": "shop",
          },{
              "from": "product",
              "localField": "product_id",
              "foreignField": "_id",
              "as": "product",
          },{
              "from": "message",
              "localField": "_id",
              "foreignField": "query_id",
              "as": "message",
              "pipeline": [
                {"$lookup": 
                  {
                    "from": "user",
                    "localField": "user_id",
                    "foreignField": "user_id",
                    "as": "user",
                  }
                },
                {"$sort": {"created_at":-1}},
                {"$limit": 10},
              ],
          },{
              "from": "option",
              "localField": "query_status",
              "foreignField": "option_value",
              "as": "query_status",
              "pipeline": [
                {"$match": {"select_name":"query_status"}},
              ],
          },{
              "from": "user",
              "localField": "user_id",
              "foreignField": "user_id",
              "as": "user",
          },
        ]
        if request.user.is_superuser == False:
            lookup[0]['pipeline'] = [{"$match":{"user_id":request.user.id}}]

        response = db.pipeline(request=request,table='query',lookup=lookup,find=find)
        option = db.find(request=request,table='option',find={'page_name':'query'})
        response['option'] = option['option']
        FORM_TEXT = db.find(request=request,table='label',find={'page_name':'query_view'})
        response['LANG_TEXT'] = list(FORM_TEXT['label'])[0]['label']
        return http_resp(response)

