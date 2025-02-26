from django.contrib import admin
from .models import AccessLogEntry, IgnoredIpPrefix

@admin.register(IgnoredIpPrefix)
class IgnoredIpPrefixAdmin(admin.ModelAdmin):
    list_display = (
        IgnoredIpPrefix.prefix.field.name,
    )

@admin.register(AccessLogEntry)
class AccessLogEntryAdmin(admin.ModelAdmin):
    list_display = (
        AccessLogEntry.datetime.field.name,
        "id",
        AccessLogEntry.ip.field.name,
        AccessLogEntry.username.field.name,
        AccessLogEntry.method.field.name,
        AccessLogEntry.path.field.name,
        AccessLogEntry.status_code.field.name,
        AccessLogEntry.reason_phrase.field.name,
        AccessLogEntry.is_authenticated.field.name,
        AccessLogEntry.is_superuser.field.name,
    )

    search_fields = (
        AccessLogEntry.ip.field.name,
        AccessLogEntry.username.field.name,
        AccessLogEntry.path.field.name,
        AccessLogEntry.reason_phrase.field.name,
    )

    list_filter = (
        AccessLogEntry.is_authenticated.field.name,
        AccessLogEntry.username.field.name,
        AccessLogEntry.method.field.name,
        AccessLogEntry.status_code.field.name,
        AccessLogEntry.is_superuser.field.name,
    )
