from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from utils.commons import LoginRequiredMixin


class ListView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'list.html')


class POrder(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'place_order.html')