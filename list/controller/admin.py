from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from .API.lib import db
from .API.function import http_resp,get_input,pre
import json
# from .API.API_admin import API_admin

db = db()

class admin :
    def dashboard(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        if 'TYPE' in request.POST:
            return API_admin.dashboard(request)
        user_detail = db.find_one(request=request,table="user",select={"name":1,"email":1,"_id":0},find={"user_id":request.user.id})['user']
        return render(request,'admin/dashboard.html',{"user_detail":json.dumps(user_detail)})
        return render(request,'pages/profile.html',{})
        return render(request,'pages/forget-password.html',{})
        return render(request,'pages/settings.html',{})
        return render(request,'pages/tables.html',{})
        return render(request,'pages/sign-up.html',{})
        return render(request,'pages/sign-in.html',{})
        return render(request,'pages/pricing.html',{})
        return render(request,'pages/layout.html',{})
        return render(request,'pages/billing.html',{})
        return render(request,'pages/404-error.html',{})

    def profile(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        else:
            return render(request,'admin/profile.html',{})

    def profile_edit(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        if 'TYPE' in request.POST:
            return API_admin.profile_edit(request)
        return render(request,'admin/profile_edit.html',{})
