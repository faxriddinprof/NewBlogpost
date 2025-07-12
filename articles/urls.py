from django.urls import path
from .views import (ArticleView, 
                    ArticleDetailView, 
                    CreateArticle,
                    ArticleDeleteview,
                    Myposts,
                )


urlpatterns=[
    path('', ArticleView.as_view(), name='article_list'),
    path('add/', CreateArticle.as_view(), name='add_article'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('delete/<int:pk>/',ArticleDeleteview.as_view(), name='article_delete'),
    path('myposts/', Myposts.as_view(), name='my_posts')
]


