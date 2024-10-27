from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from bson import json_util, ObjectId
from .function import http_resp,pre,input_POST
from .lib import db

db = db()
class sign():
    def _up(request) :
        if request.user.is_authenticated:
            return redirect('/admin')
        if request.method=='POST':
            post = input_POST(request)
            exist = db.find(request=request,table="user",find={"email":post['email']})
            if exist['usercount'] :
                return http_resp({"success":False,'message':"User Already Added"})
            else:
                username = db.insert(request=request,table="user",insert={"name":post['name'],"email":post['email']})
                User.objects.create_user(username.inserted_id, post['email'], post['password'])
                db.update(request=request,table="user",find={"_id":ObjectId(User.objects.get(email=post['email']).username)},update={"user_id":User.objects.get(email=post['email']).id})
            return http_resp({"success":True,'message':"User Added"})

    def _in(request) :
        if request.user.is_authenticated:
            return redirect('/admin')
        if request.method=='POST':
            post = input_POST(request)
            username = db.find_one(request=request,table='user',find={"email":post['email']})
            if username['usercount']:
                user = authenticate(username=username['user']['_id'], password=post['password'])
                response = {"success":True,'signin_user':user,"message":"Sign in successfull"}
                if user is not None:
                    response['user_detail'] = username
                return http_resp(response)
            return http_resp({"success":False,'message':"not match"})

    def _out(request):
        logout(request)
        return redirect('/')
