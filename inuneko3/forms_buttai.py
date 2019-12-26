from django import forms
from .models import Image_buttai
 
class DocumentForm_buttai(forms.ModelForm):
    class Meta:
        model = Image_buttai
        fields = ('image', )