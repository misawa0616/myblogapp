from django import forms
from .models import Image
from .models import Inuneko3
 
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )