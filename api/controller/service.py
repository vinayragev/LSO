from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .lib import db
from .category import category
from .function import http_resp,pre,input_POST,handle_uploaded_file
import json
import re
import os
from bson import json_util, ObjectId
from django.templatetags.static import static
from pymongo import MongoClient
import time
from datetime import datetime,timedelta

db = db()

class service :
    def add(request):
        post = input_POST(request)
        insert = {}
        insert['category_id']          = post['category_id']
        insert['product_name']         = re.sub(r'\s+', ' ', post['product_name'])
        insert['product_desc']         = post['product_desc']
        insert['regex_search']         = insert['product_name']+insert['category_id']+insert['product_desc']
        insert['regex_search']         = insert['regex_search'].lower()
        insert["active"]               = int(post['active'])
        insert["product"]              = 0
        insert["star"]                 = 0
        product_id = db.insert(request=request,table='product',insert=insert)
        product = db.count(request=request,table="product",find={"category_id":insert['category_id']})
        category = db.find_one(request=request,table="category",find={"category_name":insert['category_id']})
        if category['count_category']:
            db.update(request=request,table="category",find={"_id":category['category']['_id']},update={"total_product":product})
        else:
            db.insert(request=request,table="category",insert={"total_product":1,"category_name":insert['category_id'],"regex_search":insert['category_id'].lower()})
        product_id = product_id.inserted_id
        file_num = 0
        if 'product_photo' in post and post['product_photo']!='':
            product_photo = post['product_photo'].split(',')
            for x in product_photo:
                if x!='':
                    db.per_delete(request=request,table="delete_image",find={"file_url":x,"file_type":"product_photo_file"})
                    db.insert(request=request,table='product_photo',insert={'product_id':product_id,'file_url':x})
        return http_resp({'success':True,'message':'Service added Success'})

    def list(request,select={},json=True):
        post = input_POST(request)
        find = {'product':0}
        if 'skip' in post and post['skip']!='':
            skip = int(post['skip'])
        else:
            skip = 0
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        find['deleted_at'] = 0
        if 'product_id' in post:
            find['_id'] = ObjectId(post['product_id'])
        if 'search' in post and post['search']!='':
            andfind = []
            for x in post['search'].split(' '):
                andfind.append({"regex_search":{"$regex":x}},)
            find['$and'] = andfind
        lookup = [{'from': 'product_photo', 'localField': '_id', 'foreignField': 'product_id', 'as': 'photos',"pipeline":[{"$limit": 1}]}]
        select = {}
        response = db.pipeline(request=request,table='product',lookup=lookup,find=find,skip=int(post['skip']),select=select)
        FORM_TEXT = db.find(request=request,table='label',find={'page_name':'service_list'})
        response['LANG_TEXT'] = list(FORM_TEXT['label'])[0]['label']
        response['status'] = True
        if json:
            return http_resp(response)
        return response

    def form(request):
        post = input_POST(request)
        if 'product_id' in post:
            find = {'_id': ObjectId(post['product_id']),'deleted_at':0}
            if request.user.is_superuser == False:
                find['user_id'] = request.user.id
            lookup = [
                {'from': 'product_photo', 'localField': '_id', 'foreignField': 'product_id', 'as': 'photos'},
            ]
            select = {"category_id":1,"product_name":1,"product_desc":1,"active":1,"photos":{"file_url":1,"_id":1}}
            response = db.pipeline(request=request,table='product',find={'_id':ObjectId(post['product_id'])},lookup=lookup,select=select)
        else:
            response = {}
        response['option'] = db.find(request=request,table='option',find={'page':'product'},sort={"option_value":1},limit=False)['option']
        FORM_TEXT = db.find(request=request,table='label',find={'page_name':'service_form'})
        response['LANG_TEXT'] = list(FORM_TEXT['label'])[0]['label']
        response['status'] = True
        return http_resp(response)

    def edit(request):
        post = input_POST(request)
        if 'product_photo' in post and post['product_photo']!='':
            product_photo = post['product_photo'].split(',')
            for x in product_photo:
                if x!='':
                    db.insert(request=request,table='product_photo',insert={'product_id':ObjectId(post['product_id']),'file_url':x})
        find = {'_id':ObjectId(post['product_id'])}
        update = {}
        update['category_id']           = post['category_id']
        update['product_name']          = re.sub(r'\s+', ' ', post['product_name'])
        update['product_desc']          = post['product_desc']
        update["active"]                = int(post['active'])
        update['regex_search']          = update['product_name']+update['category_id']+update['product_desc']
        update['regex_search']          = update['regex_search'].lower()
        db.update(request=request,table='product',find=find,update=update)
        product = db.count(request=request,table="product",find={"category_id":update['category_id']})
        category = db.find_one(request=request,table="category",find={"category_name":update['category_id']})
        if category['count_category']:
            if category['category']['total_product']!=product:
                db.update(request=request,table="category",find={"_id":category['category']['_id']},update={"total_product":product})
        else:
            db.insert(request=request,table="category",insert={"total_product":1,"category_name":update['category_id'],"regex_search":update['category_id'].lower()})
        return http_resp({'success':True,'message':'Service Updated Success'})

    # @csrf_exempt
    def delete(request):
        post = input_POST(request)
        find = {}
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        find['_id'] = ObjectId(post['product_id'])
        db.delete(request=request,table='product',find=find)
        return http_resp({'success':True,'message':'Service Deleted'})

