from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Author, Post, Category, Comment


class PostsAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с постами
    list_display = ['headPost', 'preview', 'typePost', 'author', 'get_cat_post', 'dateCreation']
    # генерируем список имён всех полей для более красивого отображения
    list_filter = ('author', 'typePost', )  # добавляем примитивные фильтры в нашу админку
    fields = ['author', 'typePost', 'headPost', 'textPost', 'ratingPost', 'get_cat_post','dateCreation']
    readonly_fields = ['get_cat_post', 'dateCreation']

    def get_cat_post(self, object):
        cat_name = ""
        for cat in object.categoriesPost.all():
            cat_name += "".join(cat.nameNewsCategories) + " "

        return mark_safe(f"<strong>{cat_name}<br></strong>")

    Post.preview.short_description = "Коротко"
    get_cat_post.short_description = "Категория"


class CommentAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с постами
    list_display = ['commentUser', 'get_author_post', 'get_head_post', 'dateCreation', 'ratingComment', 'textComment']
    # генерируем список имён всех полей для более красивого отображения
    list_filter = ('commentUser', 'ratingComment', )  # добавляем примитивные фильтры в нашу админку
    fields = ['commentUser', 'get_author_post', 'get_head_post', 'dateCreation', 'ratingComment', 'textComment']
    search_fields = ('commentPost__author__userAuthor__username',)
    readonly_fields = ['get_author_post', 'get_head_post', 'dateCreation']

    def get_author_post(self, object):
        author_name = object.commentPost.author.userAuthor
        return mark_safe(f"<i>{author_name}<br></i>")

    def get_head_post(self, object):
        author_name = object.commentPost.headPost
        return mark_safe(f"<i>{author_name}<br></i>")

    get_author_post.short_description = "Автор поста"
    get_head_post.short_description = "Заголовок поста"


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("userAuthor", "ratingAuthor")
    search_fields = ('userAuthor__username',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostsAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
