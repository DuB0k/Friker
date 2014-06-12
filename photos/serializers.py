# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from models import Photo
from django.conf import settings

# Permite que BADWORDS se pueda sobreescribir desde el settings.py
# Si no exite el atributo BADWORDS, devuelve la tupla vacia ()
BADWORDS = getattr(settings, 'BADWORDS', ())


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

    def validate(self, attrs):
        existent_users = User.objects.filter(username=attrs.get('username'))
        if len(existent_users) > 0:
            raise serializers.ValidationError(u"Ya existe ese usuario")
        else:
            return attrs # todo ha ido ok


#Este serializer se hace siguiendo un modelo
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo

    def validate_description(self, attrs, source):
        description = attrs.get(source)
        for badword in BADWORDS:
            if badword.lower() in description.lower():
                raise serializers.ValidationError(badword + u" no esta permitido")

        return attrs # todo ha ido bien


class PhotoListSerializer(PhotoSerializer):
    class Meta(PhotoSerializer.Meta):
        fields = ('id', 'owner', 'name')