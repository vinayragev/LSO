from django.shortcuts import render, HttpResponse, redirect
from .API.function import http_resp,get_input,pre
# from .API.API_product_price import API_product_price
from .API.lib import db

db = db()

class product_price :
    def add(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_product_price.add(request)
        # else:
        return render(request,'admin/price/add.html', {'product_id':request.POST.get('product_id',''),'url_price_list':'/admin/product/price/list'})

    def list(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_product_price.list(request)
        # else:
        return render(request,'admin/price/list.html', {'add':'/admin/product/price/add','edit':'/admin/product/price/edit','delete':'/admin/product/price/delete'})

    def table(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_product_price.table(request)
        # else:
        return render(request,'admin/price/table.html', {'edit':'/admin/product/price/edit','delete':'/admin/product/price/delete'})

    def edit(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        if 'price_id' in request.POST:
            # if 'TYPE' in request.POST:
            #     return API_product_price.edit(request)
            # else:
            return render(request,'admin/price/edit.html', {'price_id':request.POST['price_id'],'url_price_list':'/admin/product/price/list'})
        else:
            return redirect('/admin/product/price/list')

    # def delete(request) :
    #     if not request.user.is_authenticated:
    #         return redirect('/signin')
    #     if 'price_id' in request.POST:
    #         return API_product_price.delete(request)
    #     else:
    #         return HttpResponse(404)
