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
		# POSTメソッドの場合、True
		form = DocumentForm(request.POST, request.FILES)
		# フォームからリクエスト内容を格納する。
		if form.is_valid():
		# フォームに入力された値にエラーがない場合,TRUEとする。
			lock = fasteners.InterProcessLock('./lockfile')
			lock.acquire()
			# 排他ロック
			form.save()
			# リクエストに含まれる内容をdatabaseに保存する。同時に画像が保存される。
			bb = "./testpic/" + request.FILES['image'].name
			# 送信された画像のパスを変数に代入する。
			try:
				inunekos3 = Post(bb)
			except Exception as e:
				inunekos3 = Post(bb)
			# 画像解析処理、重い。1度だけリトライする。
			try:
				os.remove(bb)
			except Exception as e:
				os.remove(bb)
			#uploadされた画像を削除している。1度だけリトライする。
			Username = request.user.username
			# 実行ユーザ-を変数に代入する。
			Inuneko3(inuneko3=inunekos3 , username=Username).save()
			# 判定結果と実行ユーザーをdatabaseに保存する。
			request.session['inunekos3'] = inunekos3
			# 判定結果をセッションに格納する。
			lock.release()
			# 排他ロック
			return redirect('index3')
	else:
		form = DocumentForm()
		# POSTメソッド以外の場合、model_form_upload.htmlへ移動する。
	return render(request, 'inuneko3/model_form_upload.html', { 'form': form})

@login_required()
def index3(request):
	historys = Inuneko3.objects.order_by('-id')[:5]
	# inuneko3 databaseから履歴を出力する。
	return render(request, 'inuneko3/index3.html', {'inunekos3': request.session['inunekos3'], 'historys': historys})

def DetailView(request):
	return render(request, 'inuneko3/detail.html')

@login_required()
def model_form_upload_buttai(request):
	if request.method == 'POST':
		# POSTメソッドの場合、True
		form_buttai = DocumentForm_buttai(request.POST, request.FILES)
		# フォームからリクエスト内容を格納する。
		if form_buttai.is_valid():
		# フォームに入力された値にエラーがない場合,TRUEとする。
			form_buttai.save()
			# リクエストに含まれる内容をdatabaseに保存する。同時に画像が保存される。
			cc = "./pics/" + request.FILES['image'].name
			# 送信された画像のパスを変数に代入する。
			request.session['cc'] = cc
			# ファイル名をセッションに格納する。
			return render(request, 'inuneko3/detail.html')
	else:
		form_buttai = DocumentForm_buttai()
		# POSTメソッド以外の場合、model_form_upload_buttai.htmlへ移動する。
	return render(request, 'inuneko3/model_form_upload_buttai.html', {'form_buttai': form_buttai})

@login_required()
def Image(request):
	lock = fasteners.InterProcessLock('./lockfile1')
	lock.acquire()
	# 排他ロック
	dd = request.session['cc']
	# 排他制御を考慮している。 下記response = Buttai()実行中に、別のプロセスのlogin_required()でccが変更されてしまい、
	# 変更後画像が、os.remove()で削除されてしまう恐れがあるため不整合が発生する恐れがある。
	# cc→ddに変更している。
	response = Buttai(dd)
	# 画像解析処理、重い
	os.remove(dd)
	#uploadされた画像を削除している。
	lock.release()
	# 排他ロック
	return response