from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='HASNoName')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostCreateFormTests.user)

    def test_create_post(self):
        """Cоздаётся новая запись в базе данных"""
        post_count = Post.objects.count()
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
        self.assertEqual(Post.objects.count(),
                         post_count + 1, 'Постов не увеличилось на 1')
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                author=self.user,
                group=self.group.id,
            ).exists()
        )

    def test_edit_post(self):
        """Редактирование поста в базе данных"""
        post_count = Post.objects.count()
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
        self.assertEqual(Post.objects.count(), post_count)
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                group=self.group.id,
            ).exists()
        )
        self.assertEqual(
            Post.objects.get(
                id=self.post.id).text,
            form_data['text'])
