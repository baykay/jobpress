from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('management/', views.ArticleManagementView.as_view(), name='article_management'),
    path('comment_create_view/<slug:slug>', views.CommentsCreateView.as_view(), name='comment_create_view'),
    path('reply_create_view/<slug:slug>', views.ReplyCreateView.as_view(), name='reply_create_view'),
    path('<slug:slug>', views.ArticleDetailView.as_view(), name='article_detail'),
    path('update/<slug:slug>', views.ArticleUpdateView.as_view(), name='article_update'),
    path('delete/<slug:slug>', views.ArticleDeleteView.as_view(), name='article_delete'),
]
