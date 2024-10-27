from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .lib import db
from .function import http_resp,pre,handle_uploaded_file,delete_file,input_POST
from .label import label
from datetime import datetime,timedelta

import json
import re
from bson import json_util, ObjectId

db = db()

class shop :
    def add(request):
        post = input_POST(request)
        insert = {}
        insert['shop_name']       = re.sub(r'\s+', ' ', post['shop_name'])
        insert['owner_full_name'] = re.sub(r'\s+', ' ', post['owner_full_name'])
        insert['currency']        = post['currency']
        insert['shop_type']       = post['shop_type']
        insert['mobile']          = re.sub(r'\s+', ' ', post['mobile'])
        insert['email']           = re.sub(r'\s+', ' ', post['email'])
        insert['country']         = post['country']
        insert['pincode']         = int(post['pincode'])
        insert['open_since']      = post['open_since']
        insert['info']            = post['info']
        insert['state']           = post['state']
        insert['city']            = post['city']
        insert['full_address']    = re.sub(r'\s+', ' ', post['full_address'])
        insert['active']          = int(post['active'])
        insert['regex_search']    = insert['shop_name']+insert['owner_full_name']+insert['shop_type']+insert['mobile']+insert['email']+insert['country']+str(insert['pincode'])+insert['open_since']+insert['info']+insert['state']+insert['city']+insert['full_address']
        insert['regex_search']    = insert['regex_search'].lower()
        if 'photo' in post:
            insert['photo']           = post['photo']
        else:
            insert['photo']           = ''
        if 'banner' in post:
            insert['banner']           = post['banner']
        else:
            insert['banner']           = ''
        insert['latitude']        = float(post['latitude'])
        insert['longitude']       = float(post['longitude'])
        insert['active']    = int(post['active'])
        shop = db.insert(request=request,table='shop',insert=insert)




        open_time = json.loads(post['open_time'])
        close_time = json.loads(post['close_time'])
        shop_time = json.loads(post['time'])
        for x in shop_time:
            db.insert(request=request,table='shop_time',insert = {'shop_id':shop.inserted_id,"day":x[0],"open_time":x[1],"close_time":x[2]})

        shop = db.count(request=request,table="shop",find={"shop_type":insert['shop_type']})
        category = db.find_one(request=request,table="shop_category",find={"category_name":insert['shop_type']})
        if category['count_shop_category']:
            if category['shop_category']['total_shop']!=shop:
                db.update(request=request,table="shop_category",find={"_id":category['shop_category']['_id']},update={"total_shop":shop})
        else:
            db.insert(request=request,table="shop_category",insert={"total_shop":1,"category_name":insert['shop_type'],"regex_search":insert['shop_type'].lower()})
        
        # db.per_delete(request=request,table="delete_image",find={"file_url":insert['photo'],"file_type":"photo"})
        # db.per_delete(request=request,table="delete_image",find={"file_url":insert['banner'],"file_type":"banner"})
        return http_resp({'success':True,'message':'Shop Added'})

    def list(request,select={},json=True):
        post = input_POST(request)
        find = {}
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        if 'skip' in post and post['skip']!='':
            skip = int(post['skip'])
        else:
            skip = 0
        if 'shop_id' in post:
            find['_id'] = ObjectId(post.items()['shop_id'])
        if 'search' in post and post['search']!='':
            andfind = []
            for x in post['search'].split(' '):
                andfind.append({"regex_search":{"$regex":x}},)
            find['$and'] = andfind
            # find['regex_search'] = {'$regex':post['search']}
        response = db.find(request=request,table='shop',find=find,skip=skip,select=select)
        FORM_TEXT = db.find(request=request,table='label',find={'page_name':'shop_list'})
        response['LANG_TEXT'] = list(FORM_TEXT['label'])[0]['label']
        if json:
            return http_resp(response)
        return response

    # def product_price_list(request,select={}):
    #     find = {}
    #     post = input_POST(request)
    #     if 'skip' in request.POST and request.POST['skip']!='':
    #         skip = int(post['skip'])
    #     else:
    #         skip = 0
    #     if 'shop_id' in post:
    #         find['regex_search'] = ObjectId(post['shop_id'])
    #     listing = db.find(request=request,table='product_price',find=find,skip=skip,select=select)
    #     count = db.count(request=request,table='product_price',find=find)

    #     if 'JSON' not in post:
    #         return {'success':True,'listing':listing,'count':count}
    #     return http_resp({'success':True,'listing':listing,'count':count})

    def form(request):
        post = input_POST(request)
        if 'shop_id' in post:
            find = {"_id":ObjectId(post['shop_id'])}
            response = db.find_one(request=request,table='shop',find=find)
            response['shop_time'] = db.pipeline(request=request,table='shop_time',find={'shop_id':ObjectId(post['shop_id'])},sort={"day":1})['shop_time']
        else:
            response = {}
        response['status'] = True
        response['LANG_TEXT'] = label.find_one(request=request,find={'page_name':'shop_form'})['label']
        response['country']   = db.find(request=request,table='country',limit=False)['country']
        return http_resp(response)

    def type(request):
        post = input_POST(request)
        find = {}
        andfind = []
        if 'search' in post:
            for x in post['search'].split(' '):
                if x!='':
                    andfind.append({"regex_search":{"$regex":x.lower()}},)
        if andfind != []:
            find["$and"] = andfind
        response = db.find(request=request,table='shop',find=find,sort={"total_shop":-1},select = {'shop_type':1})
        return http_resp(response)

    def edit(request):
        find = {}
        post = input_POST(request)
        if 'shop_id' not in post:
            return http_resp({'success':False,'shop':'Chane Success'})
        find = {"_id":ObjectId(post['shop_id'])}
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        update={}
        update['shop_name']       = re.sub(r'\s+', ' ', post['shop_name'])
        update['owner_full_name'] = re.sub(r'\s+', ' ', post['owner_full_name'])
        update['currency']        = post['currency']
        update['shop_type']       = post['shop_type'].strip()
        update['mobile']          = re.sub(r'\s+', ' ', post['mobile'])
        update['email']           = re.sub(r'\s+', ' ', post['email'])
        update['country']         = post['country']
        update['pincode']         = int(post['pincode'])
        update['state']           = post['state']
        update['open_since']      = post['open_since']
        update['info']            = post['info']
        update['city']            = post['city']
        update['full_address']    = re.sub(r'\s+', ' ', post['full_address'])
        update['active']          = int(post['active'])
        update['regex_search']    = update['shop_name']+update['owner_full_name']+update['shop_type']+update['mobile']+update['email']+update['country']+str(update['pincode'])+update['open_since']+update['info']+update['state']+update['city']+update['full_address']
        update['regex_search']    = update['regex_search'].lower()
        update['banner']          = post['banner']
        update['photo']           = post['photo']
        update['latitude']        = float(post['latitude'])
        update['longitude']       = float(post['longitude'])
        shop_time = json.loads(post['time'])
        for x in shop_time:
            shop_time_exist = db.find_one(request=request,table='shop_time',find = {'shop_id':ObjectId(post['shop_id']),"day":x[0]})
            if shop_time_exist['count_shop_time']:
                if(shop_time_exist['shop_time']['open_time']!=x[1] or shop_time_exist['shop_time']['close_time']!=x[1]):
                    db.update(request=request,table='shop_time',find={"_id":shop_time_exist['shop_time']['_id']},update = {"open_time":x[1],"close_time":x[2]})
            else:
                db.insert(request=request,table='shop_time',insert = {'shop_id':ObjectId(post['shop_id']),"day":x[0],"open_time":x[1],"close_time":x[2]})
        db.update(request=request,table='shop',find=find,update=update)
        shop = db.count(request=request,table="shop",find={"shop_type":update['shop_type']})
        category = db.find_one(request=request,table="shop_category",find={"category_name":update['shop_type']})
        if category['count_shop_category']:
            db.update(request=request,table="shop_category",find={"_id":category['shop_category']['_id']},update={"total_shop":shop})
        else:
            db.insert(request=request,table="shop_category",insert={"total_shop":1,"category_name":update['shop_type'],"regex_search":update['shop_type'].lower()})
        return http_resp({'success':True,'message':'shop Updated Success'})

    # @csrf_exempt
    def delete(request):
        find = {}
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        find['_id'] = ObjectId(request.POST['shop_id'])
        db.delete(request=request,table='shop',find=find)
        return http_resp({'success':True,'message':'Shop Deleted'})

