import os
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse, HttpRequest
from icecream import ic as iceicebaby
from rest_framework.response import Response
from rest_framework.views import APIView
from user_agents import parse

from core.utils.url import visitor_ip_address
from ninja import NinjaAPI


from .models import PageView, Website
from .seralizer import EventSerializers
from .tasks import (
    parse_agent_and_save,
    parse_page_view_and_save,
    parse_referer_and_save,
    parse_utm_and_save,
)

BASE_DIR = settings.BASE_DIR
SECRET = settings.SECRET_KEY

api = NinjaAPI()


@api.get("/test")
def test(request):
    return {"0": "0"}


class BaseScript(APIView):
    """
    This is the view that provides the tracking script for the website
    """

    def get(self, request):
        script = os.path.join(BASE_DIR, "core/static/js/script.js")
        with open(script, "r") as f:
            js = f.read()
        return HttpResponse(js, content_type="application/javascript")


class EventTrackingScript(APIView):
    def get(self, request):
        script = os.path.join(BASE_DIR, "core/static/js/script.event.js")
        with open(script, "r") as f:
            js = f.read()

        return HttpResponse(js, content_type="application/javascript")


from .models import Event


class EventApi(APIView):
    def get(self, request):
        event = Event.objects.all()
        events = EventSerializers(data=event)
        return Response(events)


class TrackAPI(APIView):
    def post(self, request: HttpRequest) -> Response:
        events = EventSerializers(data=request.data)

        if events.is_valid():
            event_type: str = events.data["n"]
            current_url: str = events.data["u"]
            referer: str = events.data["r"]
        else:
            return Response({"500": events.errors})

        user_agent = parse(request.META.get("HTTP_USER_AGENT", ""))

        if "https" in str(request.headers["Origin"]):
            base_url = str(request.headers["Origin"]).replace("https://", "")
        else:
            base_url = str(request.headers["Origin"]).replace("http://", "")

        user_ip = visitor_ip_address(request)

        website = Website.objects.get(url=base_url)

        browser = user_agent.browser.family
        browser_version = user_agent.browser.version_string
        operating_system = user_agent.os.family

        has_visited: bool = PageView.has_visited_today(user_ip, current_url)

        parse_page_view_and_save.delay(
            website=website.id,
            timestamp=datetime.now(),
            url=current_url,
            referer=referer,
            user_agent=str(request.META.get("HTTP_USER_AGENT", "")),
            ip_address=user_ip,
            event_type=event_type,
        )

        if "utm" in current_url:
            parse_utm_and_save.delay(url=current_url, website=website.id)

        if referer:
            parse_referer_and_save.delay(
                referer_url=referer,
                website=website.id,
            )

        if not has_visited:
            parse_agent_and_save.delay(
                browser_version=browser_version,
                browser=browser,
                operating_system=operating_system,
                website=website.id,
            )

        return Response(
            {
                "ok": 200,
            },
        )


class EventTrackAPI(APIView):
    def post(self, request):
        iceicebaby(request.data)
        return Response(
            {"ok": 200},
        )


class TestApi(APIView):
    def get(self, request):
        return Response({"ok": 200})
