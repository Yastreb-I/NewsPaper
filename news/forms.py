from django.forms import ModelForm, Textarea, TextInput
from .models import Post
from django.utils.translation import gettext_lazy as gl


# Создаём модельную форму
class PostForm(ModelForm):
    # categoriesPost = Post.categoriesPost.nameNewsCategories
    # categoriesPost = Post.categoriesPost.category.nameNewsCategories

    class Meta:
        model = Post
        fields = ['author', 'typePost', 'headPost', 'textPost', 'categoriesPost']
        labels = {
            'author': gl("Автор"),
            'typePost':  gl("Новость/Статья"),
            'headPost': gl("Заголовок статьи"),
            'textPost': gl("Текст статьи"),
            'categoriesPost': gl("Категория"),
        }
        widgets = {
            "textPost": Textarea(attrs={"style": "width: 60vw; height: 60vh"}),
            'headPost': TextInput(attrs={"style": "width: 60vw; "}),

        }

#
# categories = Category.objects.filter(postcategory__postThrough=instance)   # находим категории данного поста
# subscribers_mail = []
# for category in categories:   # перебираем категории
#     for sub in category.subscribers.values('email'):    # перебираем email подписчиков
#         subscribers_mail.append(sub['email'])   # на выходе получаем список адресов для рассылки


