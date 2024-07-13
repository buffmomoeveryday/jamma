from track.models import Website, UTM
from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from silk.profiling.profiler import silk_profile

from django.db.models import Count, Sum
from django.db.models.functions import Coalesce

from user.models import User


# @login_required
# @silk_profile(name="UTM Chart Profiling")
def get_utm_chart(request, url):
    try:
        user = User.objects.get(id=1)
        website = Website.objects.get(owner=user, url=url)

    except Website.DoesNotExist:
        return render(request, "404.html")

    utm_data = website.utms.values(
        "utm_medium",
        "utm_source",
        "utm_campaign",
        "utm_term",
    ).annotate(
        utm_medium_count=Count("utm_medium"),
        utm_source_count=Count("utm_source"),
        utm_campaign_count=Count("utm_campaign"),
        utm_term_count=Count("utm_term"),
    )

    list_of_medium_utms = utm_data.values("utm_medium", "utm_medium_count").distinct()
    list_of_source_utms = utm_data.values("utm_source", "utm_source_count").distinct()
    list_of_campaign_utms = utm_data.values(
        "utm_campaign", "utm_campaign_count"
    ).distinct()
    list_of_term_utms = utm_data.values("utm_term", "utm_term_count").distinct()

    context = {
        "list_of_medium_utms": list_of_medium_utms,
        "list_of_source_utms": list_of_source_utms,
        "list_of_campaign_utms": list_of_campaign_utms,
        "list_of_term_utms": list_of_term_utms,
    }

    return render(
        request=request,
        template_name="htmx/charts/utm_chart.html",
        context=context,
    )
