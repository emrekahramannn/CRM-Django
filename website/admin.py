from django.contrib import admin
from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass