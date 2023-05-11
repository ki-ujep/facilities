from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Value
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.postgres.search import TrigramWordDistance, SearchVector, SearchQuery, SearchRank
from django.db.models.functions import Least

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

def get_category_ids(query):
    categories = Category.objects.filter(name__icontains=query)
    category_ids = []
    for category in categories:
        for node in category.walk_down():
            if node.id in category_ids:
                continue
            category_ids.append(node.id)
    return category_ids

def search_result(request):
    query = request.GET.get("query")

    search_fields = [
        'name', 'serial_number',
        'contact__name', 'contact__email', 'contact__phone',
        'usages__academical_usage',
        'laboratory__name', 'laboratory__adress',
        'faculty__name',
        'department__name',
        'category__name',
        'category__parent__name'
    ]

    vector = SearchVector(*search_fields)

    search_query = SearchQuery(query)

    category_ids = get_category_ids(query)

    rank_based_ids = Device.objects.annotate(
        search=vector
    ).filter(
        search=search_query
    ).annotate(
        rank=SearchRank(vector, search_query)
    ).order_by('-rank').values_list('id', flat=True)

    category_based_ids = Device.objects.filter(category__id__in=category_ids).values_list('id', flat=True)

    all_ids = set(list(rank_based_ids) + list(category_based_ids))

    devices = Device.objects.filter(id__in=all_ids)

    found_message = "Found " + str(devices.count()) + " records."

    # If no results found, fall back on TrigramWordDistance
    if not devices.exists():
        devices = Device.objects.annotate(
            distance=Least(*[TrigramWordDistance(query, field_name) for field_name in search_fields])
        ).order_by("distance")[:10]
        found_message = "Showing 10 closest matches."
    elif len(devices) < 10:
        trigram_devices = Device.objects.annotate(
            distance=Least(*[TrigramWordDistance(query, field_name) for field_name in search_fields])
        ).order_by("distance").exclude(id__in=all_ids)[:10 - len(devices)]
        # Filter by distance
        trigram_devices = [device for device in trigram_devices if device.distance < 0.5]
        if trigram_devices:
            found_message = f"Found {len(devices)} records. Showing {len(trigram_devices)} closest matches."
            devices = list(devices) + trigram_devices



    context = {
        "faculty_devices": devices,
        "faculty_name": query,
        "found_message": found_message,
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

