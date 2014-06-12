# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class UserListAPI(APIView):

    def get(self, request):
        # Recuperamos todos los usuarios del modelo
        users = User.objects.all()
        # Con el parametro many le decimos que le estamos pasasndo muchos usuarios
        # no solo un usuario
        serializer = UserSerializer(users, many=True)
        # El objeto data modifica el formato de los datos de forma transparente
        return Response(serializer.data)
