from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from .models import Faculty, Contact, Device, Usage, Laboratory, Department, Category


def help_view(request):
    return render(request, "help.html")

def about(request):
    return render(request, "about.html")

def home(request):
    faculties = Faculty.objects.all().order_by("name")
    context = {
        "faculties": faculties,
    }
    return render(request, "home.html", context)

class FacultyDevicesListView(ListView):
    model = Device
    template_name = "facultydevices.html"
    context_object_name = "faculty_devices"

    def get_queryset(self):
        faculty_id = self.kwargs.get("faculty_id")
        order = self.kwargs.get("order")
        faculty = get_object_or_404(Faculty, id=faculty_id)
        if order == "asc":
            return Device.objects.filter(faculty=faculty).order_by("name", "department")
        else:
            return Device.objects.filter(faculty=faculty).order_by("-name", "department")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculty_id = self.kwargs.get("faculty_id")
        order = self.kwargs.get("order")
        faculty = get_object_or_404(Faculty, id=faculty_id)
        context["faculty_name"] = faculty.name
        context["faculty_id"] = faculty.id
        context["order"] = order
        return context

def search_result(request):
    query = request.GET.get("query")

    search_vector = SearchVector(
        'name', 'serial_number',
        'contact__name', 'contact__email', 'contact__phone',
        'usage__academical_usage',
        'laboratory__name', 'laboratory__adress',
        'faculty__name',
        'department__name',
        'category__name'
    )

    search_query = SearchQuery(query)
    search_rank = SearchRank(search_vector, search_query)

    devices = Device.objects.annotate(
        search=search_vector,
        rank=search_rank
    ).filter(search=search_query).order_by('-rank')

    print(devices)

    context = {
        "faculty_devices": devices,
        "faculty_name": query,
        "order": "disable"
    }

    return render(request, "facultydevices.html", context)

class ContactDevicesListView(ListView):
    model = Device
    template_name = "contactdevices.html"
    context_object_name = "contact_devices"

    def get_queryset(self):
        contact_id = self.kwargs.get("contact_id")
        order = self.kwargs.get("order")
        contact = get_object_or_404(Contact, id=contact_id)
        if order == "asc":
            return Device.objects.filter(contact=contact).order_by("name", "department")
        else:
            return Device.objects.filter(contact=contact).order_by("-name", "department")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact_id = self.kwargs.get("contact_id")
        order = self.kwargs.get("order")
        contact = get_object_or_404(Contact, id=contact_id)
        context["contact_name"] = contact.name
        context["contact_id"] = contact.id
        context["order"] = order
        return context

class DeviceDetailView(DetailView):
    model = Device
    template_name = "device.html"

    def get_object(self, queryset=None):
        device_id = self.kwargs.get("device_id")
        return get_object_or_404(Device, id=device_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faculty"] = self.object.faculty
        context["contact"] = self.object.contact
        return context

class ContactsListView(ListView):
    model = Contact
    template_name = "contacts.html"
    context_object_name = "contacts"

    def get_queryset(self):
        order = self.kwargs.get("order")
        if order == "asc":
            return Contact.objects.all().order_by("name")
        else:
            return Contact.objects.all().order_by("-name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.kwargs.get("order")
        context["order"] = order
        return context

