from django.db import models
import keras
import sys, os
import scipy
import numpy as np
from keras.models import model_from_json
from PIL import Image
from keras import backend as K

import json

imsize = (32, 32)
keras_model = "./test.json"
keras_param = "./test.hdf5"

def load_image(path):
    img = Image.open(path)
    img = img.convert('RGB')
    img = img.resize(imsize)
    # 画像データをnumpy配列の形式に変更
    img = np.asarray(img)
    img = img / 255.0
    return img

#def get_file(dir_path):
#    filenames = os.listdir(dir_path)
#    return filenames

# Create your models here.

#class Post(models.Model):
def Post(gazou):
    K.clear_session()
    model = model_from_json(open(keras_model).read())
    model.load_weights(keras_param)
    model.summary()
    inunekos = ""
    img = load_image(gazou)
    #vec = model.predict(np.array([img]), batch_size=1)
    prd = model.predict(np.array([img]))
    K.clear_session()
    prelabel = np.argmax(prd, axis=1)
    # 各画像ファイルに猫ならファイル名+0が、犬ならファイル名+1、乗り物ならファイル名+2のラベルが付いている
    if prelabel == 0:
        inunekos = "猫"
    elif prelabel == 1:
        inunekos = "犬"
    elif prelabel == 2:
        inunekos = "乗り物"

    return inunekos