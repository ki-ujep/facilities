from django import forms
from client.models import Faculty, Device


class FacultyAdminForm(forms.ModelForm):
    class Meta:
        model = Faculty
        exclude = ['is_partner_organization']

    
class DeviceAdminForm(forms.ModelForm):
    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
        label="Faculty / Organization")

    class Meta:
        model = Device
        fields = "__all__"