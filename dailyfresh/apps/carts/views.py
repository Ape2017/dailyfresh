from django.shortcuts import render

from django.views.generic import View

from utils.commons import LoginRequiredMixin


class CartView(View):
    def get(self, request):
        return render(request, 'cart.html')