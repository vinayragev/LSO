from django.shortcuts import render, HttpResponse, redirect
from .API.function import http_resp,get_input,pre
# from .API.API_order import API_order

class order :
    def view(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_order.view(request)
        # else:
        return render(request,'admin/order/view.html', {})

    def list(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_order.list(request)
        # else:
        return render(request,'admin/order/list.html', {"view":"/admin/order/view"})

    def pending(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_order.pending(request)
        # else:
        return render(request,'admin/order/list.html', {"view":"/admin/order/view"})
