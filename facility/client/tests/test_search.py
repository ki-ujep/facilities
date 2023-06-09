from django.test import TestCase
from django.urls import reverse
from client.models import Device, Category, Laboratory, Department, Contact, Faculty, Usage

class SearchResultViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up Faculty for the devices
        cls.faculty1 = Faculty.objects.create(name='Test Faculty 1')

        # Set up Category for the devices
        cls.category1 = Category.objects.create(name='Category 1')

        # Set up Department for the devices
        cls.department1 = Department.objects.create(name='Department 1', faculty=cls.faculty1)

        # Set up Laboratory for the devices
        cls.laboratory1 = Laboratory.objects.create(name='Laboratory 1', adress='Address 1', faculty=cls.faculty1)

        # Set up Usage for the devices
        cls.usage1 = Usage.objects.create(academical_usage='Usage 1')

        # Set up Contact for the devices
        cls.contact1 = Contact.objects.create(name='Contact 1', email='contact1@test.com', phone='123456789')

        # Set up Device
        cls.device1 = Device.objects.create(
            name='Device 1',
            serial_number='1234',
            faculty=cls.faculty1,
            contact=cls.contact1,
            laboratory=cls.laboratory1,
            department=cls.department1,
            category=cls.category1,
        )
        cls.device1.usages.add(cls.usage1)

    def test_search_sql_injection(self):
        response = self.client.get(reverse('search_result'), {'query': "' OR 1=1; --"})
        self.assertEqual(response.status_code, 200)

    def test_search_long_input(self):
        long_query = 'a' * 10000
        response = self.client.get(reverse('search_result'), {'query': long_query})
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("search_result") + '?query=Device%201')
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("search_result") + '?query=Device%201')
        self.assertTemplateUsed(response, "devicelist.html")

    def test_search_by_device_name(self):
        response = self.client.get(reverse('search_result') + '?query=Device%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_serial_number(self):
        response = self.client.get(reverse('search_result') + '?query=1234')
        self.assertContains(response, 'Device 1')

    def test_search_by_contact_name(self):
        response = self.client.get(reverse('search_result') + '?query=Contact%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_contact_email(self):
        response = self.client.get(reverse('search_result') + '?query=contact1@test.com')
        self.assertContains(response, 'Device 1')

    def test_search_by_contact_phone(self):
        response = self.client.get(reverse('search_result') + '?query=123456789')
        self.assertContains(response, 'Device 1')

    def test_search_by_academical_usage(self):
        response = self.client.get(reverse('search_result') + '?query=Usage%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_laboratory_name(self):
        response = self.client.get(reverse('search_result') + '?query=Laboratory%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_laboratory_address(self):
        response = self.client.get(reverse('search_result') + '?query=Address%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_faculty_name(self):
        response = self.client.get(reverse('search_result') + '?query=Test%20Faculty%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_department_name(self):
        response = self.client.get(reverse('search_result') + '?query=Department%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_category_name(self):
        response = self.client.get(reverse('search_result') + '?query=Category%201')
        self.assertContains(response, 'Device 1')
