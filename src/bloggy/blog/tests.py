from django.contrib.auth import get_user
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase

from unittest import skip


class AdminLoginTests(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.email = 'test@example.com'
        User.objects.create_user(self.username, self.email, self.password)

    def test_i_can_visit_the_login_page(self):
        """
        Test that I can visit the login page
        """
        response = self.client.get(reverse('blog:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log In')

    def test_i_can_log_in_to_the_admin(self):
        """
        Test that I can log in using the admin page
        """
        response = self.client.post(
            reverse('blog:do_login'),
            {'username': self.username, 'password': self.password}
        )
        self.assertEqual(response.status_code, 302)
        user = get_user(self.client)
        self.assertFalse(isinstance(user, AnonymousUser))

    def test_i_am_redirected_to_the_login_with_an_error_on_login_fail(self):
        """
        Test that when login fails I am redirected to the login page and that
        the login page displays an error
        """
        response = self.client.post(
            path=reverse('blog:do_login'),
            data={'username': self.username, 'password': 'wrongpassword'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        user = get_user(self.client)
        self.assertTrue(isinstance(user, AnonymousUser))
        self.assertContains(
            response, 'Username and/or password not recognised')

    def test_i_am_redirected_to_the_login_page(self):
        """
        Test that I am redirected to the login page if I visit the admin page
        when I am not logged in
        """
        response = self.client.get(reverse('blog:admin'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url.startswith(reverse('blog:login')),
            "%s does not start with %s" % (response.url, reverse('blog:login'))
        )

    def test_i_am_not_redirected_to_the_login_page_when_i_am_logged_in(self):
        """
        Test that when I am logged in I am not redirected to the login page
        when I visit an admin page
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('blog:admin'))
        self.assertEqual(response.status_code, 200)
