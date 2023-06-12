from django.db import models

# === Models for Todos app ===

"""
All models for facilities application.

1. **Usage** - The main view for Todos ([[models.py#usage]])
2. **Laboratory** - called to delete a todo ([[models.py#laboratoy]])
3. **Faculty** - called to add a new todo ([[models.py#faculty]])
4. **Department** - called to add a new todo (jump to section in [[models.py#department]] )
5. **Contact** - called to add a new todo (jump to section in [[models.py#contact]] )
6. **Category** - called to add a new todo (jump to section in [[models.py#category]] )
7. **Device** - called to add a new todo (jump to section in [[models.py#device]] )
8. **Attachment** - The main view for Todos (jump to section in [[models.py#attachment]] )

"""

# === Usage ===
class Usage(models.Model):
    """
    The Usage class defines the type of Device model way of using at facilities. Usage will be rendered in templates and will be available for filtering.
    Each Usage has only one field:
    academical_usage - stores the type of academical usage
    """
    academical_usage = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.academical_usage}"


# === Laboratory ===
class Laboratory(models.Model):
    name = models.CharField(max_length=255)
    adress = models.CharField(max_length=255, null=True, blank=True)
    faculty = models.ForeignKey('Faculty', on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name_plural = "Laboratories"

    def __str__(self):
        return f"{self.name}"


# === Faculty ===
class Faculty(models.Model):
    name = models.CharField(max_length=255)
    logo_en = models.ImageField(upload_to="faculties_logo/", max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)
    is_partner_organization = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        return f"{self.name}"


# === Department ===
class Department(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.name}"


# === Contact ===
class Contact(models.Model):
    name = models.CharField(max_length=255)
    titles = models.CharField(max_length=255, null=True, blank=True)
    titles_after = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='managers/', max_length=255, blank=True,
                              default="managers/male.png")

    def __str__(self):
        return f"{self.name}"


# === Category ===
class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children',
                               on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Categories"

    def walk(self, path=None):
        """Returns list of parent categories in order from top parent 
        (current object is last in the list)."""
        if path is None:
            path = []
        if self.parent is not None:
            self.parent.walk(path)
        path.append(self)
        return path

    def walk_down(self, path=None):
        """Returns list of child categories in order from top parent 
        (current object is first in the list)."""
        if path is None:
            path = []
        path.append(self)
        children = Category.objects.filter(parent=self)
        if children is not None:
            for child in children.all():
                child.walk_down(path)
        return path

    def have_children_devices(self):
        """Returns True if current category have devices in child Categories
        recursively."""
        children = Category.objects.filter(parent=self)
        if children is not None:
            for child in children.all():
                if child.have_children_devices():
                    return True
        devices = Device.objects.filter(category=self)
        if devices is not None and devices.count() > 0:
            return True
        return False

    def __str__(self):
        path = [cat.name for cat in self.walk()]
        return ' -> '.join(path)

# === Device ===
class Device(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True, blank=True)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    usages = models.ManyToManyField(Usage, blank=True)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.PROTECT, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.name}({self.serial_number})"


# === Attachment ===
class Attachment(models.Model):
    file = models.FileField(upload_to="attachments/", max_length=255, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True,
                               related_name="attachments")

    def __str__(self):
        return f"{self.file.name}"

class DevicePicture(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="device_pictures/", max_length=255)

    def __str__(self):
        return f"{self.device.name} - {self.image.name}"

