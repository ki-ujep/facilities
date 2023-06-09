from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse
from client.models import Contact, Category, Device, Faculty, Department, Laboratory, Usage
from django.shortcuts import get_object_or_404

class AboutPageTests(SimpleTestCase):
    def __init__(self, *args, **kwargs):
        self.client = Client()
        super(AboutPageTests, self).__init__(*args, **kwargs)

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
        # Create a few Contact instances with all fields
        cls.contact1 = Contact.objects.create(
            name='Contact Test1',
            titles='Mr.',
            titles_after='PhD',
            email='contact1@test.com',
            phone='1234567890',
            photo='managers/contact1.png'
        )
        cls.contact2 = Contact.objects.create(
            name='Contact Test2',
            titles='Mrs.',
            titles_after='MSc',
            email='contact2@test.com',
            phone='0987654321',
            photo='managers/contact2.png'
        )

    def test_url_available_by_name(self):
        response = self.client.get(reverse("contacts", args=("name",)))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("contacts", args=("name",)))
        self.assertTemplateUsed(response, "contacts.html")

    def test_contacts_list_view(self):
        response = self.client.get(reverse('contacts', kwargs={'order': 'asc'}))

        # Check that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the details of the contacts
        self.assertContains(response, 'Contact Test1')
        self.assertContains(response, 'Mr.')
        self.assertContains(response, 'PhD')
        self.assertContains(response, 'contact1@test.com')
        self.assertContains(response, '1234567890')
        self.assertContains(response, 'managers/contact1.png')

        self.assertContains(response, 'Contact Test2')
        self.assertContains(response, 'Mrs.')
        self.assertContains(response, 'MSc')
        self.assertContains(response, 'contact2@test.com')
        self.assertContains(response, '0987654321')
        self.assertContains(response, 'managers/contact2.png')

class FacultyDevicesListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up two Faculties, Categories, Departments, Laboratories, and Devices
        cls.faculty1 = Faculty.objects.create(name='Faculty 1')
        cls.category1 = Category.objects.create(name='Category 1')
        cls.department1 = Department.objects.create(name='Department 1', faculty=cls.faculty1)
        cls.laboratory1 = Laboratory.objects.create(name='Laboratory 1', faculty=cls.faculty1)
        cls.device1 = Device.objects.create(name='Device 1', category=cls.category1,
                                            department=cls.department1, laboratory=cls.laboratory1,
                                            faculty=cls.faculty1)

        cls.faculty2 = Faculty.objects.create(name='Faculty 2')
        cls.category2 = Category.objects.create(name='Category 2')
        cls.department2 = Department.objects.create(name='Department 2', faculty=cls.faculty2)
        cls.laboratory2 = Laboratory.objects.create(name='Laboratory 2', faculty=cls.faculty2)
        cls.device2 = Device.objects.create(name='Device 2', category=cls.category2,
                                            department=cls.department2, laboratory=cls.laboratory2,
                                            faculty=cls.faculty2)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("facultydevices", args=[self.faculty1.id]))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("facultydevices", args=[self.faculty1.id]))
        self.assertTemplateUsed(response, "facultydevices.html")

    def test_response_data(self):
        response = self.client.get(reverse('facultydevices', args=[self.faculty1.id]))

        # Convert response content to string
        content = str(response.content)

        # Check the devices of faculty1 are in the response content
        self.assertIn(self.device1.name, content)
        self.assertIn(self.category1.name, content)
        self.assertIn(self.department1.name, content)
        self.assertIn(self.laboratory1.name, content)

        # Check the devices of faculty2 are not in the response content
        self.assertNotIn(self.device2.name, content)
        self.assertNotIn(self.category2.name, content)
        self.assertNotIn(self.department2.name, content)
        self.assertNotIn(self.laboratory2.name, content)

class CategoryDevicesListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up Faculty for the devices
        cls.faculty = Faculty.objects.create(name='Test Faculty')

        # Set up two Categories and two Devices for each category
        cls.category1 = Category.objects.create(name='Category 1')
        cls.device1a = Device.objects.create(name='Device 1a', category=cls.category1, faculty=cls.faculty)
        cls.device1b = Device.objects.create(name='Device 1b', category=cls.category1, faculty=cls.faculty)

        cls.category2 = Category.objects.create(name='Category 2')
        cls.device2a = Device.objects.create(name='Device 2a', category=cls.category2, faculty=cls.faculty)
        cls.device2b = Device.objects.create(name='Device 2b', category=cls.category2, faculty=cls.faculty)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("categorydevices", kwargs={'category_id': self.category1.id, 'order': 'asc'}))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("categorydevices", kwargs={'category_id': self.category1.id, 'order': 'asc'}))
        self.assertTemplateUsed(response, "categorydevices.html")

    def test_response_data(self):
        response = self.client.get(reverse('categorydevices', kwargs={'category_id': self.category1.id, 'order': 'asc'}))
        content = str(response.content)

        # Check the devices of category1 are in the response content
        self.assertIn(self.device1a.name, content)
        self.assertIn(self.device1b.name, content)

        # Check the devices of category2 are not in the response content
        self.assertNotIn(self.device2a.name, content)
        self.assertNotIn(self.device2b.name, content)

    def test_ordering(self):
        response = self.client.get(reverse('categorydevices', kwargs={'category_id': self.category1.id, 'order': 'desc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1b, self.device1a])

        response = self.client.get(reverse('categorydevices', kwargs={'category_id': self.category1.id, 'order': 'asc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1a, self.device1b])

class DepartmentDevicesListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up Faculty for the devices
        cls.faculty = Faculty.objects.create(name='Test Faculty')

        # Set up two Departments and two Devices for each department
        cls.department1 = Department.objects.create(name='Department 1', faculty=cls.faculty)
        cls.device1a = Device.objects.create(name='Device 1a', department=cls.department1, faculty=cls.faculty)
        cls.device1b = Device.objects.create(name='Device 1b', department=cls.department1, faculty=cls.faculty)

        cls.department2 = Department.objects.create(name='Department 2', faculty=cls.faculty)
        cls.device2a = Device.objects.create(name='Device 2a', department=cls.department2, faculty=cls.faculty)
        cls.device2b = Device.objects.create(name='Device 2b', department=cls.department2, faculty=cls.faculty)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("departmentdevices", kwargs={'department_id': self.department1.id, 'order': 'asc'}))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("departmentdevices", kwargs={'department_id': self.department1.id, 'order': 'asc'}))
        self.assertTemplateUsed(response, "departmentdevices.html")

    def test_response_data(self):
        response = self.client.get(reverse('departmentdevices', kwargs={'department_id': self.department1.id, 'order': 'asc'}))
        content = str(response.content)

        # Check the devices of department1 are in the response content
        self.assertIn(self.device1a.name, content)
        self.assertIn(self.device1b.name, content)

        # Check the devices of department2 are not in the response content
        self.assertNotIn(self.device2a.name, content)
        self.assertNotIn(self.device2b.name, content)

    def test_ordering(self):
        response = self.client.get(reverse('departmentdevices', kwargs={'department_id': self.department1.id, 'order': 'desc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1b, self.device1a])

        response = self.client.get(reverse('departmentdevices', kwargs={'department_id': self.department1.id, 'order': 'asc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1a, self.device1b])

class LaboratoryDevicesListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up Faculty for the devices
        cls.faculty = Faculty.objects.create(name='Test Faculty')

        # Set up two Laboratories and two Devices for each laboratory
        cls.laboratory1 = Laboratory.objects.create(name='Laboratory 1', faculty=cls.faculty)
        cls.device1a = Device.objects.create(name='Device 1a', laboratory=cls.laboratory1, faculty=cls.faculty)
        cls.device1b = Device.objects.create(name='Device 1b', laboratory=cls.laboratory1, faculty=cls.faculty)

        cls.laboratory2 = Laboratory.objects.create(name='Laboratory 2', faculty=cls.faculty)
        cls.device2a = Device.objects.create(name='Device 2a', laboratory=cls.laboratory2, faculty=cls.faculty)
        cls.device2b = Device.objects.create(name='Device 2b', laboratory=cls.laboratory2, faculty=cls.faculty)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("laboratorydevices", kwargs={'laboratory_id': self.laboratory1.id, 'order': 'asc'}))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("laboratorydevices", kwargs={'laboratory_id': self.laboratory1.id, 'order': 'asc'}))
        self.assertTemplateUsed(response, "laboratorydevices.html")

    def test_response_data(self):
        response = self.client.get(reverse('laboratorydevices', kwargs={'laboratory_id': self.laboratory1.id, 'order': 'asc'}))
        content = str(response.content)

        # Check the devices of laboratory1 are in the response content
        self.assertIn(self.device1a.name, content)
        self.assertIn(self.device1b.name, content)

        # Check the devices of laboratory2 are not in the response content
        self.assertNotIn(self.device2a.name, content)
        self.assertNotIn(self.device2b.name, content)

    def test_ordering(self):
        response = self.client.get(reverse('laboratorydevices', kwargs={'laboratory_id': self.laboratory1.id, 'order': 'desc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1b, self.device1a])

        response = self.client.get(reverse('laboratorydevices', kwargs={'laboratory_id': self.laboratory1.id, 'order': 'asc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1a, self.device1b])

from django.urls import reverse

class UsageDevicesListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up Faculty for the devices
        cls.faculty = Faculty.objects.create(name='Test Faculty')

        # Set up two Usages and two Devices for each usage
        cls.usage1 = Usage.objects.create(academical_usage='Usage 1')
        cls.device1a = Device.objects.create(name='Device 1a', faculty=cls.faculty)
        cls.device1b = Device.objects.create(name='Device 1b', faculty=cls.faculty)
        cls.device1a.usages.add(cls.usage1)
        cls.device1b.usages.add(cls.usage1)

        cls.usage2 = Usage.objects.create(academical_usage='Usage 2')
        cls.device2a = Device.objects.create(name='Device 2a', faculty=cls.faculty)
        cls.device2b = Device.objects.create(name='Device 2b', faculty=cls.faculty)
        cls.device2a.usages.add(cls.usage2)
        cls.device2b.usages.add(cls.usage2)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("usagedevices", kwargs={'usage_id': self.usage1.id, 'order': 'asc'}))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("usagedevices", kwargs={'usage_id': self.usage1.id, 'order': 'asc'}))
        self.assertTemplateUsed(response, "usagedevices.html")

    def test_response_data(self):
        response = self.client.get(reverse('usagedevices', kwargs={'usage_id': self.usage1.id, 'order': 'asc'}))
        content = str(response.content)

        # Check the devices of usage1 are in the response content
        self.assertIn(self.device1a.name, content)
        self.assertIn(self.device1b.name, content)

        # Check the devices of usage2 are not in the response content
        self.assertNotIn(self.device2a.name, content)
        self.assertNotIn(self.device2b.name, content)

    def test_ordering(self):
        response = self.client.get(reverse('usagedevices', kwargs={'usage_id': self.usage1.id, 'order': 'desc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1b, self.device1a])

        response = self.client.get(reverse('usagedevices', kwargs={'usage_id': self.usage1.id, 'order': 'asc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1a, self.device1b])

class ContactDevicesListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a Faculty instance
        cls.faculty = Faculty.objects.create(name='Faculty Test')

        # Create a Department instance
        cls.department = Department.objects.create(name='Department Test', faculty=cls.faculty)

        # Create a Category instance
        cls.category = Category.objects.create(name='Category Test')

        # Create two Contact instances
        cls.contact1 = Contact.objects.create(name='Contact1 Test')
        cls.contact2 = Contact.objects.create(name='Contact2 Test')

        # Create devices for each contact
        cls.device1 = Device.objects.create(
            name='Device1', serial_number='123', 
            contact=cls.contact1, category=cls.category, 
            department=cls.department, faculty=cls.faculty,
        )

        cls.device2 = Device.objects.create(
            name='Device2', serial_number='456', 
            contact=cls.contact2, category=cls.category, 
            department=cls.department, faculty=cls.faculty,
        )

    def test_url_available_by_name(self):
        response = self.client.get(reverse("contactdevices", kwargs={'contact_id': self.contact1.id, 'order': 'asc'}))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("contactdevices", kwargs={'contact_id': self.contact1.id, 'order': 'asc'}))
        self.assertTemplateUsed(response, "contactdevices.html")

    def test_response_data(self):
        response = self.client.get(reverse('contactdevices', kwargs={'contact_id': self.contact1.id, 'order': 'asc'}))
        self.assertContains(response, 'Device1')
        self.assertNotContains(response, 'Device2')

        response = self.client.get(reverse('contactdevices', kwargs={'contact_id': self.contact2.id, 'order': 'asc'}))
        self.assertContains(response, 'Device2')
        self.assertNotContains(response, 'Device1')

    def test_ordering(self):
        # Create another device for contact1
        device3 = Device.objects.create(
            name='Device0', serial_number='789', 
            contact=self.contact1, category=self.category, 
            department=self.department, faculty=self.faculty,
        )

        response = self.client.get(reverse('contactdevices', kwargs={'contact_id': self.contact1.id, 'order': 'asc'}))
        # Verify device3 appears before device1 in the response because it's name is 'Device0' which comes before 'Device1' in alphabetical order
        self.assertLess(response.content.index(b'Device0'), response.content.index(b'Device1'))

class DeviceDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a Faculty instance
        cls.faculty = Faculty.objects.create(name='Faculty Test')

        # Create a Department instance
        cls.department = Department.objects.create(name='Department Test', faculty=cls.faculty)

        # Create a Category instance
        cls.category = Category.objects.create(name='Category Test')

        # Create a Laboratory instance
        cls.laboratory = Laboratory.objects.create(name='Laboratory Test', faculty=cls.faculty)

        # Create a Contact instance
        cls.contact = Contact.objects.create(name='Contact Test')

        # Create a Usage instance
        cls.usage = Usage.objects.create(academical_usage='Usage Test')

        # Create a Device instance
        cls.device = Device.objects.create(
            name='Device Test', 
            serial_number='123',
            contact=cls.contact,
            department=cls.department,
            faculty=cls.faculty,
            category=cls.category,
            laboratory=cls.laboratory,
        )
        cls.device.usages.add(cls.usage)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("device", kwargs={'device_id': self.device.id}))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("device", kwargs={'device_id': self.device.id}))
        self.assertTemplateUsed(response, "device.html")

    def test_device_detail_view(self):
        response = self.client.get(reverse('device', kwargs={'device_id': self.device.id}))

        self.assertContains(response, 'Device Test')
        self.assertContains(response, '123')  # Serial number
        self.assertContains(response, 'Contact Test')
        self.assertContains(response, 'Department Test')
        self.assertContains(response, 'Faculty Test')
        self.assertContains(response, 'Category Test')
        self.assertContains(response, 'Laboratory Test')
        self.assertContains(response, 'Usage Test')
