from django.db import models
from django.db.models import Manager


class AccessLogEntry(models.Model):
    class Meta:
        verbose_name_plural = "Access log entries"

    objects: Manager

    datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    ip = models.CharField(max_length=31, db_index=True, blank=True)
    is_authenticated = models.BooleanField(db_index=True)
    is_superuser = models.BooleanField(db_index=True)
    username = models.CharField(max_length=100, blank=True, db_index=True)
    email = models.CharField(max_length=100, blank=True, db_index=True)
    method = models.CharField(max_length=10, db_index=True)
    path = models.CharField(max_length=1000, db_index=True)
    query_string = models.CharField(max_length=1000, db_index=True)
    status_code = models.IntegerField(db_index=True)
    reason_phrase = models.CharField(max_length=100, blank=True, db_index=True)
    request_meta_str = models.TextField(blank=True)

    @classmethod
    def create(
        cls,
        ip: str,
        is_authenticated: bool,
        is_superuser: bool,
        username: str,
        email: str,
        method: str,
        path: str,
        query_string: str,
        status_code: int,
        reason_phrase: str,
        request_meta: str,
    ) -> "AccessLogEntry":
        return AccessLogEntry.objects.create(
            ip=ip,
            is_authenticated=is_authenticated,
            is_superuser=is_superuser,
            username=username,
            email=email,
            method=method,
            path=path,
            query_string=query_string,
            status_code=status_code,
            reason_phrase=reason_phrase,
            request_meta_str=request_meta,
        )


class IgnoredIpPrefix(models.Model):
    class Meta:
        verbose_name_plural = "Ignored IP prefixes"

    objects: Manager
    prefix = models.CharField(max_length=31, db_index=True, unique=True)

    @classmethod
    def has_match(cls, ip: str) -> bool:
        for obj in IgnoredIpPrefix.objects.all():
            if ip.startswith(obj.prefix):
                return True
        return False
