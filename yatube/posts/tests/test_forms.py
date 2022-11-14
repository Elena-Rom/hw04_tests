from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .. import models
from ..models import Post, Group

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from yatube.posts import models
        cls.user = models.User.objects.create(username='HASNoName')
        cls.group = models.Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = models.Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostCreateFormTests.user)

    def test_create_post(self):
        """Cоздаётся новая запись в базе данных"""
        post_count = models.Post.objects.count()
        form_data = {
            'text': 'Тестовый текст2',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse(
                'posts:profile',
                kwargs={'username': self.user}
            )
        )
        self.assertEqual(models.Post.objects.count(),
                         post_count + 1, 'Постов не увеличилось на 1')
        self.assertTrue(
            models.Post.objects.filter(
                text='Тестовый текст2',
                author=self.user,
                group=self.group.id,
            ).exists()
        )

    def test_edit_post(self):
        """Редактирование поста в базе данных"""
        post_count = models.Post.objects.count()
        form_data = {
            'text': 'Меняем текст',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(models.Post.objects.count(), post_count)
        self.assertTrue(
            models.Post.objects.filter(
                text='Меняем текст',
                group=self.group.id,
            ).exists()
        )
        self.assertEqual(
            models.Post.objects.get(
                id=self.post.id).text,
            form_data['text'])
