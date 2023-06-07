from django.test import TestCase, RequestFactory
from django.urls import reverse
from client.views import search_result
from client.models import Device, Category, Laboratory, Department, Contact, Faculty, Usage

class SearchResultsViewTest(TestCase):
    """
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.factory = RequestFactory()

        # Create sample devices for the tests
        cls.category = Category.objects.create(name="TestCategory")
        cls.lab = Laboratory.objects.create(name="TestLab")
        cls.dept = Department.objects.create(name="TestDept")
        cls.contact = Contact.objects.create(name="TestContact", email="contact@test.com")
        cls.faculty = Faculty.objects.create(name="TestFaculty")
        cls.usage = Usage.objects.create(academical_usage="TestUsage")

        cls.device_matching = Device.objects.create(name="TestDevice", serial_number="123456", category=cls.category,
                                                    laboratory=cls.lab, department=cls.dept, contact=cls.contact, faculty=cls.faculty)
        cls.device_matching.usages.add(cls.usage)

        cls.device_not_matching = Device.objects.create(name="AnotherDevice", serial_number="654321", category=cls.category,
                                                        laboratory=cls.lab, department=cls.dept, contact=cls.contact, faculty=cls.faculty)
        cls.device_not_matching.usages.add(cls.usage)

    def test_uses_correct_template(self):
        request = self.factory.get(reverse('search_result') + '?query=TestDevice')
        response = search_result(request)
        self.assertTemplateUsed(response, 'devicelist.html')

    def test_context_data(self):
        request = self.factory.get(reverse('search_result') + '?query=TestDevice')
        response = search_result(request)
        self.assertIn('devices', response.context)
        self.assertIn('listing_name', response.context)
        self.assertIn('found_message', response.context)
        self.assertIn('order', response.context)

    def test_matching_devices(self):
        request = self.factory.get(reverse('search_result') + '?query=TestDevice')
        response = search_result(request)
        devices = response.context['devices']

        # The queryset should contain our matching device
        self.assertIn(self.device_matching, devices)

        # The queryset should not contain our non-matching device
        self.assertNotIn(self.device_not_matching, devices)

    def test_no_matching_devices(self):
        request = self.factory.get(reverse('search_result') + '?query=NonExistentDevice')
        response = search_result(request)
        devices = response.context['devices']

        # The queryset should not contain our matching device
        self.assertNotIn(self.device_matching, devices)

        # The queryset should contain our non-matching device
        self.assertIn(self.device_not_matching, devices)
        """
    pass
