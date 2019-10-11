from django.urls import path

from . import views
 

urlpatterns = [
    path('', views.index3, name='index3'),
    path('upload/', views.model_form_upload, name='upload')
]