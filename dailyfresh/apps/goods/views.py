from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    """主页视图"""
    def get(self,request):
        return render(request,'index.html')