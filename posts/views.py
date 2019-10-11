from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

def index1(request):
#	return HttpResponse("Hello World! このページは投稿のインデックスです。")
	posts = Post.objects.order_by('-published')
	return render(request, 'posts/index1.html', {'posts': posts})
# Create your views here.
