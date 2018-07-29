from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('', include('rides.urls')),
    path('admin/', admin.site.urls),
    url('logout', auth_views.logout, {'next_page': 'login'}, name='logout'),
]
