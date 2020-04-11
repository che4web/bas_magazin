from django.contrib import admin
from articleapp.models import Article,Comment
# Register your models here.
@admin.register(Article)
class ArcticleArdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class ArcticleArdmin(admin.ModelAdmin):
    pass
