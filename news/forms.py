from django.forms import ModelForm, Textarea, TextInput, ChoiceField
from .models import Post, Author
from django.utils.translation import gettext_lazy as gl
from datetime import datetime


# Создаём модельную форму
class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = [# 'author',
                  'typePost', 'headPost', 'textPost', 'categoriesPost']
        labels = {
            # 'author': gl("Автор"),
            'typePost':  gl("Новость/Статья"),
            'headPost': gl("Заголовок статьи"),
            'textPost': gl("Текст статьи"),
            'categoriesPost': gl("Категория"),
        }
        widgets = {
            "textPost": Textarea(attrs={"style": "width: 60vw; height: 60vh", "required": "true"}),
            'headPost': TextInput(attrs={"style": "width: 60vw;", "required": "true"}),

        }


