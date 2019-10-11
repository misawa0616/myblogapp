from django.shortcuts import render,redirect
from django.http import HttpResponse
from .kerasscript import Post
from .forms import DocumentForm
from .models import Document
import os
import threading
import fasteners

global inunekos3

#def aa():
#    bb = "./testpic/" + request.FILES['document'].name
#    inunekos3 = Post(bb)
#    os.remove(bb)


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            lock = fasteners.InterProcessLock('./lockfile')
            lock.acquire()
            form.save()
            bb = "./testpic/" + request.FILES['document'].name
            global inunekos3
            try:
                inunekos3 = Post(bb)
            except Exception as e:
                inunekos3 = Post(bb)
            try:
                os.remove(bb)
            except Exception as e:
                os.remove(bb)
            lock.release()
            return redirect('index3')
    else:
        form = DocumentForm()
    return render(request, 'inuneko3/model_form_upload.html', {
        'form': form
    })

def index3(request):
#   return HttpResponse("Hello World! このページは投稿のインデックスです。")
    return render(request, 'inuneko3/index3.html', {'inunekos3': inunekos3})
# Create your views here.