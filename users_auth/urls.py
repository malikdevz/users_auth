from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('users_auth/',include('auth_app.urls')),
    path('admin/', admin.site.urls),
]
