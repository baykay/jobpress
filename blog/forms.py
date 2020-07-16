from django import forms

from blog.models import ArticleCommentsModel, ArticleModel, ArticleTagsModel, ArticleCategoryModel


class SearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Search Article'}
    )
                             )


class ReplyForm(forms.ModelForm):
    reply = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Reply', 'class': 'form-control'}
        ),
        required=True,
        label=''
    )

    class Meta:
        model = ArticleCommentsModel
        fields = ['reply']


class CommentsForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Comment', 'class': 'form-control'}
        ),
        required=True,
        label=''
    )

    class Meta:
        model = ArticleCommentsModel
        fields = ['comment']


class ArticleForm(forms.ModelForm):
    featured_image = forms.ImageField(widget=forms.FileInput(attrs={
        'id': 'featured_image',
        'name': 'featured_image',
        'type': 'file'
    }), required=False)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Article Content', 'class': 'form-control'}),
        required=True,
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Article Title', 'class': 'form-control'}),
        required=True,
    )
    tags = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={
            'class': 'chosen-select Skills',
            'data-placeholder': 'Select Tags...',
            'style': 'display: none;'
        }), required=False,
        queryset=ArticleTagsModel.objects.all(),
    )
    category = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Article\'s Category',
        queryset=ArticleCategoryModel.objects.all(),
    )

    class Meta:
        model = ArticleModel
        fields = ['title', 'tags', 'category', 'content', 'featured_image']
