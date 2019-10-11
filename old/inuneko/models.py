from django.db import models
import keras
import sys, os
import scipy
import numpy as np
from keras.models import model_from_json
from PIL import Image

import json

class Document(models.Model):
    description = models.CharField(max_length=255,blank=True)
    document = models.FileField(upload_to='testpic')
    uploaded_at = models.DateTimeField(auto_now_add=True)