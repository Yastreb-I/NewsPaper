from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    userAuthor = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора
        rating_post = self.post_set.all().aggregate(sum_rating=Sum("ratingPost"))
        col_post = 0
        col_post += rating_post.get("sum_rating")

        # суммарный рейтинг всех комментариев автора
        rating_comment = self.userAuthor.comment_set.all().aggregate(sum_rating=Sum("ratingComment"))
        col_com = 0
        col_com += rating_comment.get("sum_rating")

        # суммарный рейтинг всех комментариев к статьям автора.
        others_rating = Comment.objects.filter(commentPost__author=self).exclude(
            commentUser=self.userAuthor).aggregate(Sum('ratingComment'))
        col_oth = 0
        if others_rating.get('ratingComment__sum') == type("int"):
            col_oth += others_rating.get('ratingComment__sum')

        # Считаем рейтинг автора и сохраняем его
        self.ratingAuthor = col_com + col_oth + col_post * 3
        self.save()

    def __str__(self):
        return self.userAuthor.username


class Category(models.Model):
    nameNewsCategories = models.CharField(max_length=96, unique=True)

    def __str__(self):
        return self.nameNewsCategories


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NS'
    ARTICLE = 'AR'
    CHOICES_TYPE_POST = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]
    typePost = models.CharField(max_length=2, choices=CHOICES_TYPE_POST, default=NEWS)
    dateCreation = models.DateTimeField(auto_now_add=True)
    categoriesPost = models.ManyToManyField(Category, through="PostCategory")
    headPost = models.CharField(max_length=192)
    textPost = models.TextField()
    ratingPost = models.IntegerField(default=0)

    def __str__(self):
        str_post = f"Автор: {self.author}; \nКатегория: {self.categoriesPost}; \n" \
                   f"Дата создания: {self.dateCreation}; \nЗаголовок: {self.headPost}; \nСодержание: {self.textPost}. "

        return str_post

    # добавим абсолютный путь,
    # чтобы после создания нас перебрасывало на страницу с новостью
    def get_absolute_url(self):
         return f'/news/{self.id}'

    def like(self):
        self.ratingPost += 1
        self.save()

    def dislike(self):
        self.ratingPost -= 1
        self.save()

    # Предварительный просмотр поста
    def preview(self):
        return self.textPost[0:123] + "..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    textComment = models.TextField()
    ratingComment = models.IntegerField(default=0)

    def __str__(self):
        try:
            return self.commentPost.author.userAuthor.username
        except:
            return self.commentUser.username

    def like(self):
        self.ratingComment += 1
        self.save()

    def dislike(self):
        self.ratingComment -= 1
        self.save()

# Create your models here.
