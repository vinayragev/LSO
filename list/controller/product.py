from django.shortcuts import render, HttpResponse, redirect
from .API.function import http_resp,get_input,pre
# from .API.API_product import API_product

class product :
    def add(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_product.add(request)
        # else:
        return render(request,'admin/product/add.html', {'url_product_list':'/admin/product/list'})

    def list(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if request.method=='POST':
        #     return API_product.list(request)
        # else:
        return render(request,'admin/product/list.html', {'edit':'/admin/product/edit','delete':'/admin/product/delete','price':'/admin/product/price/table','price_add':'/admin/product/price/add'})

    def edit(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        if 'product_id' in request.POST:
            product_id = request.POST['product_id']
            # if 'TYPE' in request.POST:
            #     return API_product.edit(request)
            # else:
            return render(request,'admin/product/edit.html', {'product_id':product_id,'list_url':'/admin/product/list','url_product_list':'/admin/product/list'})
        else:
            return redirect('/admin/product/list')

    # def delete(request) :
    #     if not request.user.is_authenticated:
    #         return redirect('/signin')
    #     if request.method =='POST':
    #         if 'product_id' in request.POST:
    #             return API_product.delete(request)
    #         else:
    #             return HttpResponse(404)
    #     else:
    #         return render(request,'admin/product/add.html', {})

