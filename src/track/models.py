from datetime import datetime, timedelta

from django.db import models
from django.db.models import Count, Q
from django.utils import timezone

from core.models import BaseModel
from user.models import User


class Website(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Website Name")
    url = models.CharField(unique=True, verbose_name="Website URL", max_length=255)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name} - {self.url}"

    def calculate_bounce_rate(self):
        page_views = PageView.objects.filter(website=self)
        sessions = page_views.values("ip_address").annotate(visit_count=Count("id"))

        from icecream import ic

        single_page_sessions = 0
        total_sessions = 0

        for session in sessions:
            total_sessions += 1
            if session["visit_count"] == 1:
                single_page_sessions += 1

        # Calculate bounce rate
        bounce_rate = (
            (single_page_sessions / total_sessions) * 100 if total_sessions > 0 else 0
        )

        return round(bounce_rate, 2)


class PageView(BaseModel):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)

    timestamp = models.DateTimeField()
    url = models.URLField()
    referrer = models.URLField(blank=True, null=True)
    user_agent = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=255, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "timestamp",
                    "website",
                    "url",
                ],
            ),
        ]

    def __str__(self):
        return f"{self.website.name} - {self.url} - {self.timestamp}"

    @classmethod
    def has_visited_today(cls, ip_address, current_url):
        now = timezone.now()
        start_of_day = timezone.make_aware(datetime(now.year, now.month, now.day))
        end_of_day = start_of_day + timedelta(days=1)

        query = cls.objects.filter(
            Q(ip_address=ip_address)
            & Q(timestamp__gte=start_of_day)
            & Q(timestamp__lt=end_of_day)
            & Q(url=current_url)
        )

        has_visited: bool = query.exists()
        return has_visited


class Event(BaseModel):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)

    page_view = models.ForeignKey(PageView, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    event_properties = models.JSONField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"{self.page_view} - {self.name} - {self.timestamp}"


class Referer(BaseModel):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)

    url = models.URLField()
    referer_type = models.CharField(max_length=255)
    internal = models.BooleanField(default=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.website.name}'s {self.url}"


class UserAgent(BaseModel):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)

    user_agent = models.CharField(max_length=255, unique=True)
    browser = models.CharField(max_length=255)
    browser_version = models.CharField(max_length=255, null=True)
    operating_system = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return f" {self.website.name}-{self.user_agent}"


class UTM(BaseModel):
    website = models.ForeignKey(
        Website,
        on_delete=models.CASCADE,
        related_name="utms",
    )

    utm_medium = models.CharField(max_length=255)
    utm_source = models.CharField(max_length=255)
    utm_campaign = models.CharField(max_length=255)
    utm_content = models.TextField()
    utm_term = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return f" {self.website.name}-{self.utm_medium}"


class Ignore(BaseModel):
    webiste = models.ForeignKey(Website, on_delete=models.CASCADE)

    ignore_regex = models.CharField(max_length=255, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.ignore_regex
