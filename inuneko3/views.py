from django.shortcuts import render,redirect
from django.http import HttpResponse
from .kerasscript import Post
from .forms import DocumentForm
from .buttai import test
from .models import Image
from .models import Inuneko3
import os
import fasteners
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import io
import matplotlib.pyplot as plt
import numpy as np
import django
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt 


@login_required()
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            lock = fasteners.InterProcessLock('./lockfile')
            lock.acquire()
            form.save()
            bb = "./testpic/" + request.FILES['image'].name
            try:
                inunekos3 = Post(bb)
            except Exception as e:
                inunekos3 = Post(bb)
            try:
                os.remove(bb)
            except Exception as e:
                os.remove(bb)
            Username = request.user.username
            Inuneko3(inuneko3=inunekos3 , username=Username).save()
            request.session['inunekos3'] = inunekos3
            lock.release()
            return redirect('index3')
    else:
        form = DocumentForm()
    return render(request, 'inuneko3/model_form_upload.html', { 'form': form})

@login_required()
def index3(request):
    historys = Inuneko3.objects.order_by('-id')[:5]
    html = test()
    return render(request, 'inuneko3/index3.html', {'inunekos3': request.session['inunekos3'], 'historys': historys, 'html':html})

def DetailView(request):
    return render(request, 'inuneko3/detail.html')

'''
# グラフ作成
def image(request):
    # prepare for data 
    datas = [20, 30, 10]
    labels = ['Wine', 'Sake', 'Beer']
    colors = ['yellow', 'red', 'green']
    # create figure
    fig = plt.figure(1,figsize=(4,4))
    ax = fig.add_subplot(111) 
    ax.axis("equal")
    pie = ax.pie(datas, #データ
                 startangle=90, #円グラフ開始軸を指定
                 labels=labels, #ラベル
                 autopct="%1.1f%%",#パーセント表示
                 colors=colors, #色指定
                 counterclock=False, #逆時計回り
                 )
    # Return
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/jpg')
    canvas.print_jpg(response)
    return response
'''

def image(request):
    import cv2
    import keras
    from keras.applications.imagenet_utils import preprocess_input
    from keras.backend.tensorflow_backend import set_session
    from keras.models import Model
    from keras.preprocessing import image
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.misc import imread
    import tensorflow as tf
    from ssd import SSD300
    from ssd_utils import BBoxUtility
    from PIL import Image

    plt.rcParams['figure.figsize'] = (10, 10)
    plt.rcParams['image.interpolation'] = 'nearest'
    np.set_printoptions(suppress=True)
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.45
    set_session(tf.Session(config=config))
    voc_classes = ['Aeroplane', 'Bicycle', 'Bird', 'Boat', 'Bottle',
               'Bus', 'Car', 'Cat', 'Chair', 'Cow', 'Diningtable',
               'Dog', 'Horse','Motorbike', 'Person', 'Pottedplant',
               'Sheep', 'Sofa', 'Train', 'Tvmonitor']
    NUM_CLASSES = len(voc_classes) + 1
    # 独自に学習したモデルを使用する場合、フォルダcheckpointsのモデルを選択してください。
    input_shape=(300, 300, 3)
    model = SSD300(input_shape, num_classes=NUM_CLASSES)
    model.load_weights('weights_SSD300.hdf5', by_name=True)
    bbox_util = BBoxUtility(NUM_CLASSES)
    inputs = []
    images = []
    img_path = './pics/fish-bike.jpg'
    img = image.load_img(img_path, target_size=(300, 300))
    img = image.img_to_array(img)
    images.append(imread(img_path))
    inputs.append(img.copy())
    inputs = preprocess_input(np.array(inputs))
    preds = model.predict(inputs, batch_size=1, verbose=1)
    results = bbox_util.detection_out(preds)
    a = model.predict(inputs, batch_size=1)
    b = bbox_util.detection_out(preds)
    for i, img in enumerate(images):
        # Parse the outputs.
        det_label = results[i][:, 0]
        det_conf = results[i][:, 1]
        det_xmin = results[i][:, 2]
        det_ymin = results[i][:, 3]
        det_xmax = results[i][:, 4]
        det_ymax = results[i][:, 5]

        # Get detections with confidence higher than 0.6.
        top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.6]

        top_conf = det_conf[top_indices]
        top_label_indices = det_label[top_indices].tolist()
        top_xmin = det_xmin[top_indices]
        top_ymin = det_ymin[top_indices]
        top_xmax = det_xmax[top_indices]
        top_ymax = det_ymax[top_indices]

        colors = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()

        plt.imshow(img / 255.)
        currentAxis = plt.gca()

        for i in range(top_conf.shape[0]):
            xmin = int(round(top_xmin[i] * img.shape[1]))
            ymin = int(round(top_ymin[i] * img.shape[0]))
            xmax = int(round(top_xmax[i] * img.shape[1]))
            ymax = int(round(top_ymax[i] * img.shape[0]))
            score = top_conf[i]
            label = int(top_label_indices[i])
            label_name = voc_classes[label - 1]
            display_txt = '{:0.2f}, {}'.format(score, label_name)
            coords = (xmin, ymin), xmax-xmin+1, ymax-ymin+1
            color = colors[label]
            currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
            currentAxis.text(xmin, ymin, display_txt, bbox={'facecolor':color, 'alpha':0.5})
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    response = HttpResponse(buf.getvalue(), content_type="image/jpg")
    return response