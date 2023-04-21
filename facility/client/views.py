from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Faculty, Contact, Device, Usage, Laboratory, Department, Category
from django.db.models import Q


def home(request):
    template = loader.get_template("home.html")
    faculties = Faculty.objects.all().order_by("name").values()
    context = {
        "faculties": faculties,
    }
    return HttpResponse(template.render(context, request))


def facultydevices(request, faculty_id, order):
    template = loader.get_template("facultydevices.html")
    if order == "asc":
        faculty_devices = Device.objects.filter(faculty_id=faculty_id).order_by("name", "department")
    else:
        faculty_devices = Device.objects.filter(faculty_id=faculty_id).order_by("-name", "department")
    faculty_name = Faculty.objects.get(id=faculty_id).name
    context = {
        "faculty_devices": faculty_devices,
        "faculty_name": faculty_name,
        "faculty_id": faculty_id,
        "order": order
    }
    return HttpResponse(template.render(context, request))


def search_result(request):
    template = loader.get_template("facultydevices.html")
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
    return HttpResponse(template.render(context, request))


def contactdevices(request, contact_id, order):
    template = loader.get_template("contactdevices.html")
    if order == "asc":
        contact_devices = Device.objects.filter(contact_id=contact_id).order_by("name", "department")
    else:
        contact_devices = Device.objects.filter(contact_id=contact_id).order_by("-name", "department")
    contact_name = Contact.objects.get(id=contact_id).name
    context = {
        "contact_devices": contact_devices,
        "contact_name": contact_name,
        "contact_id": contact_id,
        "order": order
    }
    return HttpResponse(template.render(context, request))


def device(request, device_id):
    template = loader.get_template("device.html")
    device = Device.objects.get(id=device_id)
    faculty = Faculty.objects.get(id=device.faculty_id)
    contact = Contact.objects.get(id=device.contact_id)
    context = {
        "device": device,
        "faculty": faculty,
        "contact": contact
    }
    return HttpResponse(template.render(context, request))


def contacts(request, order):
    template = loader.get_template("contacts.html")
    if order=="asc":
        contacts = Contact.objects.all().order_by("name").values()
    else:
        contacts = Contact.objects.all().order_by("-name").values()
    context = {
        "contacts": contacts,
        "order": order
    }
    return HttpResponse(template.render(context, request))


def help(request):
    template = loader.get_template("help.html")
    return HttpResponse(template.render())


def about(request):
    template = loader.get_template("about.html")
    return HttpResponse(template.render())