# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status


class UserListAPI(APIView):
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
    #Un unico usuario
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        # Serializamos el user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            # Algo ha ido mal
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

