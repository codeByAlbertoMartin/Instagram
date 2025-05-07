from django.contrib import admin

# Register your models here.
from posts.models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', "caption"]

@admin.register(Comment)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['post','user', 'created_at']
