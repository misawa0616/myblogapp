import os
import numpy as np
from keras.models import model_from_json
from PIL import Image
from keras import backend as K
import gc
from memory_profiler import profile

imsize = (32, 32)
keras_model = "./inuneko3/sikibetsu/test.json"
keras_param = "./inuneko3/sikibetsu/test.hdf5"

def load_image(path):
    img = Image.open(path)
    img = img.convert('RGB')
    img = img.resize(imsize)
    # 画像データをnumpy配列の形式に変更
    img = np.asarray(img)
    print(img)
    img = img / 255.0
    return img

@profile
def Post(gazou):
    K.clear_session()
    print(os.getpid())
    # 念のため実行前後でセッションを削除する。
    model = model_from_json(open(keras_model).read())
    model.load_weights(keras_param)
    #model.summary()
    inunekos = ""
    img = load_image(gazou)
    prd = model.predict(np.array([img]))
    K.clear_session()
    # 念のため実行前後でセッションを削除する。
    prelabel = np.argmax(prd, axis=1)
    # 各画像ファイルに猫ならファイル名+0が、犬ならファイル名+1、乗り物ならファイル名+2のラベルが付いている
    if prelabel == 0:
        inunekos = "猫"
    elif prelabel == 1:
        inunekos = "犬"
    elif prelabel == 2:
        inunekos = "乗り物"
    gc.collect()
    print(gc.get_stats())
    return inunekos