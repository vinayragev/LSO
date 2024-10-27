from django.shortcuts import render, HttpResponse, redirect
from .API.function import http_resp,get_input,pre
# from .API.API_staff import API_staff

class staff :
    def list(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        if 'TYPE' in request.POST:
            return API_staff.list(request)
        else:
            return render(request,'admin/staff/list.html', {})
