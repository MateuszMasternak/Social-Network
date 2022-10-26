from django.test import SimpleTestCase
from django.urls import resolve, reverse
from network.views import index, login_view, logout_view, register, create_post, user_page, follow_user, following_page
from network.views import edit_post, likes, show_likes, delete_post


class TestUrls(SimpleTestCase):
    def test_url_resolves(self):
        urls = [
            index, login_view, logout_view, register, create_post, follow_user, following_page, edit_post, likes
        ]
        for url in urls:
            reversed_url = reverse(url)
            self.assertEquals(resolve(reversed_url).func, url)

        urls_with_id = [show_likes, delete_post]
        for url in urls_with_id:
            reversed_url = reverse(url, kwargs={'post_id': 1})
            self.assertEquals(resolve(reversed_url).func, url)

        urls_with_username = [user_page]
        for url in urls_with_username:
            reversed_url = reverse(url, kwargs={'username': 'test'})
            self.assertEquals(resolve(reversed_url).func, url)
