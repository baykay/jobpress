from django.contrib import admin

from blog.models import ArticleModel, ArticleCategoryModel, ArticleTagsModel


class ArticleModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(ArticleModel, ArticleModelAdmin)
admin.site.register(ArticleCategoryModel)
admin.site.register(ArticleTagsModel)
