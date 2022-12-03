from django.test import TestCase, Client
from django.urls import reverse
from network.views import index, login_view, logout_view, register, create_post, user_page, follow_user, following_page
from network.views import edit_post, likes, count_likes, delete_post
from network.models import User, Post, Follow


class TestViewsGet(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse(index)
        self.login_url = reverse(login_view)
        self.register_url = reverse(register)
        self.user_page_url = reverse(user_page, kwargs={'username': 'test'})

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/index.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/login.html')

    def test_register_GET(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/register.html')

    def test_user_page_GET(self):
        response = self.client.get(self.user_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/user.html')


class TestViewsPost(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', email='test@test.com', password='test123!')

    

