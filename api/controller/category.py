from django.shortcuts import render, HttpResponse, redirect
from .lib import db
from .function import http_resp,pre,input_POST,get_auth_user
import re
from pymongo import MongoClient
from bson import json_util, ObjectId
from .label import label

db = db()

class category() :
    def add(request):
        Auth_User = get_auth_user(request)
        if request.method=='POST':
            if Auth_User.is_superuser == False:
                return http_resp({'success':False,"message":"You have no authorization"})
            post = input_POST(request)
            insert = {}
            insert["category_name"] = re.sub(r'\s+', ' ', post["category_name"])
            if "parent_id" in post and post["parent_id"]!='':
                insert["parent_id"] = ObjectId(post["parent_id"])
            else:
                insert["parent_id"] = ''
            insert["total_product"] = 0
            count = db.find(request=request,table = 'category',find=insert)
            if count['count_category']!=0:
                return http_resp({'success':True,'type':'error','message':'Category already exist'})
            insert["active"] = 1
            insert["regex_search"] = insert["category_name"].lower()
            db.insert(request=request,table='category',insert=insert)
            return http_resp({'success':True,'type':'success','message':'Category Added Successfully'})
        else:
            return http_resp({"success":False,"message":"Only POST"})

    def list(request):
        Auth_User = get_auth_user(request)
        if Auth_User.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        if request.method=='POST':
            find = {}
            post = input_POST(request)
            if 'skip' in post and post['skip']!='':
                skip = int(post['skip'])
            else:
                skip = 0
            if 'search' in post and post['search']!='':
                find['regex_search'] = {'$regex':post['search']}
                skip = 0
            if 'category_id' in post and post['category_id']!='':
                find['_id'] = ObjectId(post['category_id'])
            if 'category_name' in post and post['category_name']!='':
                find['category_name'] = post['category_name']
            if 'parent_id' in post and post['parent_id']!='':
                find['parent_id'] = ObjectId(post['parent_id'])
            response = db.pipeline(request=request,table='category',lookup=[{
                        "from": 'category',
                        "localField": 'parent_id',
                        "foreignField": '_id',
                        "as": 'parent'
                    }],find=find,skip=skip,sort = {'total_product':-1})
            response['success'] = True
            if skip==0:
                response['LANG_TEXT'] = label.find_one(request=request,find={'page_name':'category_list','language':post['language']})['label']
            return http_resp(response)
        else:
            return http_resp({"success":False,"message":"Only POST"})

    def search(request):
        Auth_User = get_auth_user(request)
        if Auth_User.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        if request.method=='POST':
            post = input_POST(request)
            find = {}
            if 'search' in post and post['search']!='':
                find['regex_search'] = {'$regex':post['search']}
            response = db.find(request=request,table='category',find=find,select={"category_name":1},sort = {'total_product':-1})
            response['success'] = True
            return http_resp(response)
        else:
            return http_resp({"success":False,"message":"Only POST"})


    def edit(request):
        Auth_User = get_auth_user(request)
        if Auth_User.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        post = input_POST(request)
        if request.method=='POST':
            post = input_POST(request)
            find = {}
            find['_id'] = ObjectId(post['category_id'])
            update = {}
            update["category_name"] = re.sub(r'\s+', ' ', post['category_name'])
            update["parent_id"] = post['parent_id']
            update["regex_search"] = update["category_name"].lower()
            if update["parent_id"]!='':
                update["parent_id"] = ObjectId(update["parent_id"])
            update["active"] = int(post['active'])
            db.update(request=request,table='category',find=find,update=update)
            return http_resp({'success':True,"update":update,'message':'Change Success'})

    def view(request):
        Auth_User = get_auth_user(request)
        if Auth_User.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        post = input_POST(request)
        if request.method=='POST':
            find = {'_id':ObjectId(post['category_id'])}
            lookup = [
                {"from": "category","localField": "parent_id","foreignField": "_id","as": "parent"},
            ]
            # select = {'category_name':1,'parent_id':1,'active':1,'parent':{'category_name':1}}
            response = db.pipeline(request=request,table='category',find=find,lookup=lookup,limit=1)
            response['success'] = True
            response['LANG_TEXT'] = label.find_one(request=request,find={'page_name':'category_form','language':post['language']})['label']
            return http_resp(response)

    def form(request):
        Auth_User = get_auth_user(request)
        if Auth_User.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        post = input_POST(request)
        if 'category_id' in post:
            find = {'_id':ObjectId(post['category_id'])}
            lookup = [
                {"from": "category","localField": "parent_id","foreignField": "_id","as": "parent"},
            ]
            # select = {'category_name':1,'parent_id':1,'active':1,'parent':{'category_name':1}}
            response = db.pipeline(request=request,table='category',find=find,lookup=lookup,limit=1)
        else:
            response = {}
        response['success'] = True
        response['LANG_TEXT'] = label.find_one(request=request,find={'page_name':'category_form','language':post['language']})['label']
        return http_resp(response)


    # @csrf_exempt
    def delete(request):
        Auth_User = get_auth_user(request)
        if Auth_User.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        post = input_POST(request)
        db.delete(request=request,table='category',find={'_id':ObjectId(post['category_id'])})
        return http_resp({'success':True,'type':'success','message':'Category Removed'})
