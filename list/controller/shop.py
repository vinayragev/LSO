from django.shortcuts import render, HttpResponse, redirect
from .API.function import http_resp,get_input,pre
# from .API.API_shop import API_shop

class shop :
    def add(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if request.method == 'POST':
        #     return API_shop.add(request)
        # else:
        return render(request,'admin/shop/add.html', {'dayNames': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday'],'url_shop_list':'/admin/shop/list'})

    def list(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if request.method=='POST':
        #     return API_shop.list(request)
        # else:
        return render(request,'admin/shop/list.html', {'price':'/admin/product/price/list','edit':'/admin/shop/edit','delete':'/admin/shop/delete','product':'/admin/shop/product/list'})

    def product_list(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        if 'shop_id' in request.POST:
            # if 'TYPE' in request.POST and request.POST['TYPE']=='GET_PRODUCT':
            #     product_list = API_shop.product_list(request)['listing']
            #     return http_resp({'success':True,'product_list':product_list})
            return render(request,'admin/shop/product/list.html', {'shop_id':request.POST['shop_id'],'url_shop_list':'/admin/shop/list'})
        else:
            return redirect('/admin/shop/list')

    def edit(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        if 'shop_id' in request.POST:
            shop_id = request.POST['shop_id']
            # if 'TYPE' in request.POST:
            #     return API_shop.edit(request)
            return render(request,'admin/shop/edit.html', {'shop_id':shop_id,'dayNames': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']})
        else:
            return redirect('/admin/shop/list')

    # def delete(request) :
    #     if not request.user.is_authenticated:
    #         return redirect('/signin')
    #     if request.method =='POST':
    #         if 'shop_id' in request.POST:
    #             return API_shop.delete(request)
    #         else:
    #             return HttpResponse(404)
    #     else:
    #         return render(request,'admin/shop/add.html', {})

