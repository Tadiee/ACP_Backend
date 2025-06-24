from django.middleware.csrf import CsrfViewMiddleware
from django.http import JsonResponse
from django.conf import settings

class DisableCSRFOnAPI:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip CSRF for API endpoints
        if request.path.startswith('/upload/') or request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)
