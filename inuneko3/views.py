from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import os
import fasteners
import io
import threading

from .kensyutsu.buttai import Buttai
from .sikibetsu.kerasscript import Post
from .forms import DocumentForm
from .models import Inuneko3

lock = threading.Lock()
lock1 = fasteners.InterProcessLock('./lockfile1')
#なぜかlock.acquire()の上に置くと、スレッドセーフになれず。

@login_required()
def model_form_upload(request):
	print(threading.get_ident())
	print(os.getpid())
	if request.method == 'POST':
		# POSTメソッドの場合、True
		form = DocumentForm(request.POST, request.FILES)
		# フォームからリクエスト内容を格納する。
		if form.is_valid():
		# フォームに入力された値にエラーがない場合,TRUEとする。
			lock.acquire()
			# 排他ロック
			try:
				inunekos3 = Post(request.FILES['image'])
			except Exception as e:
				inunekos3 = Post(request.FILES['image'])
			# 画像解析処理、重い。1度だけリトライする。
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
		form_buttai = DocumentForm(request.POST, request.FILES)
		# フォームからリクエスト内容を格納する。
		if form_buttai.is_valid():
		# フォームに入力された値にエラーがない場合,TRUEとする。
			global cc
			img_read = request.FILES['image'].read()
			cc = io.BytesIO(img_read)
			# ファイル名をセッションに格納する。
			return render(request, 'inuneko3/detail.html')
	else:
		form_buttai = DocumentForm()
		# POSTメソッド以外の場合、model_form_upload_buttai.htmlへ移動する。
	return render(request, 'inuneko3/model_form_upload_buttai.html', {'form_buttai': form_buttai})

@login_required()
def Image(request):
	# 排他ロック
	lock1.acquire()
	# 排他制御を考慮している。 下記response = Buttai()実行中に、別のプロセスのlogin_required()でccが変更されてしまい、
	# 不整合が発生する恐れがある。
	response = Buttai(cc)
	# 画像解析処理、重い
	lock1.release()
	# 排他ロック
	return response