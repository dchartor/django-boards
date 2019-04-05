from django.test import TestCase
from django.shortcuts import reverse
from django.urls import resolve
from django.contrib.auth.models import User

from ..views import BoardListView, new_topic_view, TopicListView
from ..models import Board, Topic, Post


class HomeTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('boards:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, BoardListView)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('boards:board', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django Board')

    def test_board_topics_view_success_status_code(self):
        url = reverse('boards:board', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('boards:board', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEqual(view.func.view_class, TopicListView)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('boards:board', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('boards:home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django Board')
        User.objects.create_user(username='John', email='john@mail.com', password='123')
        self.client.login(username='John', password='123')

    def test_new_topic_http(self):
        url = reverse('boards:new_topic', kwargs={'pk': 2})
        self.assertEqual(url, '/boards/2/new/')

    def test_new_topic_view_success_status_code(self):
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('boards:new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEqual(view.func, new_topic_view)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('boards:new_topic', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        boards_topic_url = reverse('boards:board', kwargs={'pk': 1})
        self.assertContains(response, 'href="{0}"'.format(boards_topic_url))

    def test_new_topic_test_csrf(self):
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_validate_data(self):
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Lorem ipsum',
            'message': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())

    def test_new_topic_invalid_data(self):
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)

    def test_new_topic_empty_fields(self):
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
