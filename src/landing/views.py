from datetime import datetime

import ipinfo
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db import IntegrityError
from icecream import ic as iceicebaby
from silk.profiling.profiler import silk_profile

from core.utils.url import create_url_string
from landing.form import NewUrlForm
from track.models import Website

import asyncio


@login_required(login_url="/login")
def dashboard(request):
    user_website = Website.objects.filter(owner=request.user)

    context = {
        "user_website": user_website,
    }

    return render(
        request=request,
        template_name="landing/dashboard.html",
        context=context,
    )


@login_required(login_url="/login")
def create_new_url(request):
    form = NewUrlForm(request.POST or None)

    if request.method == "GET":
        context = {
            "form": form,
        }
        return render(request, "urls/create_new_url.html", context=context)

    if request.method == "POST":
        if form.is_valid():
            website_name = form.cleaned_data.get("name")

            if "https://" in form.cleaned_data.get("url"):
                website_url = str(form.cleaned_data.get("url")).replace("https://", "")
            else:
                website_url = str(form.cleaned_data.get("url")).replace("http://", "")

            try:
                website = Website.objects.create(
                    owner=request.user, url=website_url, name=website_name
                )
                website.save()
                messages.success(
                    request=request,
                    message=f"Website {website_url} created successfully",
                )
                return redirect("dashboard")
            except IntegrityError as e:

                messages.error(
                    request=request,
                    message=f"Website Already Exists someone already has registred this website",
                )
                return redirect("create_new_url")

        else:
            messages.error(request=request, message=f"{form.errors}")

    context = {"form": form}
    return render(request, "urls/create_new_url.html", context=context)


@login_required(login_url="/login")
def delete_url(request, url):
    website = get_object_or_404(Website, url=url)
    try:
        website.delete()
        messages.success(
            request=request, message=f"Website {website.url} deleted successfully"
        )
        return redirect(reversed("dashboard"))
    except Exception as e:
        messages.error(request=request, message="Some error occoured")
        return redirect(request.META["HTTP_REFERER"])


from django.db.models import Count

from track.models import PageView
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


@login_required(login_url="/login")
def url_detail(request, url):
    website = Website.objects.filter(url=url).prefetch_related("pageview_set").first()
    url_string = create_url_string(domain=url)

    result = PageView.objects.filter(website=website).aggregate(
        unique_views=Count("ip_address", distinct=True)
    )

    list_of_unique_urls = (
        PageView.objects.filter(website=website)
        .values("url")
        .annotate(url_count=Count("url"))
        .order_by("-url_count")
    )
    count_of_unqiue_urls = (
        PageView.objects.filter(website=website).values("url").count()
    )

    bounce = website.calculate_bounce_rate()

    labels = [item["url"] for item in list_of_unique_urls]
    data = [item["url_count"] for item in list_of_unique_urls]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    return render(
        request=request,
        template_name="urls/detail_url.html",
        context={
            "chart_labels": labels,
            "chart_data": data,
            "website": website.url,
            "last_updated": datetime.now(),
            "url_string": url_string,
            "detail": website,
            "unique": result["unique_views"],
            "urls": list_of_unique_urls,
            "count": count_of_unqiue_urls,
            "bounce": bounce,
        },
    )
