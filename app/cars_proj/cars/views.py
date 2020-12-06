from django.shortcuts import render

from .apiv1 import views as apiv1


def index(request):
    """
    A homepage of Cars API
    """
    return render(request, 'cars/index.html')
