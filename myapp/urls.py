from django.urls import path
from .views import index,tmp,yun

urlpatterns = [
    path('', index, name='index'),
    path('tmp/', tmp, name='tmp'),
    path('yun/', yun, name='yun'),
]