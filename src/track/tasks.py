import asyncio
import random
from urllib.parse import urlparse

import ipinfo
from asgiref.sync import async_to_sync
from celery import shared_task
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer
from django.conf import settings
from icecream import ic

from core.utils.utm import parse_utm_url

from .models import UTM, Event, PageView, Referer, UserAgent, Website

IP_INFO_TOKEN = settings.IP_INFO_TOKEN

channel_layer = get_channel_layer()
logger = get_task_logger(__name__)


@shared_task
def parse_utm_and_save(url: str, website: int) -> None:
    utm_list = parse_utm_url(url)

    if bool(utm_list):
        website = Website.objects.get(id=website)
        medium = utm_list["utm_medium"] or None
        source = utm_list["utm_source"] or None
        campaign = utm_list["utm_campaign"] or None
        term = utm_list["utm_term"] or None

        UTM.objects.create(
            website=website,
            utm_medium=medium,
            utm_source=source,
            utm_campaign=campaign,
            utm_term=term,
        )


@shared_task
def parse_agent_and_save(
    website: int,
    browser: str,
    browser_version: str,
    operating_system: str,
) -> None:

    website = Website.objects.get(id=website)
    UserAgent.objects.create(
        website=website,
        user_agent=random.randint(a=10, b=98744),
        browser=browser,
        browser_version=browser_version,
        operating_system=operating_system,
    )


@shared_task
def parse_referer_and_save(referer_url, website: int) -> str:
    website = Website.objects.get(id=website)
    ref_url = urlparse(referer_url)

    if website.url == ref_url.netloc:
        referer = Referer.objects.create(
            website=website,
            url=referer_url,
            referer_type="Test",
            internal=True,
        )
        return referer.url

    referer = Referer.objects.create(
        website=website,
        url=referer_url,
        referer_type="Test",
    )


@shared_task(name="Parsing Page View")
def parse_page_view_and_save(
    website: int, url, referer, user_agent, ip_address, timestamp, event_type: str
) -> str:
    ic(website)

    website = Website.objects.get(id=website)
    # address = ipinfo.getHandler(IP_INFO_TOKEN).getDetails(ip_address)
    address = "Nepal"
    page_view = PageView.objects.create(
        website=website,
        timestamp=timestamp,
        url=url,
        referrer=referer,
        user_agent=user_agent,
        ip_address=ip_address,
        country=str(address),
    )

    event = Event.objects.create(
        website=website,
        page_view=page_view,
        name=event_type,
        timestamp=timestamp,
        event_properties=None,
    )

    count_of_unqiue_urls = (
        PageView.objects.filter(website=website).values("url").count()
    )

    message_dic = {
        "type": "send_unique_page_view",
        "text": str(count_of_unqiue_urls),
    }

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(
        channel_layer.group_send("usergroup", message_dic),
    )

    return "Done"
