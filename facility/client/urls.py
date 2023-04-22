from django.urls import path
from . import views

#endpointy aplikace (cesta, metoda z view, nazev pro template tagy v url)
urlpatterns = [
    path('', views.home),
    path('home/', views.home, name="home"),
    path('help/', views.help_view, name="help"),
    path('about/', views.about, name="about"),  

    path('facultydevices/<int:faculty_id>/<str:order>',
         views.FacultyDevicesListView.as_view(), name='facultydevices'),
    path('contactdevices/<int:contact_id>/<str:order>',
         views.ContactDevicesListView.as_view(), name='contactdevices'),
    path('device/<int:device_id>',
         views.DeviceDetailView.as_view(), name='device'),
    path('contacts/<str:order>',
         views.ContactsListView.as_view(), name="contacts"),
    path('search_result/', views.search_result, name="search_result"),
]
