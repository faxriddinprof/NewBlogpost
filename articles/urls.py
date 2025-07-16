from django.urls import path
from .views import (ArticleView, 
                    ArticleDetailView, 
                    CreateArticle,
                    ArticleDeleteview,
                    ArticleUpdateview,
                    Myposts,
                    like_article,
                    dislike_article,
                    load_more_comments,
                    ajax_search,
                )


urlpatterns=[
    path('', ArticleView.as_view(), name='article_list'),
    path('add/', CreateArticle.as_view(), name='add_article'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('delete/<int:pk>/',ArticleDeleteview.as_view(), name='article_delete'),
    path('update/<int:pk>/', ArticleUpdateview.as_view(), name='article_update' ),
    path('myposts/', Myposts.as_view(), name='my_posts'),
    path('<int:pk>/like/', like_article, name='like_article'),
    path('<int:pk>/dislike/', dislike_article, name='dislike_article'),
    path('articles/<int:pk>/comments/', load_more_comments, name='load_more_comments'),
    path('search/', ajax_search, name='ajax_search'),
    
]


