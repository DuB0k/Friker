# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from models import Photo, VISIBILITY_PUBLIC
from django.http.response import HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from forms import LoginForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def home(request):
    """
    Se ejecuta en / y carga la plantilla photos/templates/photos/index.html
    :param request: objeto request
    :return: objeto response
    """
    #cogemos todas las fotos de la BD
    photo_list = Photo.objects.filter(visibility=VISIBILITY_PUBLIC).order_by('-created_at')

    context = {
        #Cogemos solo las 3 primeras fotos
        'photos' : photo_list[:3]
    }

    return render(request, 'photos/index.html', context)


def photo_detail(request, pk):
    """
    Muestra el detalle de una foto
    :param request: objeto request
    :param pk: primary key de la foto
    :return: objeto response
    """
    possible_photos = Photo.objects.filter(pk=pk)

    if request.user.is_authenticated():
        possible_photos = possible_photos.filter(Q(owner=request.user) | Q(visibility=VISIBILITY_PUBLIC))
    else:
        possible_photos = possible_photos.filter(visibility=VISIBILITY_PUBLIC)

    if len(possible_photos) == 0:
        return HttpResponseNotFound('No existe la foto seleccionada')
    else:
        context = {
            'photo': possible_photos[0]
        }
        return render(request, 'photos/photo_detail.html', context)


def user_login(request):
    """
    Muestra el formulario de login
    :param request: objeto request
    :return: objeto response
    """
    errors_messages = []

    if request.method == 'POST':

        login_form = LoginForm(request.POST)

        if login_form.is_valid():

            username = login_form.cleaned_data.get('user_username')
            password = login_form.cleaned_data.get('user_password')
            user = authenticate(username=username, password=password)
            if user is None:
                errors_messages.append('Nombre de usuario o contraseña incorrecto')
            else:
                if user.is_active:
                    # crea la sesion de usuario
                    login(request, user)
                    next_url = request.GET.get('next', '/')
                    return redirect(next_url)
                else:
                    errors_messages.append('El usuario no esta activo')

    else:
        login_form = LoginForm()

    context = {
        'form': login_form,
        'errors': errors_messages
    }
    return render(request, 'photos/login.html', context)


def user_logout(request):
    """
    Realiza el logout
    :param request: objeto request
    :return: objeto response
    """
    logout(request)
    return redirect('/')

# Forzamos a que el usuario este autenticado
@login_required()
def user_profile(request):
    """
    Presenta el user profile con sus fotos
    :param request: objeto request
    :return: response objeto response
    """
    context = {
        'photos': request.user.photo_set.all()
    }

    return render(request, 'photos/profile.html',context)