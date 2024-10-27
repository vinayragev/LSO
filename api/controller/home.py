from datetime import datetime,timedelta
from django.shortcuts import render, HttpResponse, redirect
from .lib import db
from .function import http_resp,pre,input_POST
import re
from pymongo import MongoClient
from bson import json_util, ObjectId
from .category import category

db = db()

class home :
    def shop(request):
        response = {'success':True} 
        post = input_POST(request)
        find = {"deleted_at":0}
        andfind = []
        if 'search' in post:
            for x in post['search'].split(' '):
                if x!='':
                    andfind.append({"regex_search":{"$regex":x.lower()}},)
        if andfind != []:
            find["$and"] = andfind
        if 'pincode' in post:
            find["pincode"] = int(post['pincode'])
        if 'skip' in post and post['skip']!='':
            skip = int(post['skip'])
        else:
            skip = 0
        select = {"shop_name": 1,"latitude": 1,"longitude": 1,"full_address": 1,"star": 1,"mobile": 1,"banner": 1,"distance": {"$let": {"vars": {"a": {"$add": [{"$pow": [{"$sin": {"$divide": [{"$subtract": [{"$degreesToRadians": float(post['latitude'])},{"$degreesToRadians": "$latitude"}]},2]}},2]},{"$multiply": [{"$cos": {"$degreesToRadians": "$latitude"}},{"$cos": {"$degreesToRadians": float(post['latitude'])}},{"$pow": [{"$sin": {"$divide": [{"$subtract": [{"$degreesToRadians": float(post['longitude'])},{"$degreesToRadians": "$longitude"}]},2]}},2]}]}]}},"in": {"$multiply": [6373,2,{"$atan2": [{ "$sqrt": "$$a" },{ "$sqrt": { "$subtract": [1, "$$a"] } }]}]}}}}
        if 'shop_order' in post and post['shop_order']!='':
            shop_order = int(post['shop_order'])
            if shop_order==0:
                sort = {'distance':1}
            elif shop_order==1:
                sort = {"shop.star":-1,"total_review":-1}
        else:
            sort = {'distance':1}
        response = db.pipeline(request=request,table='shop',find=find,skip=skip,select=select,sort=sort)

        if 'shop_order' not in post or post['shop_order']=='':
            response['option'] = db.find(request=request,table='option',find={'page':'home_shop'},sort={"option_value":1},limit=False,select={"option_name":1,"select_name":1,"_id":0,"option_value":1})['option']
        return http_resp(response)

    def search(request):
        response = {'success':True} 
        post = input_POST(request)
        find = {"deleted_at":0}
        lookup = [
            {
                "from": 'shop',
                "localField": 'shop_id',
                "foreignField": '_id',
                "as": 'shop',
                "pipeline": [{"$match": {'deleted_at':0}}]
            },
            {
                "from": 'product',
                "localField": 'product_id',
                "foreignField": '_id',
                "as": 'product',
                "pipeline": [
                    {
                        "$lookup": {
                            "from": 'product_photo',
                            "localField": '_id',
                            "foreignField": 'product_id',
                            "as": 'product_photo',
                        }
                    },
                    {"$match": {'deleted_at':0,"total_seller":{"$gt":0}}},{"$limit": 1}
                ]
            }
        ]
        andfind = []
        # if 'country' in post and post['country']!='':
        #     lookup[0]['pipeline'][0]['$match']['country'] = post['country']
        if 'pincode' in post and post['pincode']!='':
            lookup[0]['pipeline'][0]['$match']['pincode'] = int(post['pincode'])
        if 'search' in post:
            for x in post['search'].split(' '):
                if x!='':
                    andfind.append({"regex_search":{"$regex":x.lower()}})
            if andfind != []:
                lookup[1]['pipeline'][1]['$match']['$and'] = andfind
        find["product"] = {'$ne':[]}
        find["shop"] = {'$ne':[]}
        if 'pincode' in post and post['pincode']!='':
            lookup[0]['pipeline'][0]['$match']['pincode'] = int(post['pincode'])
        if 'min_price' in post and post['min_price'] not in ['0',''] and 'max_price' in post and post['max_price'] not in ['0','']:
            find["final_amount"] = {"$gte":int(post['min_price'].replace(',','')),"$lte":int(post['max_price'].replace(',',''))}
        elif 'min_price' in post and post['min_price'] not in ['0','']:
            find["final_amount"] = {"$gte":int(post['min_price'].replace(',',''))}
        elif 'max_price' in post and post['max_price'] not in ['0','']:
            find["final_amount"] = {"$lte":int(post['max_price'].replace(',',''))}
        if 'shop_product_condition' in post and post['shop_product_condition']!='':
            find["shop_product_condition"] = int(post['shop_product_condition'])
        if 'shop_product_listing' in post and post['shop_product_listing']!='':
            find["shop_product_listing"] = int(post['shop_product_listing'])
        if 'product_order' in post and post['product_order']!='':
            product_order = int(post['product_order'])
            if product_order==0:
                sort = {'distance':1}
            elif product_order==1:
                sort = {"product_price.final_amount":1}
            elif product_order==2:
                sort = {"product_price.final_amount":-1}
            elif product_order==3:
                sort = {"shop.star":-1,"total_review":-1}
        else:
            sort = {'distance':1}
        if "skip" in post:
            skip = int(post['skip'])
        else:
            skip = 0



        response = db.pipeline(request=request,table='product_price',lookup=lookup,find=find,skip=skip,sort={"total_review":-1})
        response['success'] = True
        return http_resp(response)

    def add_to_cart(request):
        post = input_POST(request)
        product_price = db.find_one(request=request,table='product_price',find={'_id':ObjectId(post['product_price_id'])})
        result =  db.find_one(request=request,table='cart',find={'active':1,'order_id':0,'user_id':request.user.id,'product_price_id':ObjectId(post['product_price_id'])})
        data = {
            'qty':1,
            'product_price_id':ObjectId(post['product_price_id']),
            "product_id":product_price['product_price']['product_id'],
            "shop_id":product_price['product_price']['shop_id'],
            "done":1,
            "star":0,
            "active":1,
        }
        if result['count_cart']>0:
            data['qty'] = result['cart']['qty']+1
            db.update(request=request,table='cart',find={'_id':result['cart']['_id']},update=data)
        else:
            data['order_id'] = 0
            db.insert(request=request,table='cart',insert=data)
        response = {}
        response['success'] = True
        response['message'] = "Product Added"
        return http_resp(response)

    def remove_from_cart(request):
        post = input_POST(request)
        db.per_delete(request=request,table='cart',find={'user_id':request.user.id,'_id':ObjectId(post['cart_id'])})
        response = {}
        response['success'] = True
        response['message'] = "Cart removed"
        return http_resp(response)

    def user_book_now(request):
        post = input_POST(request)
        find = {}
        shop_id = ObjectId(request.POST['shop_id'])
        find['seller_id'] = db.find_one(request=request,table="shop",find={"_id":shop_id})['shop']['user_id']
        find['shop_id'] = shop_id
        find['user_id'] = request.user.id
        find['order_status'] = 0
        user = db.find_one(request=request,table="user",find = {'user_id':request.user.id})['user']
        address_find = {}
        address_find['country'] = user['country']
        address_find['state']   = user['state']
        address_find['city']    = user['city']
        address_find['zipcode'] = int(user['zipcode'])
        address_find['address'] = user['address']
        address_exist = db.find_one(request=request,table="address",find=address_find)
        if address_exist['count_address']:
            address_id = address_exist['address']['_id']
        else:
            address_id = db.insert(request=request,table="address",insert=address_find)
            address_id = address_id.inserted_id

        find['address_id'] = address_id
        order = db.insert(request=request,table='order',insert=find)
        order_id = order.inserted_id
        response = db.find(request=request,table='cart',find={"shop_id":ObjectId(post['shop_id']),"user_id":request.user.id,"active":1})
        total_money = 0
        total_cart = 0
        for x in response['cart']:
            total_cart += 1
            product_price = db.find_one(request=request,table="product_price",find = {'_id':x['product_price_id']})['product_price']
            total_money += product_price['final_amount']
            db.update(request=request,table='cart',find={'_id':x['_id']},update={"order_id":order_id,"active":0})
        db.update(request=request,table='order',find={'_id':order_id},update={"total_money":total_money,"total_cart":total_cart})
        response = {}
        response['success'] = True
        response['message'] = "Order Placed"
        return http_resp(response)

    def user_send_query(request):
        post = input_POST(request)
        insert = {}
        insert['product_price_id'] = ObjectId(post['product_price_id'])
        product_price = db.find_one(request=request,table='product_price',find={'_id':ObjectId(post['product_price_id'])})['product_price']
        insert['shop_id']          = product_price['shop_id']
        insert['seller_id'] = db.find_one(request=request,table="shop",find={"_id":product_price['shop_id']})['shop']['user_id']
        insert['user_id'] = request.user.id
        insert['product_id']       = product_price['product_id']
        exist = db.find_one(request=request,table='query',find=insert)
        if exist['count_query']:
            query_id = exist['query']["_id"]
            db.update(request=request,table='query',find={"_id":query_id},update={"query_status":0})
        else:
            insert['user_id']          = request.user.id
            insert['query_status']     = 0
            query = db.insert(request=request,table='query',insert=insert)
            query_id = query.inserted_id
        db.insert(request=request,table='message',insert={"query_id":query_id,"query":post['query']})
        return http_resp({"success":True,'message':"Query Send to Seller"})

    def product_detail(request):
        post = input_POST(request)
        product_id=ObjectId(post['product_id'])
        lookup = [
            {"from": "product_photo", "localField": "_id", "foreignField": "product_id", "as": "photos"},
            {"from": "cart","localField": "_id","foreignField": "product_id","as": "cart","pipeline": [{"$match": {"star": { "$in": [0, 1, 2, 3, 4, 5] }}}]},
            {"from":"option","localField":"product_qty_type","foreignField":"option_value","as":"qty_type",
                "pipeline":[
                    {"$match":{"select_name":"product_qty_type"}}
                ]
            },

        ]
        select = {
            "product_name":1,
            "product_manufacturer":1,
            "product_desc":1,
            "product_qty":1,
            "photos":{"file_url":1},
            "qty_type":{"option_name":1},
            "star":1,
        }
        response = db.pipeline(request=request,table="product",lookup=lookup,find={"_id":product_id},select=select,limit=10)
        response['option'] = db.find(request=request,table='option',find={'select_name':{"$in":["product_order","shop_product_condition","shop_product_listing"]}},sort={"option_value":1},limit=False,select={"option_name":1,"select_name":1,"_id":0,"option_value":1})['option']

        # pre(list(response['option']))
        response['geolocation'] = 'https://www.google.com/maps?q='
        response['success'] = True
        return http_resp(response)

    def search_filter_select(request):
        response = db.find(request=request,table='option',find={'select_name':{"$in":["product_order","shop_product_condition","shop_product_listing"]}},sort={"option_value":1},limit=False,select={"option_name":1,"select_name":1,"_id":0,"option_value":1})
        response['success'] = True
        return http_resp(response)

    def product_shop_list(request):
        post = input_POST(request)
        product_id=ObjectId(post['product_id'])
        lookup = [
            {
                'from':'product_price',
                'localField':'_id',
                'foreignField':'shop_id',
                'as':'product_price',
                "pipeline":[
                    {
                       "$lookup":{
                            "from":"option",
                            "localField":"shop_product_condition",
                            "foreignField":"option_value",
                            "as":"product_condition",
                            "pipeline":[
                                {"$match":{"select_name":"shop_product_condition"}}
                            ]
                        }
                    },
                    {"$match":{"product_id":product_id,"deleted_at":0}},
                ]
            },
        ]
        select = {"shop_name": 1,"latitude": 1,"longitude": 1,"full_address": 1,"star": 1,"distance": {"$let": {"vars": {"a": {"$add": [{"$pow": [{"$sin": {"$divide": [{"$subtract": [{"$degreesToRadians": float(post['latitude'])},{"$degreesToRadians": "$latitude"}]},2]}},2]},{"$multiply": [{"$cos": {"$degreesToRadians": "$latitude"}},{"$cos": {"$degreesToRadians": float(post['latitude'])}},{"$pow": [{"$sin": {"$divide": [{"$subtract": [{"$degreesToRadians": float(post['longitude'])},{"$degreesToRadians": "$longitude"}]},2]}},2]}]}]}},"in": {"$multiply": [6373,2,{"$atan2": [{ "$sqrt": "$$a" },{ "$sqrt": { "$subtract": [1, "$$a"] } }]}]}}},"product_price": 1}
        find = {"product_price":{"$ne":[]}}
        if 'min_price' in post and post['min_price'] not in ['0',''] and 'max_price' in post and post['max_price'] not in ['0','']:
            lookup[0]["pipeline"][1]["$match"]["final_amount"] = {"$gte":int(post['min_price'].replace(',','')),"$lte":int(post['max_price'].replace(',',''))}
        elif 'min_price' in post and post['min_price'] not in ['0','']:
            lookup[0]["pipeline"][1]["$match"]["final_amount"] = {"$gte":int(post['min_price'].replace(',',''))}
        elif 'max_price' in post and post['max_price'] not in ['0','']:
            lookup[0]["pipeline"][1]["$match"]["final_amount"] = {"$lte":int(post['max_price'].replace(',',''))}
        if 'shop_product_condition' in post and post['shop_product_condition']!='':
            lookup[0]["pipeline"][1]["$match"]["shop_product_condition"] = int(post['shop_product_condition'])
        if 'shop_product_listing' in post and post['shop_product_listing']!='':
            lookup[0]["pipeline"][1]["$match"]["shop_product_listing"] = int(post['shop_product_listing'])
        if 'pincode' in post and post['pincode']!='':
            find['pincode'] = int(post['pincode'])
        if 'product_order' in post and post['product_order']!='':
            product_order = int(post['product_order'])
            if product_order==0:
                sort = {'distance':1}
            elif product_order==1:
                sort = {"product_price.final_amount":1}
            elif product_order==2:
                sort = {"product_price.final_amount":-1}
            elif product_order==3:
                sort = {"shop.star":-1,"total_review":-1}
        else:
            sort = {'distance':1}
        if "skip" in post:
            skip = int(post['skip'])
        else:
            skip = 0
        response = db.pipeline(request=request,table='shop',find=find,lookup=lookup,select=select,sort=sort,skip=skip,limit=10)
        response['geolocation'] = 'https://www.google.com/maps?q='
        response['success'] = True
        return http_resp(response)

    def service_detail(request):
        post = input_POST(request)
        product_id=ObjectId(post['product_id'])
        lookup = [
            {"from": "product_photo", "localField": "_id", "foreignField": "product_id", "as": "photos"},
            {"from": "cart","localField": "_id","foreignField": "product_id","as": "cart","pipeline": [{"$match": {"star": { "$in": [0, 1, 2, 3, 4, 5] }}}]},
        ]
        select = {
            "product_name":1,
            "product_desc":1,
            "photos":{"file_url":1},
            "star":1,
        }
        response = db.pipeline(request=request,table="product",lookup=lookup,find={"_id":product_id},select=select,limit=10)
        response['option'] = db.find(request=request,table='option',find={'select_name':{"$in":["product_order","shop_product_condition","shop_product_listing"]}},sort={"option_value":1},limit=False,select={"option_name":1,"select_name":1,"_id":0,"option_value":1})['option']

        # pre(list(response['option']))
        response['geolocation'] = 'https://www.google.com/maps?q='
        response['success'] = True
        return http_resp(response)

    def service_shop_list(request):
        post = input_POST(request)
        product_id=ObjectId(post['product_id'])
        lookup = [
            {
                'from':'product_price',
                'localField':'_id',
                'foreignField':'shop_id',
                'as':'product_price',
                "pipeline":[
                    {"$match":{"product_id":product_id,"deleted_at":0}},
                ]
            },
        ]
        select = {"shop_name": 1,"latitude": 1,"longitude": 1,"full_address": 1,"star": 1,"distance": {"$let": {"vars": {"a": {"$add": [{"$pow": [{"$sin": {"$divide": [{"$subtract": [{"$degreesToRadians": float(post['latitude'])},{"$degreesToRadians": "$latitude"}]},2]}},2]},{"$multiply": [{"$cos": {"$degreesToRadians": "$latitude"}},{"$cos": {"$degreesToRadians": float(post['latitude'])}},{"$pow": [{"$sin": {"$divide": [{"$subtract": [{"$degreesToRadians": float(post['longitude'])},{"$degreesToRadians": "$longitude"}]},2]}},2]}]}]}},"in": {"$multiply": [6373,2,{"$atan2": [{ "$sqrt": "$$a" },{ "$sqrt": { "$subtract": [1, "$$a"] } }]}]}}},"product_price": 1}
        find = {"product_price":{"$ne":[]}}
        if 'min_price' in post and post['min_price'] not in ['0',''] and 'max_price' in post and post['max_price'] not in ['0','']:
            lookup[0]["pipeline"][1]["$match"]["final_amount"] = {"$gte":int(post['min_price'].replace(',','')),"$lte":int(post['max_price'].replace(',',''))}
        elif 'min_price' in post and post['min_price'] not in ['0','']:
            lookup[0]["pipeline"][1]["$match"]["final_amount"] = {"$gte":int(post['min_price'].replace(',',''))}
        elif 'max_price' in post and post['max_price'] not in ['0','']:
            lookup[0]["pipeline"][1]["$match"]["final_amount"] = {"$lte":int(post['max_price'].replace(',',''))}
        if 'pincode' in post and post['pincode']!='':
            find['pincode'] = int(post['pincode'])
        if 'product_order' in post and post['product_order']!='':
            product_order = int(post['product_order'])
            if product_order==0:
                sort = {'distance':1}
            elif product_order==1:
                sort = {"product_price.final_amount":1}
            elif product_order==2:
                sort = {"product_price.final_amount":-1}
            elif product_order==3:
                sort = {"shop.star":-1,"total_review":-1}
        else:
            sort = {'distance':1}
        if "skip" in post:
            skip = int(post['skip'])
        else:
            skip = 0
        response = db.pipeline(request=request,table='shop',find=find,lookup=lookup,select=select,sort=sort,skip=skip,limit=10)
        response['geolocation'] = 'https://www.google.com/maps?q='
        response['success'] = True
        return http_resp(response)

    def seller_product(request):
        post = input_POST(request)
        shop_id = ObjectId(post['shop_id'])
        sort = {}
        find = {'shop_id':shop_id}
        find['product'] = {'$ne':[]}
        lookup = [
            {
                "from": "product",
                "localField": "product_id",
                "foreignField": "_id",
                "as": "product",
                "pipeline":[
                    {
                        "$lookup":{
                            "from":"option","localField":"product_qty_type","foreignField":"option_value","as":"qty_type",
                            "pipeline":[{"$match":{"select_name":"product_qty_type"}}]
                        }
                    },
                    {'$match':{"product":1}}
                ]
            },{
                "from": "product_photo",
                "localField": "product_id",
                "foreignField": "product_id",
                "as": "photos",
                "pipeline":[{"$match":{"deleted_at":0}},{"$limit":1}]
            }
        ]
        if 'skip' in post and post['skip']!='':
            skip = int(post['skip'])
        else:
            skip = 0
        if 'search' in post:
            andfind = []
            for x in post['search'].split(' '):
                if x !='':
                    andfind.append({"regex_search":{"$regex":x}},)
            lookup[0]['pipeline'].append({"$match":{'$and':andfind}})
        # select = {"currency": 1,"final_amount": 1,"discount_percentage": 1,"shop_product_msp": 1,"final_amount": 1,"shop_product_qty": 1,"product": {"product_name": 1,"product_photo": 1,"product_manufacturer": 1},"qty_type": { "option_name": 1 },"cart": { "qty": 1 },"photos": {"file_url":1}}
        response = db.pipeline(request=request,table='product_price',lookup=lookup,skip=skip,find=find)
        response['success'] = True
        return http_resp(response)

    def seller_service(request):
        post = input_POST(request)
        shop_id = ObjectId(post['shop_id'])
        sort = {}
        find = {'shop_id':shop_id}
        find['product'] = {'$ne':[]}
        lookup = [
            {
                "from": "product",
                "localField": "product_id",
                "foreignField": "_id",
                "as": "product",
                "pipeline":[
                    {'$match':{"product":0}}
                ]
            },{
                "from": "product_photo",
                "localField": "product_id",
                "foreignField": "product_id",
                "as": "photos",
                "pipeline":[{"$match":{"deleted_at":0}},{"$limit":1}]
            }
        ]
        if 'skip' in post and post['skip']!='':
            skip = int(post['skip'])
        else:
            skip = 0
        if 'search' in post:
            andfind = []
            for x in post['search'].split(' '):
                if x !='':
                    andfind.append({"regex_search":{"$regex":x}},)
            lookup[0]['pipeline'].append({"$match":{'$and':andfind}})
        response = db.pipeline(request=request,table='product_price',lookup=lookup,skip=skip,find=find)
        response['success'] = True
        return http_resp(response)

    def seller_cart_list(request):
        post = input_POST(request)
        shop_id = ObjectId(post['shop_id'])
        find = {'shop_id':shop_id}
        find['cart'] = {'$ne':[]}
        lookup = [
            {
                "from": "product",
                "localField": "product_id",
                "foreignField": "_id",
                "as": "product",
                "pipeline": [
                    {
                        '$lookup':{
                            "from":"option",
                            "localField":"product_qty_type",
                            "foreignField":"option_value",
                            "as":"qty_type",
                            "pipeline":[{"$match":{"select_name":"product_qty_type"}}]
                        }
                    }
                ]
            },{
                "from": "product_photo",
                "localField": "product_id",
                "foreignField": "product_id",
                "as": "photos",
                "pipeline":[{"$match":{"deleted_at":0}},{"$limit":1}]
            },{
                "from":'cart',
                "localField":'_id',
                "foreignField":'product_price_id',
                "as":'cart',
                "pipeline":[                          {
                        "$match": {
                          "order_id": 0,
                        },
                      },
                ]
            },
        ]
        response = db.pipeline(request=request,table='product_price',lookup=lookup,find=find)
        response['success'] = True
        return http_resp(response)

    def seller_order_list(request):
        post = input_POST(request)
        shop_id = ObjectId(post['shop_id'])
        find = {'_id':shop_id}
        # select = {"banner":1,"owner_full_name":1,"shop_name":1,"info":1,"mobile":1,"open_since":1,"email":1,"latitude":1,"longitude":1,"full_address":1,"pincode":1,"city":1,"state":1,"country":1,"order":{"order_status":1,"created_at":1},"option":{"option_name":1}}
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
                        },
                    },
                ],
            },
            {
                "from": "option",
                "localField": "order_status",
                "foreignField": "option_value",
                "as": "order_status",
                "pipeline": [
                    {
                        "$match": {
                            "select_name": "order_status",
                        },
                    },
                ],
            },
        ]
        if 'skip' in post and post['skip']!='':
            skip = int(post['skip'])
        else:
            skip = 0
        response = db.pipeline(request=request,table='order',find={"shop_id":shop_id,"user_id":request.user.id},lookup=lookup,skip=skip,sort={"created_at":-1})
        response['success'] = True
        return http_resp(response)

    def seller_detail(request):
        post = input_POST(request)
        shop_id = ObjectId(request.POST['shop_id'])
        response = db.find(request=request,table='shop',find={'_id':shop_id})
        return http_resp(response)

    def user_profile_detail(request):
        post = input_POST(request)
        response = db.find_one(request=request,table='user',find={"user_id":request.user.id})
        response['success'] = True
        return http_resp(response)

    def user_profile_update(request):
        post = input_POST(request)
        update = {}
        update["name"]    = post['name']
        update["phone"]   = post['phone']
        update["dob"]     = post['dob']
        update["gender"]  = post['gender']
        update["city"]    = post["city"]
        update["country"] = post["country"]
        update["state"]   = post["state"]
        update["zipcode"] = post["zipcode"]
        update["address"] = post["address"]







        db.update(request=request,table='user',find={"user_id":request.user.id},update=update)
        return http_resp({"success":True,'message':"Profile Updated"})

    def change_cart_status(request):
        post = input_POST(request)
        cart = db.find_one(request=request,table='cart',find={'_id':ObjectId(post['cart_id'])})
        if cart['cart']['done']==0:
            done = 1
        else:
            done = 0
        db.update(request=request,table='cart',find={'user_id':request.user.id,'_id':ObjectId(post['cart_id'])},update={"done":done})
        return http_resp({"success":True})

    def user_order_list(request):
        post = input_POST(request)
        lookup = [
          {
            "from": "shop",
            "localField": "shop_id",
            "foreignField": "_id",
            "as": "shop",
          },
          {
            "from": "option",
            "localField": "order_status",
            "foreignField": "option_value",
            "as": "order_status",
            "pipeline": [
              { "$match": { "select_name": "order_status" } },
            ],
          },
        ]
        if 'skip' in post and post['skip']!='':
            skip = int(post['skip'])
        else:
            skip = 0
        find = {"user_id":request.user.id}
        sort = {"created_at":-1}
        response = db.pipeline(request=request,table='order',find=find,sort=sort,skip=skip,lookup=lookup)
        response['success'] = True
        return http_resp(response)

    def user_query_list(request):
        post = input_POST(request)
        find = {"user_id":request.user.id}
        lookup = [
          {
              "from": "shop",
              "localField": "shop_id",
              "foreignField": "_id",
              "as": "shop",
              # "pipeline": [
              #   {"$match": {"user_id":request.user.id}},
              # ],
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
          },
        ]
        response = db.pipeline(request=request,table='query',lookup=lookup,find=find)
        response['success'] = True
        return http_resp(response)

    def user_address_add(request):
        post = input_POST(request)
        insert = {}
        insert['country'] = post['country']
        insert['state']   = post['state']
        insert['city']    = post['city']
        insert['zipcode'] = post['zipcode']
        insert['address'] = post['address']
        db.insert(request=request,table="address",insert=insert)

        response = {}
        response['success'] = True
        return http_resp(response)

    def user_address_edit(request):
        post = input_POST(request)
        find = {"user_id":request.user.id}
        response = db.pipeline(request=request,table='address',find=find)
        response['success'] = True
        return http_resp(response)

    def user_address_delete(request):
        post = input_POST(request)
        find = {"user_id":request.user.id}
        response = db.pipeline(request=request,table='address',find=find)
        response['success'] = True
        return http_resp(response)

    def user_address_list(request):
        post = input_POST(request)
        find = {"user_id":request.user.id}
        response = db.pipeline(request=request,table='address',find=find)
        response['success'] = True
        return http_resp(response)

    def user_cart_list(request):
        post = input_POST(request)
        find = {}
        find['cart'] = {'$ne':[]}
        lookup = [
            {
              "from": "cart",
              "localField": "_id",
              "foreignField": "shop_id",
              "as": "cart",
              "pipeline": [
                {
                    "$lookup": {
                        "from": "product_price",
                        "localField": "product_price_id",
                        "foreignField": "_id",
                        "as": "product_price",
                    },
                },{
                    "$lookup": {
                        "from": "product",
                        "localField": "product_id",
                        "foreignField": "_id",
                        "as": "product",
                        "pipeline":[
                           {
                                "$lookup": {
                                    "from":"option",
                                    "localField":"product_qty_type",
                                    "foreignField":"option_value",
                                    "as":"qty_type",
                                    "pipeline":[
                                        {"$match":{"select_name":"product_qty_type"}}
                                    ]
                                },
                            },{
                                "$lookup": {
                                  "from": "product_photo",
                                  "localField": "_id",
                                  "foreignField": "product_id",
                                  "as": "product_photo",
                                  "pipeline": [
                                    {
                                      "$limit": 1,
                                    },
                                  ],
                                },
                              },
                        ]
                    },
                  },
                  { "$match": { "user_id": request.user.id ,"order_id": 0 ,'product_price':{"$ne":[]}} },
              ],
            },
        ]
        response = db.pipeline(request=request,table='shop',lookup=lookup,find=find)
        response['success'] = True
        return http_resp(response)

    def user_add_review(request):
        post = input_POST(request)
        db.update(request=request,table='cart',find={"_id":ObjectId(post['cart_id'])},update={"star":int(post['star'])})
        cart = db.find_one(request=request,table="cart",find={"_id":ObjectId(post['cart_id'])},select={})['cart']
        product = db.find_one(request=request,table="cart",find={"product_id":cart['product_id'],'star':{"$ne":0}},select={"star":{ "$avg": "$star" }})['cart']
        product_total_review = db.count(request=request,table="cart",find={"product_id":cart['product_id'],'star':{"$ne":0}})
        db.update(request=request,table="product",find={"_id":cart['product_id']},update={"star":product['star'],"total_review":product_total_review})
        shop = db.find_one(request=request,table="cart",find={"shop_id":cart['shop_id']},select={"star":{ "$avg": "$star" }})['cart']
        db.update(request=request,table="shop",find={"_id":cart['shop_id'],'star':{"$ne":0}},update={"star":shop['star']})
        star_1 = db.count(request=request,table="cart",find={"shop_id":cart['shop_id'],"star":1})
        star_2 = db.count(request=request,table="cart",find={"shop_id":cart['shop_id'],"star":2})
        star_3 = db.count(request=request,table="cart",find={"shop_id":cart['shop_id'],"star":3})
        star_4 = db.count(request=request,table="cart",find={"shop_id":cart['shop_id'],"star":4})
        star_5 = db.count(request=request,table="cart",find={"shop_id":cart['shop_id'],"star":5})
        update = {}
        update['star_1'] = star_1
        update['star_2'] = star_2
        update['star_3'] = star_3
        update['star_4'] = star_4
        update['star_5'] = star_5
        update['total_review'] = db.count(request=request,table="cart",find={"shop_id":cart['shop_id'],"star":{"$ne":0}})
        db.update(request=request,table="shop",find={"_id":cart['shop_id']},update=update)
        return http_resp({"success":True,'message':"Review Added"})

    def user_order_token(request):
        post = input_POST(request)
        order = db.find_one(request=request,table='order',find={"_id":ObjectId(post['order_id'])})
        total_order_token = db.count(request=request,table='order',find={"shop_id":ObjectId(order['order']['shop_id'])})
        current_order_token = db.count(request=request,table='order',find={'order_status':0,"shop_id":ObjectId(order['order']['shop_id'])})
        user_order_token = db.count(request=request,table='order',find={"shop_id":ObjectId(order['order']['shop_id']),"created_at":{"$lte":order['order']['created_at']}})
        response = {}
        response['current_order_token'] = total_order_token-current_order_token+1
        response['user_order_token']    = user_order_token
        response['total_order_token']   = total_order_token
        return http_resp(response)

    def user_order_detail(request):
        post = input_POST(request)
        find = {}
        find['cart'] = {'$ne':[]}
        find['_id'] = ObjectId(post['order_id'])
        lookup = [
          {
              "from": "shop",
              "localField": "shop_id",
              "foreignField": "_id",
              "as": "shop",
          },{
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
                        "pipeline":[
                            {
                                "$lookup": {
                                    "from":"option",
                                    "localField":"product_qty_type",
                                    "foreignField":"option_value",
                                    "as":"qty_type",
                                    "pipeline":[
                                        {"$match":{"select_name":"product_qty_type"}}
                                    ]
                                },
                            },{
                                "$lookup": {
                                    "from": "product_photo",
                                    "localField": "_id",
                                    "foreignField": "product_id",
                                    "as": "product_photo",
                                    "pipeline": [{"$limit": 1,}]
                                },
                            },
                        ]
                    },
                },{
                    '$lookup':{
                        "from": "product_price",
                        "localField": "product_price_id",
                        "foreignField": "_id",
                        "as": "product_price",
                    },
                }
            ]
          },{
              "from": "option",
              "localField": "order_status",
              "foreignField": "option_value",
              "as": "order_status",
              "pipeline": [
                {"$match": {"select_name":"order_status"}},
              ],
          },
        ]
        response = db.pipeline(request=request,table='order',find=find,lookup=lookup)
        order = db.find_one(request=request,table='order',find={"_id":ObjectId(post['order_id'])})
        total_order_token = db.count(request=request,table='order',find={"shop_id":ObjectId(order['order']['shop_id'])})
        current_order_token = db.count(request=request,table='order',find={'order_status':0,"shop_id":ObjectId(order['order']['shop_id'])})
        user_order_token = db.count(request=request,table='order',find={"shop_id":ObjectId(order['order']['shop_id']),"created_at":{"$lte":order['order']['created_at']}})
        response['current_order_token'] = total_order_token-current_order_token+1
        response['user_order_token']    = user_order_token
        response['total_order_token']   = total_order_token
        return http_resp(response)

    def user_query_replay(request):
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
        response = db.pipeline(request=request,table='message',lookup=lookup,find=find,sort={"created_at":-1})
        response['success'] = True
        return http_resp(response)

    def user_query_detail(request):
        find = {}
        post = input_POST(request)
        find['_id'] = ObjectId(post['query_id'])
        lookup = [
          {
              "from": "shop",
              "localField": "shop_id",
              "foreignField": "_id",
              "as": "shop"
          },
          {
              "from": "product",
              "localField": "product_id",
              "foreignField": "_id",
              "as": "product"
          },
          {
              "from": "message",
              "localField": "_id",
              "foreignField": "query_id",
              "as": "message",
              "pipeline":[
                {"$match":{"query_id":ObjectId(post['query_id'])}},
                {
                  "$lookup":{
                      "from": "user",
                      "localField": "user_id",
                      "foreignField": "user_id",
                      "as": "user",

                  }
                },
                {"$sort":{"created_at":-1}},
                {"$limit":10},
              ]
          },
        ]
        response = db.pipeline(request=request,table='query',find=find,lookup=lookup)
        response['success'] = True
        return http_resp(response)
