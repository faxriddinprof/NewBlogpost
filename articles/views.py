from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment, LikeDislike
from .forms import CommentForm, ArticleForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.template.loader import render_to_string

# class ArticleView(ListView):
#     model = Article
#     template_name = 'article_list.html'
#     context_object_name = 'object_list'
#     paginate_by = 10

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         query = self.request.GET.get('q')
#         if query:
#             queryset = queryset.filter(
#                 Q(title__icontains=query) |
#                 Q(summary__icontains=query) |
#                 Q(body__icontains=query) |
#                 Q(author__username__icontains=query)
#             ).distinct()
#         return queryset

class ArticleView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(body__icontains=query) |
                Q(author__username__icontains=query)
            ).distinct()
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('partials/search_results.html', context, request=self.request)
            return JsonResponse({'html': html})
        return super().render_to_response(context, **response_kwargs)


# def ajax_search(request):
#     query = request.GET.get('q', '').strip()

#     if query:
#         articles = Article.objects.filter(
#             Q(title__icontains=query) |
#             Q(summary__icontains=query) |
#             Q(body__icontains=query) |
#             Q(author__username__icontains=query)
#         ).order_by('-date')
#     else:
#         articles = Article.objects.all().order_by('-date')[:10]

#     html = render_to_string(
#         'partials/search_results.html',
#         {'object_list': articles},
#         request=request  # BU MUHIM! context_processor ishlashi uchun
#     )
#     return JsonResponse({'html': html})


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', 'article_list')
        context['form'] = CommentForm()

        post = self.get_object()
        context['comments'] = Comment.objects.filter(post=post).order_by('-created_at')[:5]
        context['total_comments'] = Comment.objects.filter(post=post).count()

        context['like_count'] = post.likes.filter(value=True).count()
        context['dislike_count'] = post.likes.filter(value=False).count()

        if self.request.user.is_authenticated:
            context['user_liked'] = post.likes.filter(user=self.request.user, value=True).exists()
            context['user_disliked'] = post.likes.filter(user=self.request.user, value=False).exists()
        else:
            context['user_liked'] = False
            context['user_disliked'] = False

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            messages.success(request, "💬 Fikr muvaffaqiyatli qo‘shildi.")
            return redirect('article_detail', pk=self.object.pk)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class CreateArticle(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'add_article.html'

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, "✅ Maqola muvaffaqiyatli yaratildi.")
        return HttpResponseRedirect(self.get_success_url())


class ArticleUpdateview(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'summary', 'body', 'photo']
    template_name = 'article_update.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "✏️ Maqola yangilandi.")
        return super().form_valid(form)


class ArticleDeleteview(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, "🗑️ Maqola o‘chirildi.")
        return super().delete(request, *args, **kwargs)


class Myposts(ListView):
    model = Article
    template_name = 'my_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


# ----------------------- Like / Dislike -----------------------------------

def _like_dislike_response_data(article, user):
    return {
        'likes': article.likes.filter(value=True).count(),
        'dislikes': article.likes.filter(value=False).count(),
        'user_liked': article.likes.filter(user=user, value=True).exists(),
        'user_disliked': article.likes.filter(user=user, value=False).exists()
    }


@require_POST
@login_required
def like_article(request, pk):
    article = Article.objects.get(pk=pk)
    obj, created = LikeDislike.objects.get_or_create(post=article, user=request.user, defaults={'value': True})

    if not created:
        if obj.value is True:
            obj.delete()
        else:
            obj.value = True
            obj.save()

    return JsonResponse(_like_dislike_response_data(article, request.user))


@require_POST
@login_required
def dislike_article(request, pk):
    article = Article.objects.get(pk=pk)
    obj, created = LikeDislike.objects.get_or_create(post=article, user=request.user, defaults={'value': False})

    if not created:
        if obj.value is False:
            obj.delete()
        else:
            obj.value = False
            obj.save()

    return JsonResponse(_like_dislike_response_data(article, request.user))


# ---------------------- Load more comments --------------------------------

def load_more_comments(request, pk):
    page = request.GET.get('page', 2)
    article = Article.objects.get(pk=pk)
    comments = article.comments.all().order_by('-created_at')
    paginator = Paginator(comments, 5)
    page_obj = paginator.get_page(page)

    return JsonResponse({
        'comments': [
            {
                'author': c.author.username,
                'content': c.content,
                'created_at': c.created_at.strftime('%d %b %Y, %H:%M')
            } for c in page_obj
        ],
        'has_next': page_obj.has_next()
    })
