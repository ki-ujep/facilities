from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse
from client.models import Contact, Category, Device
from django.shortcuts import get_object_or_404

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
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Contact.objects.create(name='Test Contact 1')
        Contact.objects.create(name='Test Contact 2')

    def test_url_exists_at_correct_location(self):
        response = self.client.get(reverse("contacts", args=("name",)))
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("contacts", args=("name",)))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("contacts", args=("name",)))
        self.assertTemplateUsed(response, "contacts.html")

    def test_view_displays_contacts(self):
        response = self.client.get(reverse("contacts", args=("name",)))
        self.assertContains(response, 'Test Contact 1')
        self.assertContains(response, 'Test Contact 2')

class CategoryDevicesListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        category1 = Category.objects.create(name='Test Category 1')
        category2 = Category.objects.create(name='Test Category 2')

        Device.objects.create(name='Device 1', category=category1)
        Device.objects.create(name='Device 2', category=category1)
        Device.objects.create(name='Device 3', category=category2)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse("categorydevices", args=(1,"name")))
        self.assertEqual(response.status_code, 200)
    
    """
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("categorydevices", args=(1,"name")))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("categorydevices", args=(1,"name")))
        self.assertTemplateUsed(response, "categorydevices.html")

    def test_view_displays_correct_category_devices(self):
        response = self.client.get(reverse("categorydevices", args=(1,"name")))
        self.assertContains(response, 'Device 1')
        self.assertContains(response, 'Device 2')
        self.assertNotContains(response, 'Device 3')

        response = self.client.get(reverse("categorydevices", args=(2,"name")))
        self.assertContains(response, 'Device 3')
        self.assertNotContains(response, 'Device 1')
        self.assertNotContains(response, 'Device 2')
        """
    # TODO: test for correct reverse url