# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from models import Photo

class UserSerializer(serializers.Serializer):
    #Estos campos son los que van a aparecer en el api REST

    #Field es un campo de solo lectura
    id = serializers.Field()

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def restore_object(self, attrs, instance=None):
        """
        Devuelve un objeto user en funcion de attrs
        :param attrs: diccionario con datos
        :param instance:  objeto user a actualizar
        :return: objeto user
        """
        # Si no nos pasan instance, es un User vacio
        if not instance:
            instance = User()

        instance.first_name = attrs.get('first_name')
        instance.last_name = attrs.get('last_name')
        instance.username = attrs.get('username')
        instance.email = attrs.get('email')

        #La password esta almacenada en la bbdd encriptada por django.
        #Para almacenar la pass recibida la encriptamos con la siguiente funcion

        new_password = make_password(attrs.get('password'))
        instance.password = new_password

        return instance


#Este serializer se hace siguiendo un modelo
class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo