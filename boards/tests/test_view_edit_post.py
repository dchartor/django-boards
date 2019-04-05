from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from ..models import Board, Post, Topic
from ..views import PostUpdateView


class PostUpdateViewTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='About Django')
        self.username = 'oskolka'
        self.password = '123456'
        user = User.objects.create_user(username=self.username, email='oskolka@mail.com',
                                        password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=user)
        self.post = Post.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
        self.url = reverse('boards:edit', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk
        })


class LoginRequiredPostUpdateViewTests(PostUpdateViewTest):
    def test_rediretion(self):
        login_url = reverse('accounts:login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class UnauthorizedPostUpdateViewTests(PostUpdateViewTest):
    def setUp(self):
        super().setUp()
        username = 'ivan'
        password = '123'
        user = User.objects.create_user(username=username, email='ivan@mail.com',
                                        password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 404)
