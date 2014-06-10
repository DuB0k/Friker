from django.shortcuts import render
from models import Photo

def home(request):
    """
    Se ejecuta en / y carga la plantilla photos/templates/photos/index.html
    :param request: objeto request
    :return: objeto response
    """
    photo_list = Photo.objects.all() #cogemos todas las fotos de la BD

    context = {
        'photos' : photo_list
    }

    return render(request, 'photos/index.html', context)