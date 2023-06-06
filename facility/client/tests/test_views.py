from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse


class AboutPageTests(SimpleTestCase):
    def __init__(self, *args, **kwargs):
        self.client = Client()
        super(AboutPageTests, self).__init__(*args, **kwargs)

    """
    def test_url_exists_at_correct_location(self):
        response = self.client.get("about")
        self.assertEqual(response, 200)
    """
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


class HelpPageTests(SimpleTestCase):
    def __init__(self, *args, **kwargs):
        self.client = Client()
        super(HelpPageTests, self).__init__(*args, **kwargs)

    """
    def test_url_exists_at_correct_location(self):
        response = self.client.get(reverse("help"))
        self.assertEqual(response.status_code, 200)
    """
    def test_url_available_by_name(self):
        response = self.client.get(reverse("help"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("help"))
        self.assertTemplateUsed(response, "help.html")

    def test_template_content(self):
        response = self.client.get(reverse("help"))
        self.assertContains(response, "<h2>Help</h2>")
        self.assertNotContains(response, "Under construction ...")


class HomePageTests(TestCase):
    def __init__(self, *args, **kwargs):
        self.client = Client()
        super(HomePageTests, self).__init__(*args, **kwargs)

    """
    def test_url_exists_at_correct_location(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
    """
    def test_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

    def test_template_content(self):
        response = self.client.get(reverse("home"))
        #self.assertContains(response, "<h2>Facilities</h2>")
        self.assertNotContains(response, "Under construction ...")


class ContactsPageTests(TestCase):
    def __init__(self, *args, **kwargs):
        self.client = Client()
        super(ContactsPageTests, self).__init__(*args, **kwargs)

    """
    def test_url_exists_at_correct_location(self):
        response = self.client.get(reverse("contacts"))
        self.assertEqual(response.status_code, 200)
    """
    # django.urls.exceptions.NoReverseMatch: Reverse for 'contacts' with arguments '('c', 'o', 'n', 't', 'a', 'c', 't', 's')' not found. 1 pattern(s) tried: ['contacts/(?P<order>[^/]+)\\Z']
    def test_url_available_by_name(self):
        response = self.client.get(reverse("contacts", args=("contacts",)))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("contacts", args=("contacts",)))
        self.assertTemplateUsed(response, "contacts.html")

    def test_template_content(self):
        response = self.client.get(reverse("contacts", args=("contacts",)))
        self.assertContains(response, "<h2>Contacts</h2>")
        self.assertNotContains(response, "Under construction ...")