# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from serializers import UserSerializer, PhotoSerializer, PhotoListSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from models import Photo
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from permissions import UserPermissions


class UserListAPI(APIView):
    permission_classes = (UserPermissions,)
    #Una lista de usuarios
    def get(self, request):
        # Recuperamos todos los usuarios del modelo
        users = User.objects.all()
        # Con el parametro many le decimos que le estamos pasando muchos usuarios
        # no solo un usuario
        serializer = UserSerializer(users, many=True)
        # El objeto data modifica el formato de los datos de forma transparente
        return Response(serializer.data)

    def post(self, request):
        # Para crear un usuario
        # Hay que pasar request.DATA en vez de request.POST
        serializer = UserSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Algo ha ido mal
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPI(APIView):
    permission_classes = (UserPermissions,)
    #Un unico usuario
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:
            # Serializamos el user
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:
            serializer = UserSerializer(user, data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                # Algo ha ido mal
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoListAPI(ListCreateAPIView):
    """
    Implementa el listado (GET) y creacion (POST) de fotos
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        # si es un post podemos enviar el modelo con todos los campos
        return PhotoSerializer if self.request.method == "POST" else self.serializer_class


class PhotoDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Implementa el API de listado (GET), update (PUT) y borrado (DELETE) de fotos
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)



