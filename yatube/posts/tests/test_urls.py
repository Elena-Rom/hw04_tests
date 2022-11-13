from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post, User

User = get_user_model()


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='HASNoName')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description="Тестовое описание",
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(URLTests.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон.
        Для всех пользователей"""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{self.group.slug}/',
            'posts/profile.html': f'/profile/{self.user}/',
            'posts/post_detail.html': f'/posts/{self.post.id}/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_url_no_correct(self):
        """Страница /unexisting_page/ не существует"""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_create_url_uses_correct_template(self):
        """Страница по адресу /create/
        использует шаблон posts/create_post.html."""
        response = self.authorized_client.get('/create/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_edit_url_uses_correct_template_for_author(self):
        """Страница /posts/<post_id>/edit/
        использует шаблон posts/create_post.html.
        Доступно только автору"""
        with self.subTest(author=self.user):
            response = self.authorized_client.get(
                f'/posts/{self.post.id}/edit/'
            )
            self.assertTemplateUsed(response, 'posts/create_post.html')
