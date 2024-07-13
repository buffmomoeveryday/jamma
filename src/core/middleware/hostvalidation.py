from django.core.exceptions import DisallowedHost


class HostValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        HOST = request.META["HTTP_HOST"]

        if "fest" in HOST:
            raise DisallowedHost("Cannot Continue My Darling")

        response = self.get_response(request)
        request.test = "hif"

        return response
