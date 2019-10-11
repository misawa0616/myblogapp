from django.shortcuts import render,redirect
from django.http import HttpResponse
from .kerasscript import Post
from .forms import DocumentForm
from .models import Document
import os
import threading

global inunekos3

#def aa():
#    bb = "./testpic/" + request.FILES['document'].name
#    inunekos3 = Post(bb)
#    os.remove(bb)


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            bb = "./testpic/" + request.FILES['document'].name
            global inunekos3
            inunekos3 = Post(bb)
            os.remove(bb)
#            t1 = threading.Thread(target=aa)
#            t1.start()
#            t1.join()
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