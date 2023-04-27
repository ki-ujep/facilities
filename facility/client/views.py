from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

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

    devices = Device.objects.filter(Q(name=query) | Q(serial_number=query))
    
    contacts = Contact.objects.filter(Q(name=query) | Q(email=query) | Q(phone=query))
    devices = devices | Device.objects.filter(contact_id__in = contacts)

    usages = Usage.objects.filter(Q(academical_usage=query))
    devices = devices | Device.objects.filter(usages__in=usages)

    laboratories = Laboratory.objects.filter(Q(name=query) | Q(adress=query))
    devices = devices | Device.objects.filter(laboratory__in = laboratories)

    faculties = Faculty.objects.filter(Q(name=query))
    devices = devices | Device.objects.filter(faculty_id__in = faculties)

    departments = Department.objects.filter(Q(name=query))
    devices = devices | Device.objects.filter(department_id__in = departments)

    # Recursively search categories
    def get_descendants(category):
        descendants = list(category.children.all())
        for child in category.children.all():
            descendants.extend(get_descendants(child))
        return descendants

    categories = Category.objects.filter(Q(name=query))
    descendant_categories = []
    for category in categories:
        descendant_categories.extend(get_descendants(category))

    all_categories = list(categories) + descendant_categories
    devices = devices | Device.objects.filter(category_id__in=all_categories)

    # Fix device duplicates
    devices = devices.distinct()

    faculty_name = query
    
    context = {
        "faculty_devices": devices,
        "faculty_name": faculty_name,
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

