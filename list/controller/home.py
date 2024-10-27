from django.shortcuts import render, HttpResponse, redirect
from .function import http_resp,get_input,pre
# from .API.API_home import API_home

class home :
    def index(request) :
        return render(request,'home/index.html', {})

    def search(request) :
        if 'TYPE' in request.POST:
            # return API_home.search(request)
            pass
        return render(request,'home/shop/search.html', {})

    def shop(request) :
        if 'TYPE' in request.POST:
            # return API_home.shop(request)
            pass
        return render(request,'home/shop/shop.html', {})

    def product(request) :
        if 'TYPE' in request.POST:
            # return API_home.product(request)
            pass
        return render(request,'home/shop/product.html', {})

    def service(request) :
        if 'TYPE' in request.POST:
            # return API_home.service(request)
            pass
        return render(request,'home/shop/service.html', {})

    def geolocation(request) :
        pre(request.GET)

    def seller(request) :
        if 'TYPE' in request.POST:
            # return API_home.seller(request)
            pass
        return render(request,'home/shop/seller.html', {"shop_id":request.GET['seller_id']})

    def profile(request) :
        if 'TYPE' in request.POST:
            # return API_home.profile(request)
            pass
        return render(request,'home/shop/profile.html', {})

    def order(request) :
        if 'TYPE' in request.POST:
            # return API_home.order(request)
            pass
        return render(request,'home/shop/order.html', {})

    def profile_edit(request) :
        if 'TYPE' in request.POST:
            # return API_home.profile_edit(request)
            pass
        return render(request,'home/shop/profile_edit.html', {})

    def order_list(request) :
        if 'TYPE' in request.POST:
            # return API_home.order_list(request)
            pass
        return render(request,'home/shop/order.html', {})

    def order_detail(request) :
        if 'TYPE' in request.POST:
            # return API_home.order_detail(request)
            pass
        return render(request,'home/shop/order_detail.html', {})

    def query_detail(request) :
        if 'TYPE' in request.POST:
            # return API_home.query_detail(request)
            pass
        return render(request,'home/shop/query_detail.html', {})

    def add_staff(request) :
        # return API_home.add_staff(request)
        pass
