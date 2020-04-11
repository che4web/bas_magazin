from django.shortcuts import render
from articleapp.models import Article

from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.exceptions import ValidationError
# Create your views here.

from django import forms

from django.contrib.auth import logout

from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return render(request,'logout.html',context)

class SearcForm(forms.Form):
    title = forms.CharField(label=  'Заголовок', max_length=100)
    date = forms.DateField(label='Дата')

def index(request):
    user = request.user
    art = Article.objects.all()

    user_list = User.objects.all().annotate(Count('article')).distinct()
    print("---")
    search_form =SearcForm(request.GET)
    context ={'article_list':art}
    if search_form.is_valid():
        art = art.filter(title__icontains=search_form.cleaned_data['title'])
        art = art.filter(date=search_form.cleaned_data['date'])
    context['author_list']=user_list
    context['form']=search_form
    return render(request,'index.html',context)

def article_detail(request,pk):
    art = Article.objects.get(id=pk)
    if art.author == request.user:
        context={'object':art}
    else:
        context={'object': "У вас нет прав"}

    context['main_url'] = reverse('article-list')
    return render(request,'article_detail.html',context)
def article_form(request,pk):
    art = Article.objects.get(id=pk)
    art.save()
    # some code
    print('hello')
    return render(request,'article_detail.html',context)

