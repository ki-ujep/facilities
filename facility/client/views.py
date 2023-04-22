from django.shortcuts import render, get_object_or_404
from .models import Faculty, Contact, Device, Usage, Laboratory, Department, Category
from django.db.models import Q


def home(request):
    faculties = Faculty.objects.all().order_by("name")
    context = {
        "faculties": faculties,
    }
    return render(request, "home.html", context)

def facultydevices(request, faculty_id, order):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    if order == "asc":
        faculty_devices = Device.objects.filter(faculty=faculty).order_by("name", "department")
    else:
        faculty_devices = Device.objects.filter(faculty=faculty).order_by("-name", "department")
    context = {
        "faculty_devices": faculty_devices,
        "faculty_name": faculty.name,
        "faculty_id": faculty.id,
        "order": order
    }
    return render(request, "facultydevices.html", context)

def search_result(request):
    query = request.GET.get("query")

    devices = Device.objects.filter(Q(name=query) | Q(serial_number=query))
    
    contacts = Contact.objects.filter(Q(name=query) | Q(email=query) | Q(phone=query))
    devices = devices | Device.objects.filter(contact_id__in = contacts)

    usages = Usage.objects.filter(Q(academical_usage=query))
    devices = devices | Device.objects.filter(usage_id__in = usages)

    laboratories = Laboratory.objects.filter(Q(name=query) | Q(adress=query))
    devices = devices | Device.objects.filter(laboratory_id__in = laboratories)

    faculties = Faculty.objects.filter(Q(name=query))
    devices = devices | Device.objects.filter(faculty_id__in = faculties)

    departments = Department.objects.filter(Q(name=query))
    devices = devices | Device.objects.filter(department_id__in = departments)

    categories = Category.objects.filter(Q(name=query))
    devices = devices | Device.objects.filter(category_id__in = categories)

    faculty_name = query
    
    context = {
        "faculty_devices": devices,
        "faculty_name": faculty_name,
        "order": "disable"
    }
    return render(request, "facultydevices.html", context)

def contactdevices(request, contact_id, order):
    contact = get_object_or_404(Contact, id=contact_id)
    if order == "asc":
        contact_devices = Device.objects.filter(contact=contact).order_by("name", "department")
    else:
        contact_devices = Device.objects.filter(contact=contact).order_by("-name", "department")
    context = {
        "contact_devices": contact_devices,
        "contact_name": contact.name,
        "contact_id": contact.id,
        "order": order
    }
    return render(request, "contactdevices.html", context)

def device(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    faculty = device.faculty
    contact = device.contact
    context = {
        "device": device,
        "faculty": faculty,
        "contact": contact
    }
    return render(request, "device.html", context)

def contacts(request, order):
    if order == "asc":
        contacts = Contact.objects.all().order_by("name")
    else:
        contacts = Contact.objects.all().order_by("-name")
    context = {
        "contacts": contacts,
        "order": order
    }
    return render(request, "contacts.html", context)

def help(request):
    return render(request, "help.html")

def about(request):
    return render(request, "about.html")

