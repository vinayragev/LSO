from django.shortcuts import render, HttpResponse, redirect
from .lib import db
from .function import http_resp,pre,input_POST
import re
from pymongo import MongoClient
from bson import json_util, ObjectId
from datetime import datetime,timedelta

db = db()

class user :
    def list(request,select={},json=True):        
        if request.user.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        post = input_POST(request)
        find = {}
        if 'search' in post and post['search']!='':
            find['email'] = {'$regex':post['search']}
        if 'skip' in post and post['skip']!='':
            skip = int(post['skip'])
        else:
            skip = 0
        response = db.find(request=request,table='user',skip=skip,find=find)
        response['status'] = True
        FORM_TEXT = db.find(request=request,table='label',find={'page_name':'user_list'})
        response['LANG_TEXT'] = list(FORM_TEXT['label'])[0]['label']
        return http_resp(response)

    def edit(request):
        if request.user.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        file_num = 0
        post = input_POST(request)
        find = {'_id':ObjectId(post['_id'])}
        update = {}
        update['name']   = post['name']
        update['bio']    = post['bio']
        update['active'] = post['active']
        db.update(request=request,table='user',find=find,update=update)
        return http_resp({'success':True,'message':'Chane Success'})

    def form(request):
        if request.user.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        post = input_POST(request)
        if 'user_id' in post:
            listing = db.find(request=request,table='user',find={"_id":ObjectId(post['user_id'])})
        else :
            listing = {}

        FORM_TEXT = db.find(request=request,table='label',find={'page_name':'user_form'})
        listing['FORM_TEXT'] = list(FORM_TEXT['label'])[0]['label']
        return http_resp(listing)

    def delete(request):
        if request.user.is_superuser == False:
            return http_resp({'success':False,"message":"You have no authorization"})
        post = input_POST(request)
        find = {}
        find['_id'] = ObjectId(post['user_id'])
        db.delete(request=request,table='user',find=find)
        return http_resp({'success':True,'message':'user Deleted'})

