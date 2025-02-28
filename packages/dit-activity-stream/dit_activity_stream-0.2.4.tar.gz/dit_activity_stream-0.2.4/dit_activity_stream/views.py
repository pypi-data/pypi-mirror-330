from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from django.views import View
from django_hawk.middleware import HawkResponseMiddleware
from django_hawk.utils import DjangoHawkAuthenticationFailed, authenticate_request

from dit_activity_stream.client import get_activity_stream_client


class DitActivityStreamView(View):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.client = get_activity_stream_client()

    @decorator_from_middleware(HawkResponseMiddleware)
    def dispatch(self, request, *args, **kwargs):
        if not self.authenticate(request):
            return self.forbidden()

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.client.render_page(request)

    def authenticate(self, request):
        # Ensure not being accessed via public networking
        via_public_internet = "x-forwarded-for" in request.headers
        if via_public_internet:
            return False

        # Try to authenticate with Django Hawk
        try:
            authenticate_request(request=request)
        except DjangoHawkAuthenticationFailed:
            return False

        return True

    def forbidden(self):
        return JsonResponse(
            data={},
            status=403,
        )
