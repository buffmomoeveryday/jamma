from django.utils.deprecation import MiddlewareMixin
from track.models import Website
import logging

logger = logging.getLogger(__name__)


class WebsiteListMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            website_qs = Website.objects.filter(owner=request.user)
            websites = [{"url": website.url} for website in website_qs]
            request.websites = websites
            logger.debug(f"Websites added to request: {request.websites}")
        else:
            request.websites = []
            logger.debug("No websites available for unauthenticated user")
