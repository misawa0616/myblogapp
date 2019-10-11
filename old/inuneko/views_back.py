from django.shortcuts import render,redirect
from django.http import HttpResponse
from .a import Post
from .forms import DocumentForm
from .models import Document

def index(request):
#   return HttpResponse("Hello World! このページは投稿のインデックスです。")
    gazou = {{ gazou }}
    inunekos = Post(gazou)
    return render(request, 'inuneko/index.html', {'inunekos': inunekos})
# Create your views here.

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            gazou = form.save()
            return redirect('index', {'gazou' : gazou})
    else:
        form = DocumentForm()
    return render(request, 'inuneko/model_form_upload.html', {
        'form': form
    })