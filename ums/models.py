from django.db import models

# Create your models here.
class User(models.Model):
    class Role(models.TextChoices):
        Client = "client", "Client",
        Contractor = "contractor", "Contractor",
        Admin = "admin", "Admin"

    roles = models.CharField(max_length=50, choices= Role.choices)    