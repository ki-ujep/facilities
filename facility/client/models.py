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
    adress = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


# === Faculty ===
class Faculty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


# === Department ===
class Department(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"


# === Contact ===
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='img/managers', blank=True)

    def __str__(self):
        return f"{self.name}"


# === Category ===
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.name}"


# === Device ===
class Device(models.Model):
    name = models.CharField(max_length=255)
    picture_path = models.FilePathField(null=True)
    description = models.CharField(max_length=1000)
    serial_number = models.CharField(max_length=255, null=True)
    usage = models.ForeignKey(Usage, on_delete=models.SET_NULL, null=True)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}({self.serial_number})"


# === Attachment ===
class Attachment(models.Model):
    path = models.FilePathField()
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.path}"