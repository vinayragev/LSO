from bson import json_util, ObjectId
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
# from datetime import datetime,timedelta
from django.utils.crypto import get_random_string
from PIL import Image
from .lib import db

db = db()

def http_resp(data):
    if 'signin_user' in data :
        return data
    return HttpResponse(json_util.dumps(data))

def pre(obj):
    raise Exception(obj)

def input_POST(request):
    post = {'language':'english'}
    for x in request.POST.items():
        if x[1]!='':
            post[x[0]] = x[1]
    return post

def get_input(value):
    if type(value)  in [tuple,list]:
        value = value[0]
    return value

def get_auth_user(request):
    # return User.objects.get(id=1)
    return request.user

def delete_file(path):
    return __file__.split('/controller')[0]+'/static/'+path
    os.remove(__file__.split('/controller')[0]+'/static/'+path)

def handle_uploaded_file(request):
    files = []
    FILES = request.FILES
    for x in FILES:
        file = FILES[x]
        ext = str(file).split('.')[-1]

        path = __file__.split('/controller')[0]+'/static/'
        file_path = 'upload/'+x+'/'+str(request.user.id)+'_'+get_random_string(32)+'.'+ext
        db.insert(request=request,table="image",insert={"file_path":file_path,"name":x,"folder":x})
        dest = open(path+file_path, 'wb')
        if file.multiple_chunks:
            for c in file.chunks():
                dest.write(c)
        else:
            dest.write(file.read())
        dest.close()

        files.append(file_path)
    return file_path




    # image = Image.open('/home/vs/Public/python/shop/list/static/'+file_path)
    # image.save('/home/vs/Public/python/shop/list/static/'+file_path,quality=20,optimize=True)
    # return file_path
