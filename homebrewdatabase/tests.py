from django.core.urlresolvers import reverse
from django.test import Client, TestCase

class TestViewHomePage(TestCase):

    def test_homepage_returns_correct_template(self):
        url = reverse('index')
        self.client = Client()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homebrewdatabase/index.html')
        self.assertContains(response, 'Hashtagbrews')
