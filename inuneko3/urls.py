from django.urls import path

from . import views

urlpatterns = [
    path('index3/', views.index3, name='index3'),
    path('upload/', views.model_form_upload, name='upload'),
    path('image/', views.Image, name='image'),
    path('a/', views.DetailView, name='a'),
    path('upload_buttai/', views.model_form_upload_buttai, name='upload_buttai'),
]