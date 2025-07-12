from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
# from django.co
# Create your views here.


class ArticleView(ListView):
    model= Article
    template_name='article_list.html'
    # context_object_name = 'articles'
    # login_url = 'login'

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

class CreateArticle(CreateView):
    model= Article
    fields=['title','summary', 'body', 'photo']
    template_name='add_article.html'

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ArticleDeleteview(DeleteView):
    model = Article
    template_name='article_delete.html'
    success_url = reverse_lazy('article_list')


class Myposts(ListView):
    model=Article
    template_name='my_posts.html'
    context_object_name ='posts'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)