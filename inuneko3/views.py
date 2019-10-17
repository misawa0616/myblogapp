from django.shortcuts import render,redirect
from django.http import HttpResponse
from .kerasscript import Post
from .forms_buttai import DocumentForm_buttai
from .forms import DocumentForm
from .models import Image
from .models import Image_buttai
from .models import Inuneko3
import os
import fasteners
from django.contrib.auth.decorators import login_required
from .buttai import Buttai
import matplotlib.pyplot as plt
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
	return render(request, 'inuneko3/index3.html', {'inunekos3': request.session['inunekos3'], 'historys': historys})

def DetailView(request):
	return render(request, 'inuneko3/detail.html')

@login_required()
def model_form_upload_buttai(request):
	if request.method == 'POST':
		form_buttai = DocumentForm_buttai(request.POST, request.FILES)
		if form_buttai.is_valid():
			form_buttai.save()
			cc = "./pics/" + request.FILES['image'].name
			request.session['cc'] = cc
			return render(request, 'inuneko3/detail.html')
	else:
		form_buttai = DocumentForm_buttai()
	return render(request, 'inuneko3/model_form_upload_buttai.html', {'form_buttai': form_buttai})

@login_required()
def Image(request):
	lock = fasteners.InterProcessLock('./lockfile1')
	lock.acquire()
	dd = request.session['cc']
	response = Buttai(dd)
	os.remove(dd)
	lock.release()
	return response