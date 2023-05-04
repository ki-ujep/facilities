from django.contrib import admin
from .models import Device, Usage, Laboratory, Faculty, Department, Contact, Category, Attachment

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "serial_number", "laboratory", "department", "contact")
    inlines = [AttachmentInline]


class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ("name", "adress")


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty")


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")


# Register your models here.
admin.site.register(Device, DeviceAdmin)
admin.site.register(Usage)
admin.site.register(Laboratory, LaboratoryAdmin)
admin.site.register(Faculty)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Category)
admin.site.register(Attachment)
