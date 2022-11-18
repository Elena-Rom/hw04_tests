from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Post

User = get_user_model()


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        label = {
            'text': 'Текст записи',
            'group': 'Группа',
        }
        help_text = {
            'text': 'Введите текст записи',
            'group': 'Выберите группу',
        }
