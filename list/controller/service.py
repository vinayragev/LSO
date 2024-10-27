from django.shortcuts import render, HttpResponse, redirect
from .API.function import http_resp,get_input,pre
# from .API.API_service import API_service

class service :
    def add(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_service.add(request)
        # else:
        return render(request,'admin/service/add.html', {'url_service_list':'/admin/service/list'})

    def list(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if request.method=='POST':
        #     return API_service.list(request)
        # else:
        return render(request,'admin/service/list.html', {'edit':'/admin/service/edit','delete':'/admin/service/delete','price':'/admin/service/price/table','price_add':'/admin/service/price/add'})

    def edit(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        if 'product_id' in request.POST:
            product_id = request.POST['product_id']
            # if 'TYPE' in request.POST:
            #     return API_service.edit(request)
            # else:
            return render(request,'admin/service/edit.html', {'product_id':product_id,'list_url':'/admin/service/list','url_service_list':'/admin/service/list'})
        else:
            return redirect('/admin/service/list')

    # def delete(request) :
    #     if not request.user.is_authenticated:
    #         return redirect('/signin')
    #     if request.method =='POST':
    #         if 'product_id' in request.POST:
    #             return API_service.delete(request)
    #         else:
    #             return HttpResponse(404)
    #     else:
    #         return render(request,'admin/service/add.html', {})

