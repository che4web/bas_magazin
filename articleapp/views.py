from django.shortcuts import render
from articleapp.models import Article

from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.exceptions import ValidationError
# Create your views here.
from django.http import JsonResponse
import json

from articleapp.forms import SearcForm,ArticleModelForm

from django.contrib.auth import logout

from django.shortcuts import redirect
from django.views.generic import DetailView,CreateView

def logout_view(request):
    logout(request)
    return render(request,'logout.html',context)

def article_json_search(request):
    q = request.GET.get('q','')
    if q:
        art = Article.objects.filter(title__icontains=q)
    else:
        art=[]
    art_list=[]
    for x in art:
        if x.author:
            author=x.author.username
        else:
            author=''

        art_dict ={
            'title':x.title,
            'text':x.text,
            'author':author,
            'data':x.date,
            'get_absolute_url':x.get_absolute_url()
            }
        art_list.append(art_dict)
    return JsonResponse({'data':art_list})

def article_json(request,pk):
    art = Article.objects.get(id=pk)
    art_dict ={
           'title':art.title,
           'text':art.text
        }
    return JsonResponse(art_dict)

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
    context={'object':art}
    return render(request,'articleapp/article_detail.html',context)

class ArticleDetailView(DetailView):
    model = Article
    def get_context_data(self,*args,**kwargs):
        context = super(ArticleDetailView,self).get_context_data(*args,**kwargs)
        context['text'] ="hello word"
        return context

class MyCreate(object):
    def form_valid(self,form):
        form.instance.author = request.user
        return super(MyCreate,self).from_valid(form)

class ArticleCreateView(CreateView,MyCreate):
    model = Article
    fields = "__all__"



def article_form(request):
    if request.POST:
        form = ArticleModelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect(instance.get_absolute_url())
    else:
        form  = ArticleModelForm()
    context={'form':form}
    context['main_url'] = reverse('article-list')
    return render(request,'article_form.html',context)


