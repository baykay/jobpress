from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import SearchForm, CommentsForm, ArticleForm, ReplyForm
from blog.models import (
    ArticleModel, ArticleCategoryModel, ArticleTagsModel,
    ArticleCommentsModel, ArticleViews, ReplyModel
)
from utilities.mixins import ContextData


class UserArticleQueryset:
    title = 'Article Management'

    def get_queryset(self):
        queryset = self.model.objects.filter(author=self.request.user)
        search_management = self.request.GET.get('search')
        if search_management:
            split_search = [search_qs for search_qs in search_management.split(' ')]
            for query in split_search:
                queryset = self.model.objects.filter(
                    Q(title__icontains=query) &
                    Q(author=self.request.user)
                ).distinct()
                pluralize = 's' if queryset.count() > 1 else ''
                self.title = f'{queryset.count()} Result{pluralize} found for {search_management}'
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserArticleQueryset, self).get_context_data(**kwargs)
        context['article_lists'] = self.get_queryset()
        context['title'] = self.title
        return context


class ArticleDeleteView(LoginRequiredMixin, UserArticleQueryset, DeleteView):
    title = 'Article Management'
    template_name = 'article_delete.html'
    model = ArticleModel

    def get_context_data(self, **kwargs):
        context = super(ArticleDeleteView, self).get_context_data(**kwargs)
        context['post_to_delete'] = self.get_object()
        return context

    def get_success_url(self):
        from django.urls import reverse
        return reverse('blog:article_management')

    def get_object(self, queryset=None):
        obj_article = get_object_or_404(self.model, author=self.request.user, slug=self.kwargs.get('slug'))
        self.title = f'Delete {obj_article.title}?'
        return obj_article


class ArticleUpdateView(LoginRequiredMixin, UserArticleQueryset, UpdateView):
    title = 'Update Article Management'
    template_name = 'article_management.html'
    model = ArticleModel
    form_class = ArticleForm

    def get_object(self, queryset=None):
        obj_article = get_object_or_404(self.model, author=self.request.user, slug=self.kwargs.get('slug'))
        self.title = f'Update {obj_article.title}'
        return obj_article


class ArticleManagementView(LoginRequiredMixin, UserArticleQueryset, CreateView):
    template_name = 'article_management.html'
    model = ArticleModel
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        messages.success(self.request, f'{form.cleaned_data.get("title")} Posted Successfully')
        return super(ArticleManagementView, self).form_valid(form)


class ArticleListView(ContextData, ListView):
    template_name = 'article_list.html'
    model = ArticleModel
    category_model = ArticleCategoryModel
    tags_model = ArticleTagsModel
    context_object_name = 'article_list'
    ordering = '-date_created'
    title = 'Articles from experienced professionals'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            split_search = [search_qs for search_qs in search.split(' ')]
            for query in split_search:
                queryset = self.model.objects.filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                ).distinct()
                pluralize = 's' if queryset.count() > 1 else ''
                self.title = f'{queryset.count()} Article{pluralize} found for {search}'
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['get_categories'] = self.get_categories()
        context['get_tags'] = self.get_tags()
        context['popular_articles'] = self.get_popular_articles_by_view_count()
        context['form'] = SearchForm(self.request.GET)
        context['article_paginator'] = self.request.GET.get('search')
        return context

    def get_popular_articles_by_view_count(self):
        popular_articles = self.model.objects.exclude(views_count__lt=10).order_by('-views_count')
        return popular_articles

    def get_categories(self):
        all_categories = self.category_model.objects.exclude(articlemodel__isnull=True).distinct()
        return all_categories

    def get_tags(self):
        all_tags = self.tags_model.objects.exclude(articlemodel__isnull=True)
        return all_tags


class ArticleDetailView(ContextData, DetailView):
    template_name = 'article_detail.html'
    model = ArticleModel
    context_object_name = 'article'
    title = 'Article Detail'

    def get_object(self, queryset=None):
        request_user = self.request.user
        obj_article = get_object_or_404(self.model, slug=self.kwargs.get('slug'))
        if request_user.is_authenticated:
            is_viewed = ArticleViews.objects.filter(article=obj_article, user=request_user)
            if is_viewed.exists():
                obj_article.views_count = obj_article.views_count
            else:
                ArticleViews.objects.get_or_create(article=obj_article, user=request_user)
                obj_article.views_count += 1
                obj_article.save()
        else:
            obj_article.views_count += 1
            obj_article.save()
        self.title = f'{obj_article.title}'
        return obj_article

    def get_context_data(self, **kwargs):
        article = get_object_or_404(ArticleModel, slug=self.kwargs.get('slug'))
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentsForm
        context['reply_form'] = ReplyForm
        context['title'] = self.title
        context['comments'] = ArticleCommentsModel.objects.filter(
            article=article, active=True
        ).order_by('-commented_at')
        return context


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = ReplyModel
    fields = ['reply', ]

    def form_valid(self, form):
        comment_id = int(self.request.POST.get('comment_id'))
        comment_obj = get_object_or_404(ArticleCommentsModel, id=comment_id)
        form.instance.user = self.request.user
        form.instance.comment = comment_obj
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        article_slug = get_object_or_404(ArticleModel, slug=self.kwargs['slug'])
        return reverse('blog:article_detail', kwargs={'slug': article_slug.slug})


class CommentsCreateView(LoginRequiredMixin, CreateView):
    model = ArticleCommentsModel
    fields = ['comment', ]

    def form_valid(self, form):
        article = get_object_or_404(ArticleModel, slug=self.kwargs.get('slug'))
        form.instance.commenter = self.request.user
        form.instance.article = article
        form.save()
        return super().form_valid(form)
