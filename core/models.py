from django.db import models
from django.conf import settings

class Agreement(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        FUNDED = "funded", "Funded"
        APPROVED = "approved", "Approved"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="agreement_as_client", on_delete=models.CASCADE)
    contractor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="agreement_as_contractor", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)


class Milestone(models.Model):
    agreement = models.ForeignKey(Agreement, related_name="milestones", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)


class Entry(models.Model):
    class EntryType(models.TextChoices):
        FUNDING = "funding", "Funding"
        RELEASE = "release", "Release"

    agreement = models.ForeignKey(Agreement, related_name="ledger", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(max_length=20, choices=EntryType.choices)
    timestamp = models.DateTimeField(auto_now_add=True)


class Audit(models.Model):
    agreement = models.ForeignKey(Agreement, related_name="audit_log", on_delete=models.CASCADE)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)