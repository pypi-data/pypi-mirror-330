import logging

from django.http import HttpRequest, HttpResponse

from .ipware import get_client_ip

_log = logging.getLogger(__name__)


class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response: HttpResponse = self.get_response(request)
        try:
            _log_request(request, response)
        except Exception as e:
            _log.exception(e)
        return response


def _log_request(request: HttpRequest, response: HttpResponse):
    from .models import AccessLogEntry, IgnoredIpPrefix

    ip, _ = get_client_ip(request)

    if IgnoredIpPrefix.has_match(ip):
        return

    user = request.user
    method = request.method
    is_authenticated = user.is_authenticated
    is_superuser = getattr(user, "is_superuser", False)
    username = getattr(user, "username", "")
    email = getattr(user, "email", "")
    path = request.path
    query_string = request.META.get("QUERY_STRING", "")
    request_meta = "\n".join(f"{k}: {v}" for k, v in request.META.items())

    AccessLogEntry.create(
        ip,
        is_authenticated,
        is_superuser,
        username,
        email,
        method,
        path,
        query_string,
        response.status_code,
        response.reason_phrase,
        request_meta,
    )
