from django import forms
from django.forms import ModelForm
from articleapp.models import Article

class SearcForm(forms.Form):
    title = forms.CharField(label=  'Заголовок', max_length=100)
    date = forms.DateField(label='Дата')

class ArticleModelForm(ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
