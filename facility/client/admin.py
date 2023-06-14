from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .forms import FacultyAdminForm, DeviceAdminForm
from .models import Device, Usage, Laboratory, Faculty, Department, Contact, Category, Attachment, DevicePicture

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

class DevicePictureInline(admin.TabularInline):
    model = DevicePicture
    extra = 1

class DeviceAdmin(admin.ModelAdmin):
    form = DeviceAdminForm
    list_display = ("name", "serial_number", "laboratory", "department", "contact")
    inlines = [DevicePictureInline, AttachmentInline]

class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ("name", "adress", "faculty")


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty")


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")



class FacultyAdmin(admin.ModelAdmin):
    form = FacultyAdminForm

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.filter(is_partner_organization=False)

    def save_model(self, request: HttpRequest, obj: Any, form: Any, change: Any) -> None:
        obj.is_partner_organization = False
        return super().save_model(request, obj, form, change)


class PartnerOrganization(Faculty):
    class Meta:
        proxy = True
        verbose_name = "Partner Organization"
        verbose_name_plural = "Partner Organizations"


class PartnerOrganizationAdmin(admin.ModelAdmin):
    form = FacultyAdminForm
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.filter(is_partner_organization=True)

    def save_model(self, request: HttpRequest, obj: Any, form: Any, change: Any) -> None:
        obj.is_partner_organization = True
        return super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(Device, DeviceAdmin)
admin.site.register(Usage)
admin.site.register(Laboratory, LaboratoryAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(PartnerOrganization, PartnerOrganizationAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Category)
admin.site.register(Attachment)
admin.site.register(DevicePicture)
