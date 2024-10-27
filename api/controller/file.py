from django.shortcuts import render, HttpResponse, redirect
from .lib import db
from .function import http_resp,pre,input_POST,get_auth_user,handle_uploaded_file
import re
from pymongo import MongoClient
from .label import label
from bson import json_util, ObjectId
from datetime import datetime,timedelta

db = db()

class file() :
    def upload(request):
        file_name = handle_uploaded_file(request=request)
        return http_resp({"success":True,"file_name":file_name})

    def remove(request):

        return http_resp({"success":True})

