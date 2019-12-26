from django import forms

class DocumentForm(forms.Form):
    image = forms.FileField()

# model(データベース連携) https://eiry.bitbucket.io/tutorials/guest_board/models.html
# form(データベース非連携) https://noumenon-th.net/programming/2019/10/28/django-forms/