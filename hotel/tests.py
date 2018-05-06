from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class TestLoggedUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', 'user@test.net', 'secret')
        self.user.save()
        self.client.login(username='test_user', password='secret')

    def tearDown(self):
        self.user.delete()

    def test_logged_user_get_homepage(self):
        response = self.client.get(reverse('hotel:homepage'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logged_user_get_listing(self):
        response = self.client.get(reverse('hotel:listing'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logged_user_get_listing_without_sorting(self):
        response = self.client.get(reverse('hotel:listing'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<h3 class="h4 panel-title">Sort</h3>')


class TestAdminUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', 'user@test.net', 'secret')
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username='test_user', password='secret')

    def tearDown(self):
        self.user.delete()

    def test_admin_user_get_homepage(self):
        response = self.client.get(reverse('hotel:homepage'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_admin_user_get_listing(self):
        response = self.client.get(reverse('hotel:listing'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_admin_user_get_listing_with_sorting(self):
        response = self.client.get(reverse('hotel:listing'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h3 class="h4 panel-title">Sort</h3>')


class TestAPIForUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', 'user@test.net', 'secret')
        self.user.save()
        self.client.login(username='test_user', password='secret')

    def tearDown(self):
        self.user.delete()

    def test_success_response(self):
        response = self.client.get(reverse('hotel:api_hotel'), follow=True)
        self.assertEqual(response.status_code, 200)


class TestAPIForAdminUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', 'user@test.net', 'secret')
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username='test_user', password='secret')

    def tearDown(self):
        self.user.delete()

    def test_success_response(self):
        response = self.client.get(reverse('hotel:api_hotel'), follow=True)
        self.assertEqual(response.status_code, 200)
