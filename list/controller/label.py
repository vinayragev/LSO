from django.shortcuts import render, HttpResponse, redirect
from .API.function import http_resp,get_input,pre
# from .API.API_label import API_label
from .API.lib import db

db = db()

class label :
    def add(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_label.add(request)
        # else:
        return render(request,'admin/label/add.html', {'url_label_list':'/admin/label/list'})

    def list(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        # if 'TYPE' in request.POST:
        #     return API_label.list(request)
        # else:
        return render(request,'admin/label/list.html', {'add':'/admin/label/add','edit':'/admin/label/edit','delete':'/admin/label/delete'})

    def edit(request) :
        if not request.user.is_authenticated:
            return redirect('/signin')
        if request.method=='POST':
            # if 'TYPE' in request.POST:
            #     return API_label.edit(request)
            # else:
            return render(request,'admin/label/edit.html', {'label_id':request.POST['label_id'],'list_url':'/admin/label/list','url_label_list':'/admin/label/list'})
        else:
            return redirect('/admin/label/list')

    # def delete(request) :
    #     if not request.user.is_authenticated:
    #         return redirect('/signin')
    #     if 'label_id' in request.POST:
    #         return API_label.delete(request)
    #     else:
    #         return HttpResponse(404)
