from django.shortcuts import render,redirect
from django.http import HttpResponse
from .kerasscript import Post
from .forms import DocumentForm
from .models import Image
from .models import Inuneko3
import os
import fasteners
from django.contrib.auth.decorators import login_required

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