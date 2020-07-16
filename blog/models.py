from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from company.models import CompanyProfile
from freelancer.models import FreelancerProfile
from utilities.slug_generator import slug_generator

User = get_user_model()


class ArticleCategoryModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ArticleTagsModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ArticleModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(ArticleCategoryModel, on_delete=models.DO_NOTHING, null=True, blank=True)
    tags = models.ManyToManyField(ArticleTagsModel, blank=True)
    views_count = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255)
    featured_image = models.ImageField(upload_to='Articles featured images', default='article_featured_image.jpg')

    def authoring_date(self):
        author = self.author
        authoring_date = self.__class__.objects.filter(author=author).first()
        author_authoring_date = authoring_date.date_created
        return author_authoring_date

    def get_author_avatar(self):
        author_avatar = None
        if self.author.is_company:
            author = CompanyProfile.objects.get(user=self.author)
            author_avatar = author.logo
        elif self.author.is_freelancer:
            author = FreelancerProfile.objects.get(user=self.author)
            author_avatar = author.avatar
        return author_avatar

    def get_author_bio(self):
        author_bio = None
        if self.author.is_company:
            author = CompanyProfile.objects.get(user=self.author)
            author_bio = author.description
        elif self.author.is_freelancer:
            author = FreelancerProfile.objects.get(user=self.author)
            author_bio = author.description
        return author_bio

    def get_author_profile(self):
        author_profile = None
        if self.author.is_company:
            author_profile = reverse('company:company_detail', kwargs={'username': self.author.username})
        elif self.author.is_freelancer:
            author_profile = reverse('freelancer:detail', kwargs={'username': self.author.username})
        return author_profile

    def get_author_email(self):
        return self.author.email

    def get_author(self):
        author = None
        if self.author.is_company:
            author = self.author.company_profile.name
        elif self.author.is_freelancer:
            author = self.author.freelancer_profile.get_full_name
        return author

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.title, instance.slug)
        if instance.slug in ['delete', 'update', 'create']:
            instance.slug = slug_generator(instance, instance.title, instance.slug)


pre_save.connect(slug_save, sender=ArticleModel)


class ArticleViews(models.Model):
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE, related_name='viewed_article')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewed_user')


class ArticleCommentsModel(models.Model):
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE, related_name='comment_article')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    comment = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    # reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return 'Comment by {}'.format(self.get_commenter())

    def get_commenter(self):
        commenter = None
        if self.commenter.is_company:
            commenter = self.commenter.company_profile.name
        elif self.commenter.is_freelancer:
            commenter = self.commenter.freelancer_profile.get_full_name
        return commenter

    def get_commenter_profile_url(self):
        if self.commenter.is_company:
            return reverse('company:company_detail', kwargs={'username': self.commenter.username})
        elif self.commenter.is_freelancer:
            return reverse('freelancer:detail', kwargs={'username': self.commenter.username})

    def get_commenter_avatar(self):
        commenter_avatar = None
        if self.commenter.is_company:
            commenter = CompanyProfile.objects.get(user=self.commenter)
            commenter_avatar = commenter.logo
        elif self.commenter.is_freelancer:
            commenter = FreelancerProfile.objects.get(user=self.commenter)
            commenter_avatar = commenter.avatar
        return commenter_avatar

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.article.slug})


class ReplyModel(models.Model):
    comment = models.ForeignKey(ArticleCommentsModel, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_user')
    reply = models.TextField()
    date_replied = models.DateTimeField(default=timezone.now)

    def get_replier_profile_url(self):
        if self.user.is_company:
            return reverse('company:company_detail', kwargs={'username': self.user.username})
        elif self.user.is_freelancer:
            return reverse('freelancer:detail', kwargs={'username': self.user.username})

    def get_replier(self):
        replier = None
        if self.user.is_company:
            replier = self.user.company_profile.name
        elif self.user.is_freelancer:
            replier = self.user.freelancer_profile.get_full_name
        return replier

    def get_replier_avatar(self):
        replier_avatar = None
        if self.user.is_company:
            reply_user = CompanyProfile.objects.get(user=self.user)
            replier_avatar = reply_user.logo
        elif self.user.is_freelancer:
            reply_user = FreelancerProfile.objects.get(user=self.user)
            replier_avatar = reply_user.avatar
        return replier_avatar
