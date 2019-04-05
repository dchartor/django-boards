from django.test import TestCase
from django.urls import resolve
from django.shortcuts import reverse
from django.contrib.auth.forms import UserCreationForm

from ..views import signup
# from ..forms import SignUpForm


# class SignUpTests(TestCase):
#     def setUp(self):
#         url = reverse('accounts:signup')
#         self.response = self.client.get(url)
#
#     def test_signup_satus_code(self):
#         self.assertEqual(self.response.status_code, 200)
#
#     def test_signup_url_resolves_signup_view(self):
#         view = resolve('/signup/')
#         self.assertEqual(view.func, signup)
#
#     def test_signup_csrf_token(self):
#         self.assertContains(self.response, 'csrfmiddlewaretoken')
#
#     def test_contains_form(self):
#         form = self.response.context.get('form')
#         self.assertIsInstance(form, UserCreationForm)
#
#     def test_form_inputs(self):
#         self.assertContains(self.response, '<input', 5)
#         self.assertContains(self.response, 'type="text"', 1)
#         self.assertContains(self.response, 'type="email"', 1)
#         self.assertContains(self.response, 'type="password"', 2)
#
#
# class SuccessfulSignUpTest(TestCase):
#     def setUp(self):
#         url = reverse('accounts:signup')
#         data = {
#             'username': 'john',
#             'email': 'oskolka@mail.com',
#             'password1': '123123d',
#             'password2': '123123d'
#         }
#         self.response = self.client.post(url, data)
#         self.home_url = reverse('boards:home')
#
#     def test_redirection(self):
#         self.assertRedirects(self.response, self.home_url)
