from django.test import TestCase
from client.models import Usage, Laboratory, Faculty, Department, Contact, Category, Device, Attachment, DevicePicture

class UsageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Usage.objects.create(academical_usage='Test Usage')

    def test_academical_usage_label(self):
        usage = Usage.objects.get(id=1)
        field_label = usage._meta.get_field('academical_usage').verbose_name
        self.assertEqual(field_label,'academical usage')


class LaboratoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Laboratory.objects.create(name='Test Lab', adress='Test Adress')

    def test_name_label(self):
        laboratory = Laboratory.objects.get(id=1)
        field_label = laboratory._meta.get_field('name').verbose_name
        self.assertEqual(field_label,'name')


class FacultyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Faculty.objects.create(name='Test Faculty')

    def test_name_label(self):
        faculty = Faculty.objects.get(id=1)
        field_label = faculty._meta.get_field('name').verbose_name
        self.assertEqual(field_label,'name')


class DepartmentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Department.objects.create(name='Test Department')

    def test_name_label(self):
        department = Department.objects.get(id=1)
        field_label = department._meta.get_field('name').verbose_name
        self.assertEqual(field_label,'name')


class ContactModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Contact.objects.create(name='Test Contact')

    def test_name_label(self):
        contact = Contact.objects.get(id=1)
        field_label = contact._meta.get_field('name').verbose_name
        self.assertEqual(field_label,'name')


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.category1 = Category.objects.create(name='Test Category1')
        cls.category2 = Category.objects.create(name='Test Category2', parent=cls.category1)
        cls.category3 = Category.objects.create(name='Test Category3', parent=cls.category2)
        cls.category4 = Category.objects.create(name='Test Category4')
        cls.device = Device.objects.create(name='Test Device', serial_number='123456', category=cls.category3)

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label,'name')

    def test_walk_method(self):
        categories = [cat.name for cat in self.category3.walk()]
        self.assertListEqual(categories, ['Test Category1', 'Test Category2', 'Test Category3'])

    def test_walk_down_method(self):
        categories = [cat.name for cat in self.category1.walk_down()]
        self.assertListEqual(categories, ['Test Category1', 'Test Category2', 'Test Category3'])

    def test_have_children_devices_method(self):
        self.assertTrue(self.category1.have_children_devices())
        self.assertTrue(self.category2.have_children_devices())
        self.assertTrue(self.category3.have_children_devices())
        self.assertFalse(self.category4.have_children_devices())

class DeviceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Device.objects.create(name='Test Device', serial_number='123456')

    def test_name_label(self):
        device = Device.objects.get(id=1)
        field_label = device._meta.get_field('name').verbose_name
        self.assertEqual(field_label,'name')

class AttachmentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Attachment.objects.create()

    def test_file_label(self):
        attachment = Attachment.objects.get(id=1)
        field_label = attachment._meta.get_field('file').verbose_name
        self.assertEqual(field_label,'file')


class DevicePictureModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Device.objects.create(name='Test Device', serial_number='123456')
        DevicePicture.objects.create(device=Device.objects.get(id=1))

    def test_image_label(self):
        device_picture = DevicePicture.objects.get(id=1)
        field_label = device_picture._meta.get_field('image').verbose_name
        self.assertEqual(field_label,'image')