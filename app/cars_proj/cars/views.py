from django.shortcuts import render

from . import apiv1


def index(request):
    """
    A homepage of Cars API
    """
    return render(request, 'cars/index.html')
