from django.shortcuts import render, HttpResponse, redirect
from .lib import db
from .function import http_resp,pre,input_POST,get_auth_user
import re
from pymongo import MongoClient
from .label import label
from bson import json_util, ObjectId

db = db()

class admin() :
    def profile(request):
        post = input_POST(request)
        Auth_User = get_auth_user(request)
        response = db.find_one(request=request,table='user',find={'user_id':Auth_User.id})
        response['LANG_TEXT'] = label.find_one(request=request,find={'page_name':'profile_edit','language':post['language']})
        response['success'] = True
        return http_resp(response)

    def profile_edit(request):
        Auth_User = get_auth_user(request)
        post = input_POST(request)
        update = {}
        update["name"]     = post["name"]
        update["phone"]    = post["phone"]
        update["country"]  = post["country"]
        update["state"]    = post["state"]
        update["city"]     = post["city"]
        update["areacode"] = post["areacode"]
        db.update(request=request,table="user",find={"user_id":Auth_User.id},update=update)
        return http_resp({"success":True,'message':"Profile Updated"})

    def dashboard(request):
        Auth_User = get_auth_user(request)
        post = input_POST(request)
        response = {"success":True}
        if request.user.is_superuser == True:
            response['order']         = db.count(request=request,table='order',find={})
            response['pending_order'] = db.count(request=request,table='order',find={'order_status':0})
            response['done_order']    = db.count(request=request,table='order',find={'order_status':{"$ne":0}})
            response['query']         = db.count(request=request,table='query',find={'query_status':0})
        else:
            response['order']         = db.count(request=request,table='order',find={"seller_id":Auth_User.id})
            response['pending_order'] = db.count(request=request,table='order',find={"seller_id":Auth_User.id,'order_status':0})
            response['done_order']    = db.count(request=request,table='order',find={"seller_id":Auth_User.id,'order_status':{"$ne":0}})
            response['query']         = db.count(request=request,table='query',find={"seller_id":Auth_User.id,'query_status':0})
        response['orer_list'] = db.find(request=request,table='order',sort={'created_at':-1},find={"seller_id":Auth_User.id,'order_status':0})
        return http_resp(response)
