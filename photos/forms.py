# -*- coding: utf-8 -*-
from django import forms
from models import Photo

# lista de tacos http://goo.gl/G2nCu7
#BADWORDS = (u'bocachancla', u'perroflauta', u'prensaestopa', u'pelagatos', u'talentum', u'afinabanjos')


class LoginForm(forms.Form):

    user_username = forms.CharField(label='Nombre de usuario')
    user_password = forms.CharField(label='Password', widget=forms.PasswordInput)


class PhotoForm(forms.ModelForm):
    """
    Pinta un formulario de creacion de una foto
    """
    class Meta:
        model = Photo
        fields = ['name', 'url', 'description', 'license', 'visibility']

"""
    def clean(self):
        cleaned_data = super(PhotoForm, self).clean()
        # Si no tiene la clave description, devuelve una cadena vacia
        description = cleaned_data.get('description', '')
        for badword in BADWORDS:
            if badword in description:
                # Lo de u es porque es unicode
                raise forms.ValidationError(badword + u' no está permitido')

        return cleaned_data # Todo ha ido ok
"""