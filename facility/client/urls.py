from django.urls import path
from . import views

#endpointy aplikace (cesta, metoda z view, nazev pro template tagy v url)
urlpatterns = [
    path('', views.home),
    path('home/', views.home, name="home"),
    path('help/', views.help_view, name="help"),
    path('about/', views.about, name="about"),  

    path('faculty/<int:faculty_id>',
         views.FacultyDevicesListView.as_view(), name='facultydevices'),
    path('organization/<int:faculty_id>',
         views.FacultyDevicesListView.as_view(), name='organizationdevices'),
    path('contact/<int:contact_id>/<str:order>',
         views.ContactDevicesListView.as_view(), name='contactdevices'),
    path('device/<int:device_id>',
         views.DeviceDetailView.as_view(), name='device'),
    path('contacts/<str:order>',
         views.ContactsListView.as_view(), name="contacts"),
    path('search_result/', views.search_result, name="search_result"),

    path("category/<int:category_id>/<str:order>",
         views.CategoryDevicesListView.as_view(), name="categorydevices"),
    path("department/<int:department_id>/<str:order>",
         views.DepartmentDevicesListView.as_view(), name="departmentdevices"),
    path("laboratory/<int:laboratory_id>/<str:order>",
         views.LaboratoryDevicesListView.as_view(), name="laboratorydevices"),
    path("usage/<int:usage_id>/<str:order>",
         views.UsageDevicesListView.as_view(), name="usagedevices"),
]
