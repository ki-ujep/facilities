from django.urls import path
from . import views

#endpointy aplikace (cesta, metoda z view, nazev pro template tagy v url)
urlpatterns = [
    path('', views.home),
    path('home/', views.home, name="home"),
    path('facultydevices/<int:faculty_id>/<str:order>', views.facultydevices, name='facultydevices'),
    path('contactdevices/<int:contact_id>/<str:order>', views.contactdevices, name='contactdevices'),
    path('device/<int:device_id>', views.device, name='device'),
    path('contacts/<str:order>', views.contacts, name="contacts"),
    path('help/', views.help, name="help"),
    path('about/', views.about, name="about"),  
    path('search_result/', views.search_result, name="search_result"),
]