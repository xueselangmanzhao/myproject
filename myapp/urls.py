from django.urls import path
from .views import index,tmp,yun,python_page,register, user_login, password_reset, phone_login

urlpatterns = [
    path('', index, name='index'),
    path('tmp/', tmp, name='tmp'),
    path('yun/', yun, name='yun'),
    path('python_page/', python_page, name='python_page'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('password_reset/', password_reset, name='password_reset'),
    path('phone_login/', phone_login, name='phone_login'),
]