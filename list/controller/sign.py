from django.shortcuts import render, HttpResponse, redirect
from .API.function import http_resp,get_input,pre
from .API.API_sign import API_sign
from django.contrib.auth import authenticate, login, logout


class sign :
    def _up(request) :
        if request.user.is_authenticated:
            return redirect('/admin')
        if request.method=='POST':
            return API_sign._up(request)
        elif request.method=='GET':
            return render(request,'preLogin/signup.html', {})

    def _in(request) :
        if request.user.is_authenticated:
            return redirect('/admin')
        if request.method=='POST':
            user = API_sign._in(request)
            if  'signin_user' in user and user['signin_user'] is not None:
                login(request, user['signin_user'])
                return redirect('/admin')
            else:
                return redirect('/signin?error=1')
        elif request.method=='GET':
            return render(request,'preLogin/signin.html', {})

    def _out(request):
        logout(request)
        return redirect('/')
