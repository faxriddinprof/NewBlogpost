from django.contrib import admin
from .models import Article, Comment, LikeDislike

admin.site.register(Article)
admin.site.register(LikeDislike)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)

admin.site.register(Comment, CommentAdmin)
