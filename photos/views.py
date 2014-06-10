from django.shortcuts import render
from django.http.response import HttpResponse

def home(request):
    """
    Se ejecuta en /helloworld
    :param request: objeto request
    :return: objeto response

    """
    html = '<strong>Hola mundo</strong>'
    return HttpResponse(html)