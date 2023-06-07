from django.test import SimpleTestCase
from django.urls import reverse, resolve
from client import views

class UrlsTest(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, views.home)

    def test_help_url_resolves(self):
        url = reverse('help')
        self.assertEquals(resolve(url).func, views.help_view)

    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEquals(resolve(url).func, views.about)

    def test_facultydevices_url_resolves(self):
        url = reverse('facultydevices', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.FacultyDevicesListView)

    def test_contactdevices_url_resolves(self):
        url = reverse('contactdevices', args=[1, 'order'])
        self.assertEquals(resolve(url).func.view_class, views.ContactDevicesListView)

    def test_device_url_resolves(self):
        url = reverse('device', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.DeviceDetailView)

    def test_contacts_url_resolves(self):
        url = reverse('contacts', args=['order'])
        self.assertEquals(resolve(url).func.view_class, views.ContactsListView)

    def test_search_result_url_resolves(self):
        url = reverse('search_result')
        self.assertEquals(resolve(url).func, views.search_result)

    def test_categorydevices_url_resolves(self):
        url = reverse('categorydevices', args=[1, 'order'])
        self.assertEquals(resolve(url).func.view_class, views.CategoryDevicesListView)

    def test_departmentdevices_url_resolves(self):
        url = reverse('departmentdevices', args=[1, 'order'])
        self.assertEquals(resolve(url).func.view_class, views.DepartmentDevicesListView)

    def test_laboratorydevices_url_resolves(self):
        url = reverse('laboratorydevices', args=[1, 'order'])
        self.assertEquals(resolve(url).func.view_class, views.LaboratoryDevicesListView)

    def test_usagedevices_url_resolves(self):
        url = reverse('usagedevices', args=[1, 'order'])
        self.assertEquals(resolve(url).func.view_class, views.UsageDevicesListView)
