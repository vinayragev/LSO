from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .lib import db
from .function import http_resp,input_POST,pre
import json
import re
from .shop import shop
from .product import product
from .label import label
from bson import json_util, ObjectId

db = db()

class service_price :
    def add(request):
        post = input_POST(request)
        if 'TYPE' in post:
            if post['TYPE']=='GET_FORM_TEXT':
                response = {'success':True}
                FORM_TEXT = db.find(request=request,table='label',find={'page_name':'price_form'})
                response['LANG_TEXT'] = list(FORM_TEXT['label'])[0]['label']
                response['option'] = db.find(request=request,table='option',find={'page':'product_price'},sort={"option_value":1},limit=False)['option']
                find_shop = {"deleted_at": 0,"active": 1}
                if request.user.is_superuser == False:
                    find_shop['user_id'] = request.user.id
                response['shop'] = db.find(request=request,table='shop',find=find_shop,select={'shop_name':1})['shop']
                response['product'] = db.find(request=request,table='product',find={"_id":ObjectId(request.GET.get('product_id'))},select={'product_name':1,'product_manufacturer':1})['product']
                if 'product_id' in request.POST and request.POST['product_id'] !='' :
                    response['product'] = product.list(request=request,json=False)['product']
                return http_resp(response)
            elif post['TYPE']=='ADD_SHOP_PRODUCT':
                exist = db.count(request=request,table='product_price',find={"shop_id":ObjectId(post["shop_id"]),"product_id":ObjectId(post["product_id"]),"deleted_at":0})
                if exist:
                    return http_resp({'success':False,'message':'product already Added in your shop'})
                insert = {}
                insert["shop_id"]                     = ObjectId(post["shop_id"])
                insert["product_id"]                  = ObjectId(post["product_id"])
                insert["final_amount"]                = int(post["final_amount"].replace(',',''))
                insert["discount_percentage"]         = int(post["discount_percentage"].replace(',',''))
                insert["shop_product_msp"]            = int(post["shop_product_msp"].replace(',',''))
                insert["shop_product_price"]          = int(post["shop_product_price"].replace(',',''))
                insert["shop_product_tax"]            = int(post["shop_product_tax"])
                insert["shop_product_tax_percentage"] = int(post["shop_product_tax_percentage"])
                insert["active"]                      = int(post["active"])
                insert["active"]                      = int(post["active"])
                shop = db.find_one(request=request,table="shop",find={"_id":insert["shop_id"]})['shop']
                insert["currency"]                    = shop["currency"]
                insert["pincode"]                     = shop['pincode']
                db.insert(request=request,table='product_price',insert=insert)
                total_seller = db.count(request=request,table="product_price",find={"product_id":insert["product_id"],'deleted_at':0})
                db.update(request=request,table='product',find={"_id":insert["product_id"]},update={'total_seller':total_seller})
                return http_resp({'success':True,'message':'product Added in a shop'})

    def list(request,select={}):
        post = input_POST(request)
        find = {"deleted_at":0,"product":{'$ne':[]}}
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        if 'skip' in post and post['skip'] != '':
            skip = int(post['skip'])
        else:
            skip = 0
        if 'shop_id' in post:
            find['shop_id'] = ObjectId(post['shop_id'])
        if 'product_id' in post:
            find['product_id'] = ObjectId(post['product_id'])
        response = {'success':True}
        lookup = [
          {
            "from": "product",
            "localField": "product_id",
            "foreignField": "_id",
            "as": "product",
            "pipeline": [
              {
                "$lookup": {
                  "from": "product_photo",
                  "localField": "_id",
                  "foreignField": "product_id",
                  "as": "photo",
                  "pipeline": [{ "$limit": 1 }],
                },
              },
              { "$match": {"product":0} },
              { "$limit": 1 },
            ],
          },
          {
            "from": "shop",
            "localField": "shop_id",
            "foreignField": "_id",
            "as": "shop",
          },
        ]
        listing = db.pipeline(request=request,table='product_price',skip=skip,lookup=lookup,find=find)
        response['shop_product_count'] = listing['count_product_price']
        response['listing'] = listing['product_price']
        FORM_TEXT = db.find(request=request,table='label',find={'page_name':'price_list'})
        response['LANG_TEXT'] = list(FORM_TEXT['label'])[0]['label']
        return http_resp(response)

    def table(request,select={}):
        post = input_POST(request)
        find = {"deleted_at":0}
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        if 'skip' in post and post['skip'] != '':
            skip = int(post['skip'])
        else:
            skip = 0
        if 'product_id' in post:
            find['product_id'] = ObjectId(post['product_id'])
        response = {'success':True}
        lookup = [
            {
              "from": "shop",
              "localField": "shop_id",
              "foreignField": "_id",
              "as": "shop",
            },
            {"from":'option',"localField":'shop_product_condition',"foreignField":'option_value',"as":'product_condition',
                "pipeline":[{"$match": {'select_name':'shop_product_condition'}}]
            },
            {"from":'option',"localField":'shop_product_listing',"foreignField":'option_value',"as":'product_listing',
                "pipeline":[{"$match": {'select_name':'shop_product_listing'}}]
            }
        ]
        listing = db.pipeline(request=request,table='product_price',skip=skip,lookup=lookup,find=find)
        lookup = [{
                  "from": "product_photo",
                  "localField": "_id",
                  "foreignField": "product_id",
                  "as": "photo",
                  "pipeline": [{ "$limit": 1 }],
                }]
        product = db.pipeline(request=request,table='product',lookup=lookup,find={"_id":ObjectId(post['product_id'])})
        option = db.find(request=request,table='option',find={"page":'shop_product'})
        response['shop_product_count'] = listing['count_product_price']
        response['listing'] = listing['product_price']
        response['product'] = product['product']
        response['option']  = option['option']
        FORM_TEXT = db.find(request=request,table='label',find={'page_name':'price_list'})
        response['LANG_TEXT'] = list(FORM_TEXT['label'])[0]['label']
        return http_resp(response)

    def edit(request):
        post = input_POST(request)
        update = {}
        update["final_amount"]                = int(post["final_amount"].replace(',',''))
        update["discount_percentage"]         = int(post["discount_percentage"].replace(',',''))
        update["shop_product_msp"]            = int(post["shop_product_msp"].replace(',',''))
        update["shop_product_price"]          = int(post["shop_product_price"].replace(',',''))
        update["shop_product_tax"]            = int(post["shop_product_tax"])
        update["shop_product_tax_percentage"] = int(post["shop_product_tax_percentage"])
        update["active"]                      = int(post["active"])
        find = {'_id':ObjectId(post["price_id"])}
        exist_price  = db.find_one(request=request,table="cart",find={'product_price_id':ObjectId(post["price_id"]),"order_id":{"$ne":0}})
        if exist_price['count_cart']:
            db.update(request=request,table='product_price',find={'_id':ObjectId(post["price_id"])},update={"deleted_at":request.user.id})
            price = db.insert(request=request,table='product_price',insert=update)
            db.update(request=request,table='cart',find={'product_price_id':ObjectId(post["price_id"])},update={"product_price_id":price.inserted_id})
            db.update(request=request,table='query',find={'product_price_id':ObjectId(post["price_id"])},update={"product_price_id":price.inserted_id})
            price_id = str(price.inserted_id)
        else:
            db.update(request=request,table='product_price',find=find,update=update)
            price_id =  post['price_id']
        return http_resp({'success':True,"price_id":price_id,'message':'product Updated'})

    def form(request):
        post = input_POST(request)
        if 'price_id' in post:
            find = {'_id' : ObjectId(post['price_id'])}
            lookup = [
                {'from':'product','localField':'product_id','foreignField':'_id','as':'product'},
                {'from':'shop','localField':'shop_id','foreignField':'_id','as':'shop'}
            ]
            if request.user.is_superuser == False:
                lookup[1]['pipeline'] = [{ "$match": { "user_id":request.user.id}, }]
            select = {
                "shop_id":1,
                "product_id":1,
                "final_amount":1,
                "discount_percentage":1,
                "shop_product_msp":1,
                "shop_product_price":1,
                "shop_product_tax":1,
                "shop_product_tax_percentage":1,
                "active":1,
                "product":{"product_name":1,"product_manufacturer":1},
                "shop":{"shop_name":1},
            }
            response = db.pipeline(request=request,table='product_price',lookup=lookup,find=find,select=select)
        else:
            response = {}
            response['product'] = db.find(request=request,table='product',find={"_id":ObjectId(post['product_id'])})['product']
        response['LANG_TEXT'] = label.find_one(request=request,find={'page_name':'service_price_form','language':post['language']})['label']
        response['shop'] = shop.list(request=request,json=False,select={'shop_name':1})['shop']
        response['option'] = db.find(request=request,table='option',find={'page_name':'product_price_form'},sort={"option_value":1},limit=False)['option']
        response['success'] = True
        return http_resp(response)

    # @csrf_exempt
    def delete(request):
        post = input_POST(request)
        find = {}
        find['_id'] = ObjectId(post['price_id'])
        if request.user.is_superuser == False:
            find['user_id'] = request.user.id
        db.delete(request=request,table='product_price',find=find)
        return http_resp({'success':True,'message':'product Deleted'})
