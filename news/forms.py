from django.forms import ModelForm, Textarea, TextInput
from .models import Post
from django.utils.translation import gettext_lazy as gl


# Создаём модельную форму
class PostForm(ModelForm):

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
