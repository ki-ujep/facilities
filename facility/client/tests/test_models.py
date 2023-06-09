from django.test import TestCase
from client.models import Usage, Laboratory, Faculty, Department, Contact, Category, Device, Attachment, DevicePicture
from unittest.mock import MagicMock
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

class UsageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Usage.objects.create(academical_usage='Test Usage')

    def test_object_created(self):
        usage = Usage.objects.get(academical_usage='Test Usage')
        self.assertEqual(usage.academical_usage, 'Test Usage')

class LaboratoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Faculty.objects.create(name='Test Faculty')
        Laboratory.objects.create(name='Test Lab', adress='Test Address', faculty=Faculty.objects.get(name='Test Faculty'))

    def test_object_created(self):
        lab = Laboratory.objects.get(name='Test Lab')
        self.assertEqual(lab.name, 'Test Lab')
        self.assertEqual(lab.adress, 'Test Address')

class FacultyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Faculty.objects.create(name='Test Faculty')

    def test_object_created(self):
        faculty = Faculty.objects.get(name='Test Faculty')
        self.assertEqual(faculty.name, 'Test Faculty')

class DepartmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Faculty.objects.create(name='Test Faculty')
        Department.objects.create(name='Test Department', faculty=Faculty.objects.get(name='Test Faculty'))

    def test_object_created(self):
        department = Department.objects.get(name='Test Department')
        self.assertEqual(department.name, 'Test Department')

class ContactModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Contact.objects.create(name='Test Contact')

    def test_object_created(self):
        contact = Contact.objects.get(name='Test Contact')
        self.assertEqual(contact.name, 'Test Contact')

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name='Test Category1')
        cls.category2 = Category.objects.create(name='Test Category2', parent=cls.category1)

    def test_object_created(self):
        category1 = Category.objects.get(name='Test Category1')
        self.assertEqual(category1.name, 'Test Category1')
        category2 = Category.objects.get(name='Test Category2')
        self.assertEqual(category2.name, 'Test Category2')

class DeviceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usage = Usage.objects.create(academical_usage='Test Usage')
        cls.faculty = Faculty.objects.create(name='Test Faculty')
        cls.category = Category.objects.create(name='Test Category')
        cls.contact = Contact.objects.create(name='Test Contact')
        cls.department = Department.objects.create(name='Test Department', faculty=cls.faculty)
        cls.laboratory = Laboratory.objects.create(name='Test Laboratory', faculty=cls.faculty, adress='Test Address')
        cls.device = Device.objects.create(
            name="Test Device",
            description="This is a test device",
            serial_number="12345",
            laboratory=cls.laboratory,
            department=cls.department,
            contact=cls.contact,
            category=cls.category,
            faculty=cls.faculty,
        )
        cls.device.usages.add(cls.usage)

    def test_object_created(self):
        device = Device.objects.get(name='Test Device')
        self.assertEqual(device.name, 'Test Device')
        self.assertEqual(device.description, 'This is a test device')
        self.assertEqual(device.serial_number, '12345')

class AttachmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = Device.objects.create(name='Test Device', serial_number='12345')

        # mock an uploaded file
        file_mock = MagicMock(spec=File)
        file_mock.name = 'test_file.pdf'
        file_mock.size = 50_000
        Attachment.objects.create(device=cls.device, file=file_mock)

    def test_object_created(self):
        attachment = Attachment.objects.get(device=self.device)
        self.assertTrue(isinstance(attachment, Attachment))
        self.assertIn('test_file', attachment.file.name)


class DevicePictureModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = Device.objects.create(name='Test Device', serial_number='12345')

        # mock an uploaded image
        image_mock = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        DevicePicture.objects.create(device=cls.device, image=image_mock)

    def test_object_created(self):
        picture = DevicePicture.objects.get(device=self.device)
        self.assertTrue(isinstance(picture, DevicePicture))
        # test that the image name contains test_image
        self.assertIn('test_image', picture.image.name)
