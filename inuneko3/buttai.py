import matplotlib.pyplot as plt
import matplotlib
import io
import cv2
from keras.applications.imagenet_utils import preprocess_input
from keras.backend.tensorflow_backend import set_session
from keras.preprocessing import image
import numpy as np
from scipy.misc import imread
import tensorflow as tf
from ssd import SSD300
from ssd_utils import BBoxUtility
from django.http import HttpResponse


def Buttai(gazou):
	matplotlib.use('agg')
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
	img = image.load_img(gazou, target_size=(300, 300))
	img = image.img_to_array(img)
	images.append(imread(gazou))
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
	plt.savefig(buf, format='jpg')
	response = HttpResponse(buf.getvalue(), content_type="image/jpg")
	plt.close()
	return response