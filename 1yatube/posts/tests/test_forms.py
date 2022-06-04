from django.contrib.auth import get_user_model
from posts.forms import PostForm
from posts.models import Group, Post
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем неавторизованный клиент
        cls.guest_client = Client()
        # Создаем авторизованый клиент
        cls.user = User.objects.create(username='User')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        # Создадим группу в БД
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Описание группы'
        )
        # Создадим пост в БД
        cls.post = Post.objects.create(
            text='Тестовая запись',
            author=cls.user,
            group=cls.group
        )
        cls.form = PostForm()

    def test_create_post(self):
        """Валидная форма создает запись"""
        # Подсчитаем количество записей
        posts_count = Post.objects.count()
        # Подготавливаем данные для передачи в форму
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': PostCreateFormTests.user})
        )
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем, что создалась запись с нашим слагом
        self.assertTrue(
            Post.objects.filter(
                group=PostCreateFormTests.group,
                author=PostCreateFormTests.user,
                text='Тестовый текст'
            ).exists()
        )
