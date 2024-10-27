from django.shortcuts import render, HttpResponse, redirect
from .API.function import http_resp,get_input,pre
# from .API.API_category import API_category

class category() :
    def add(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     if request.POST["TYPE"]=='SEARCH_PARENT_CATEGORY':
        #         return API_category.search_parent_category(request=request)
        #     return API_category.add(request)
        # else:
        return render(request,'admin/category/add.html', {'url_category_list':'/admin/category/list'})

    def list(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_category.list(request)
        if 'parent_id' in request.POST:
            return render(request,'admin/category/list.html', {'add':'/admin/category/add','edit':'/admin/category/edit','delete':'/admin/category/delete','parent_id':request.POST['parent_id']})
        return render(request,'admin/category/list.html', {'add':'/admin/category/add','edit':'/admin/category/edit','delete':'/admin/category/delete'})

    def edit(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        return render(request,'admin/category/edit.html', {'category_id':request.POST['category_id'],'list_url':'/admin/category/list','url_category_list':'/admin/category/list'})
        # if 'TYPE' not in request.POST:
        # if request.POST["TYPE"]=='SEARCH_PARENT_CATEGORY':
        #     return API_category.search_parent_category(request=request)
        # if request.POST["TYPE"]=='GET_CATEGORY':
        #     return API_category.update(request=request)
        # if request.POST["TYPE"]=='UPDATE_CATEGORY':
        #     return API_category.update(request=request)

    def delete(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if request.method =='POST':
        #     if 'category_id' in request.POST:
        #         return API_category.delete(request)
        #     else:
        #         return HttpResponse(404)
        # else:
            # return render(request,'admin/category/add.html', {})
