from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def tmp(request):
    return render(request, 'tmp.html')

def yun(request):
    return render(request, 'yun.html')