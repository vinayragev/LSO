from datetime import datetime,timedelta
import os
import json
from bson import json_util, ObjectId
from bson.son import SON
from pymongo import MongoClient
myclient = MongoClient("mongodb://localhost:27017/")
mongo = myclient["project"]

class db(object):
    def insert(self,request,table,insert):
        mongodb = mongo[table]
        time_str = datetime.now()
        insert['active']     = 1
        insert['user_id']    = request.user.id
        insert['updated_at'] = time_str
        insert['created_at'] = time_str
        insert['deleted_at'] = 0
        return mongodb.insert_one(insert)

    def insert_many(self,request,table,insert):
        mongodb = mongo[table]
        time_str = datetime.now()
        insert['active']     = 1
        insert['user_id']    = request.user.id
        insert['updated_at'] = time_str
        insert['created_at'] = time_str
        insert['deleted_at'] = 0
        return mongodb.insert_many(insert)

    def pipeline(self,request,table,find={},skip=0,limit=10,select={},group={},sort={},lookup=[]):
        mongodb = mongo[table]
        pipeline = []
        for x in lookup:
            pipeline.append({"$lookup":x})
        find['deleted_at'] = 0
        count = mongodb.count_documents(find)
        pipeline.append({"$match":find})
        if group!={}:
            pipeline.append({"$group":group})
        if select!={}:
            pipeline.append({"$project":select})
        if sort != {}:
            pipeline.append({"$sort":sort})
        pipeline.append({"$skip":skip})
        pipeline.append({"$limit":limit})
        print("\n"+table)
        print(pipeline)
        print(skip)
        print("\n")
        mongodb = mongodb.aggregate(pipeline = pipeline)
        return {table:mongodb,'count_'+table:count}

    def find(self,request,table,find={},skip=0,limit=True,select={},sort={},pipeline=[]):
        mongodb = mongo[table]
        # print("\n")
        # print(select)
        # print("\n")
        find['deleted_at'] = 0
        count = mongodb.count_documents(find)
        if pipeline!=[]:
            mongodb = mongodb.aggregate(pipeline = pipeline)
        else:
            mongodb = mongodb.find(find,select)
            if sort:
                mongodb = mongodb.sort(sort)
            if limit:
                mongodb = mongodb.limit(10)
            mongodb = mongodb.skip(skip)
        return {table:mongodb,'count_'+table:count}

    def count(self,request,table,find={}):
        mongodb = mongo[table]
        result = mongodb.count_documents(find)
        return result

    def find_one(self,request,table,find={},select={},skip=0,pipeline=[]):
        listing = self.find(table=table,request=request,find=find,select=select,pipeline=pipeline)
        count = listing['count_'+table]
        if listing['count_'+table] != 0:
            listing = list(listing[table])[0]
        else:
            listing = []
        return {table:listing,'count_'+table:count}

    def update(self,request,table,find={},update={}):
        mongodb = mongo[table]
        # time_str = str((datetime.now()+timedelta(minutes=0)).strftime('%F %T.%f'))
        update['updated_at'] = datetime.now()
        newvalues = { "$set": update } 
        mongodb.update_one(find,newvalues)
        return True

    def update_many(self,request,table,find={},update={}):
        mongodb = mongo[table]
        # time_str = str((datetime.now()+timedelta(minutes=0)).strftime('%F %T.%f'))
        update['updated_at'] = datetime.now()
        mongodb.update_many(find,{ "$set": update })
        return True

    def delete(self,request,table,find):
        mongodb = mongo[table]
        mongodb.update_one(find,{ "$set": {'deleted_at':request.user.id} } )
        return True

    def per_delete(self,request,table,find):
        mongodb = mongo[table]
        # print(find)
        mongodb.delete_one(find)
        return True
