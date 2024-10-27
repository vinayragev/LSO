from django.shortcuts import render, HttpResponse, redirect
from .API.function import http_resp,get_input,pre
# from .API.API_service_price import API_service_price
from .API.lib import db

db = db()

class service_price :
    def add(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_service_price.add(request)
        # else:
        return render(request,'admin/service_price/add.html', {'product_id':request.POST.get('product_id',''),'url_price_list':'/admin/service/price/list'})

    def list(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_service_price.list(request)
        # else:
        return render(request,'admin/service_price/list.html', {'add':'/admin/service/price/add','edit':'/admin/service/price/edit','delete':'/admin/service/price/delete'})

    def table(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_service_price.table(request)
        # else:
        return render(request,'admin/service_price/table.html', {'edit':'/admin/service/price/edit','delete':'/admin/service/price/delete'})

    def edit(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        if 'price_id' in request.POST:
            # if 'TYPE' in request.POST:
            #     return API_service_price.edit(request)
            # else:
            return render(request,'admin/service_price/edit.html', {'price_id':request.POST['price_id'],'url_price_list':'/admin/service/price/list'})
        else:
            return redirect('/admin/service/price/list')

    # def delete(request) :
    #     if not request.user.is_authenticated:
    #         return redirect('/signin')
    #     if 'price_id' in request.POST:
    #         return API_service_price.delete(request)
    #     else:
    #         return HttpResponse(404)
