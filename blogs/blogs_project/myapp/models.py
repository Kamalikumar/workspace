# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Todo(models.Model):

    text = models.TextField(max_length=100,blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    user=models.ForeignKey(User,null=True)
    #slug = models.SlugField(editable=True)
    #mydate = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'text',))

    def __str__(self):
        return self.text



