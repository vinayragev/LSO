from django.shortcuts import render, HttpResponse, redirect
from .API.function import http_resp,get_input,pre
# from .API.API_user import API_user

class user :
    def add(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
            # return API_user.add(request)
        # else:
        return render(request,'admin/user/add.html', {'url_user_list':'/admin/user/list'})

    def list(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
            # return API_user.list(request)
        # else:
        return render(request,'admin/user/list.html', {'add':'/admin/user/add','edit':'/admin/user/edit','delete':'/admin/user/delete'})

    def edit(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        if request.method=='POST':
            # if 'TYPE' in request.POST:
                # return API_user.edit(request)
            # else:
            return render(request,'admin/user/edit.html', {'user_id':request.POST['user_id'],'list_url':'/admin/user/list','url_user_list':'/admin/user/list'})
        else:
            return redirect('/admin/user/list')

    # def delete(request) :
    #     if not request.user.is_authenticated:
    #         return redirect('/signin')
    #     # if 'user_id' in request.POST:
    #         # return API_user.delete(request)
    #     # else:
    #     return HttpResponse(404)

