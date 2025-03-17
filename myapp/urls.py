from django.urls import path
from .views import index,tmp,yun,python_page

urlpatterns = [
    path('', index, name='index'),
    path('tmp/', tmp, name='tmp'),
    path('yun/', yun, name='yun'),
    path('python_page/', python_page, name='python_page'),
]