from django.db import models

# Create your models here.
class Agreement(models.Model):
   class Status(models.TextChoices):
         PENDING = "pending", "Pending"
         FUNDED = "funded", "funded"
         APPROVED= "approved", "Approved"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="agreement_as_client", on_delete=models.CASCADE)
    contractor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="agreement_as_contractor", on_delete=models.CASCADE)
    amount = models. DecimalField(max_digits=15, decimal_places=2)
    descriptions = models.TextField()
    status = models.CharField(max_length=100, choices=Status.choices, default="PENDING")
    created_at = models.DateTimeField(auto_add_now=True)

class Milestone(models.Model):
    agreement= models.ForeignKey(Agreement, related_name="agreement",on_delete=models.CASCADE),
    title = models.CharField(max_length=200, blank=False)
    amount = models.DecimalField(max_digit=15, decimal_places=2)
    created_at = models.DateTimeField(auto_add_now=True)
    status = models.CharField(max_length=100, default="PENDING")
    due_date= models.DateTimeField(null=True, auto_add_now=True)


class Entry(models.Model):
    class EntryType(models.TextChoices):
           FUNDING = "funding", "Funding",
           RELEASE =  "releasing", "Releasing",

    agreement= models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ledger_entry")
    amount= models.DecimalField(max_digit=15, decimal_places=2)
    type= models.CharField(max_length=100, type=EntryType.choices)
    timestamp = models.DateTimeField(auto_add_now=True)


class Audit(models.Model):
    agreement = models.ForeignKey(Agreement, related_name="audit_log", on_delete=models.CASCADE)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

