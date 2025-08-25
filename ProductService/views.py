from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class HomePageView(View):
    template_name = 'product_service/home.html'

    def get(self, request):
        return render(request, self.template_name)