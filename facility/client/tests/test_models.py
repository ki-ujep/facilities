from django.test import TestCase, SimpleTestCase
from django.urls import reverse


class AboutPageTests(SimpleTestCase):
    """
    def test_url_exists_at_correct_location(self):
        response = self.client.get("about")
        self.assertEqual(response, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("about"))
        self.assertTemplateUsed(response, "about.html")

    def test_template_content(self):
        response = self.client.get(reverse("about"))
        self.assertContains(response, "<h2>About</h2>")
        self.assertNotContains(response, "Under construction ...")
    """
    pass
