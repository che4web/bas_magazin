#! -*- coding=utf8 -*-
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        unique=True,
    )

    date = models.DateField(auto_now_add=True,verbose_name="Дата")
    date_publihed = models.DateField(
        verbose_name="Дата публикации ",
        blank=True,null=True
    )
    text = models.TextField(blank=True,verbose_name="Текст")
    CHOISES= (
        ('DR','Черновик'),
        ('PR','Проверка'),
        ('PU','Обубликовано'),
              )
    status = models.CharField(
        max_length=2,
        choices=CHOISES,
        blank=True,
        default='DR',
        verbose_name=u'Статус'
    )
    author = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return '{}. {}. {}'.format(self.id, self.title,self.date)

    def get_absolute_url(self):
        return reverse('article-detail',kwargs={'pk':self.id})
    class Meta:
        verbose_name = u"Статья"
        verbose_name_plural = u"Статьи"

    def save(self,*args,**kwargs):
        ret =  super(Article,self).save(*args,**kwargs)
        print('article %d save',self.id )
        return ret

class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    text = models.TextField(blank=True,verbose_name="Текст")
    date = models.DateField(auto_now_add=True,verbose_name="Дата")


