from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from ckeditor.fields import RichTextField

# Create your models here.

User = get_user_model()

class Article(models.Model):
    title=models.CharField(max_length=150)
    summary=models.CharField(max_length=250, blank=True)
    body=RichTextField()
    date=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True

    )
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])


# for images  
class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='article_images/')

    def __str__(self):
        return f"Image for {self.article.title}"







class Comment(models.Model):
    post = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:30]

class LikeDislike(models.Model):
    post = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.BooleanField()  # True = like, False = dislike
    
    class Meta:
        unique_together = ('post', 'user')  # Har bir user faqat bitta like/dislike qila oladi

    def __str__(self):
        return f"{self.user.username} - {'Like' if self.value else 'Dislike'}"
