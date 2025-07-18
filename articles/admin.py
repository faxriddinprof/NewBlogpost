from django.contrib import admin
from .models import Article, ArticleImage, Comment, LikeDislike

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')  # 'created_at' emas, 'date'
    list_filter = ('date',)
    search_fields = ('title', 'summary', 'author__username')
    ordering = ('-date',)

@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('article', 'image')
    list_filter = ('article',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'content')
    ordering = ('-created_at',)

@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'value')
    list_filter = ('value',)
    search_fields = ('user__username', 'post__title')
