from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='HASNoName')
        cls.user2 = User.objects.create(username='ElenaRomm')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description="Тестовое описание",
        )
        cls.templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{cls.group.slug}/',
            'posts/profile.html': f'/profile/{cls.user}/',
            'posts/post_detail.html': f'/posts/{cls.post.id}/',
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client2 = Client()
        self.authorized_client.force_login(URLTests.user)
        self.authorized_client2.force_login(URLTests.user2)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон.
        Для всех пользователей"""
        for template, address in self.templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_url_no_correct(self):
        """Страница /unexisting_page/ не существует"""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_url_uses_correct_template(self):
        """Страница по адресу /create/
        использует шаблон posts/create_post.html."""
        response_authorized = self.authorized_client.get('/create/')
        self.assertTemplateUsed(response_authorized, 'posts/create_post.html')

    def test_anonim_user_redirect_guest(self):
        """Редирект неавторизованного пользователя"""
        pages = {'/create/': '/auth/login/?next=/create/',
                 f'/posts/{self.post.id}/edit/':
                     f'/auth/login/?next=/posts/{self.post.id}/edit/',
                 }
        for page, redirect_url in pages.items():
            self.assertRedirects(self.guest_client.get(page), redirect_url)

    def test_edit_url_uses_correct_template_for_author(self):
        """Страница /posts/<post_id>/edit/
        использует шаблон posts/create_post.html.
        Доступно только автору"""
        with self.subTest(author=self.user):
            response = self.authorized_client.get(
                f'/posts/{self.post.id}/edit/'
            )
            self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_redirect_no_author_post(self):
        """Редирект авторизованного пользователя, но не автора"""
        url_redirect = f'/posts/{self.post.id}/'
        with self.subTest(author=self.user):
            response = self.authorized_client2.get(
                f'/posts/{self.post.id}/edit/'
            )
            self.assertRedirects(response, url_redirect)
