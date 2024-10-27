from django.shortcuts import render, HttpResponse, redirect
from .API.function import http_resp,get_input,pre
# from .API.API_query import API_query

class query :
    def list(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_query.list(request)
        # else:
        return render(request,'admin/query/list.html', {})

    def view(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_query.view(request)
        # else:
        return render(request,'admin/query/view.html', {})

