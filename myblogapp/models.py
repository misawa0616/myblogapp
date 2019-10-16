
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import keras
import sys, os
import scipy
import numpy as np
from keras.models import model_from_json
from PIL import Image

import json

class RacchaiUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        return self.create_user(username, password)

class RacchaiUser(AbstractBaseUser):
    username = models.CharField(max_length=128, unique=True)

    USERNAME_FIELD = 'username'

    objects = RacchaiUserManager()

    class Meta:
        db_table = 'racchai_user'
        swappable = 'AUTH_USER_MODEL'