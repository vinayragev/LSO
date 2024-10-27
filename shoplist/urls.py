from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('django_admin/', admin.site.urls),
    path('', include('list.urls')),
    path('api/', include('api.urls')),
    path('index.php/', include('list.urls')),
]
