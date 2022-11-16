from django.contrib.auth import get_user_model
from django.test import TestCase
from django.conf import settings
from ..models import Group, Post


User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Духовной жаждою',
        )

    def test_models_post_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        text_post = PostModelTest.post
        self.assertEqual(str(text_post), text_post.text[:15])

    def test_models_group_have_correct_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        title_group = PostModelTest.group
        self.assertEqual(str(title_group), title_group.title)
