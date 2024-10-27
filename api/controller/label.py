from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .lib import db
from .function import http_resp,pre,input_POST,get_auth_user
import json
import re
from bson import json_util, ObjectId
db = db()

class label :
    def add(request):
        Auth_User = get_auth_user(request)
        if Auth_User.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        if request.method == 'POST':
            post = input_POST(request)
            insert = {}
            insert['page_name']    = post['page_name']
            insert['label']        = json.loads(post['label'])
            insert['language']     = post['language']
            insert["active"]       = int(post['active'])
            exist = db.find(request=request,table='label',find={"page_name":post['page_name'],"language":post['language']})
            if exist['count_label']:
                return http_resp({'success':True,"message":"label already Added"})
            db.insert(request=request,table='label',insert=insert)
            return http_resp({'success':True,"message":"label Added"})
        else:
            return http_resp({'success':False,"message":"Only POST"})

    def list(request,select={},json=True):        
        Auth_User = get_auth_user(request)
        if Auth_User.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        post = input_POST(request)
        if request.method == 'POST':
            find = {}
            if 'search' in post and post['search']!='':
                find['page_name'] = {'$regex':post['search']}
            if 'skip' in post and post['skip']!='':
                skip = int(post['skip'])
            else:
                skip = 0
            response = db.find(request=request,table='label',skip=skip,find=find,select={'page_name':1,"language":1})
            response['status'] = True
            response['LANG_TEXT'] = label.find_one(request=request,find={'page_name':'label_list'})['label']
            return http_resp(response)
        else:
            return http_resp({'success':False})

    def edit(request):
        Auth_User = get_auth_user(request)
        if Auth_User.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        post = input_POST(request)
        find = {'_id':ObjectId(post['label_id'])}
        update = {}
        update['page_name']    = post['page_name']
        update['label']        = json.loads(post['label'])
        update['language']     = post['language']
        update["active"]       = int(post['active'])
        db.update(request=request,table='label',find=find,update=update)
        return http_resp({'success':True,'message':'Change Success'})

    def view(request):
        Auth_User = get_auth_user(request)
        if Auth_User.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        post = input_POST(request)
        response = db.find(request=request,table='label',find={"_id":ObjectId(post['label_id'])})
        response['LANG_TEXT'] = label.find_one(request=request,find={'page_name':'label_form'})['label']
        return http_resp(response)

    def form(request):
        Auth_User = get_auth_user(request)
        if Auth_User.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        post = input_POST(request)
        if 'label_id' in post:
            response = db.find(request=request,table='label',find={"_id":ObjectId(post['label_id'])})
        else:
            response = {}
        response['LANG_TEXT'] = label.find_one(request=request,find={'page_name':'label_form'})['label']
        return http_resp(response)

    # @csrf_exempt
    def delete(request):
        Auth_User = get_auth_user(request)
        if Auth_User.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        post = input_POST(request)
        find = {}
        find['_id'] = ObjectId(post['label_id'])
        db.delete(request=request,table='label',find=find)
        return http_resp({'success':True,'message':'label Deleted'})

    def find_one(request,find={}):
        Auth_User = get_auth_user(request)
        label =  db.find_one(request=request,table='label',find=find)
        return label['label']

    def get(request,find={}):
        Auth_User = get_auth_user(request)
        post = input_POST(request)
        find = {'language':post['language'],'page_name':post['page_name']}
        label =  db.find_one(request=request,table='label',find=find)['label']['label']
        option =  db.find(request=request,table='option',find={"page_name":post['page_name']})['option']

        return http_resp({'success':True,'LANG_TEXT':label,'option':option})

