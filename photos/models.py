# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError


DEFAULT_LICENSES = (
    ('RIG', 'Copyright'),
    ('LEF', 'Copyleft'),
    ('CC', 'Creative Commons')
)

#LICENSES tiene que coger el LICENSES que haya en el settings y si no hay nada coger
# el default licenses
LICENSES = getattr(settings, 'LICENSES', DEFAULT_LICENSES)

VISIBILITY_PUBLIC = 'PUB'
VISIBILITY_PRIVATE = 'PRI'

VISIBILITY = (
    ('PUB', 'Pública'),
    ('PRI', 'Privada'),
)

BADWORDS = getattr(settings, 'BADWORDS', ())

class Photo(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    url = models.URLField()
    description = models.TextField(blank=True) #opcional
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    license = models.CharField(max_length=3, choices=LICENSES)
    visibility = models.CharField(max_length=3, choices=VISIBILITY)

    def __unicode__(self):
        return self.name

    def clean(self):
        for badword in BADWORDS:
            if badword in self.description:
                raise ValidationError(badword + u" no esta permitido")
