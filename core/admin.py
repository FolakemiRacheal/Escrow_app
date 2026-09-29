from django.contrib import admin
from core.models import Agreement, Entry, Audit, Milestone

# Register your models here.
admin.site.register(Agreement)
admin.site.register(Entry)
admin.site.register(Audit)
admin.site.register(Milestone)