from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import path, reverse

from .views import create_new_url, dashboard, delete_url, url_detail
from .htmx_views import get_utm_chart


def redirect_to_dashboard(request):
    return redirect(to=reverse("dashboard"))


urlpatterns = [
    path("", redirect_to_dashboard, name="index"),
    path("dashboard/", dashboard, name="dashboard"),
    path("url/create/", create_new_url, name="create_new_url"),
    path("url/<str:url>", url_detail, name="url_detail"),
    path("url/<str:url>/delete/", delete_url, name="delete_url"),
]


htmx = [
    path("charts/utm_chart/<str:url>/", get_utm_chart, name="htmx-utm-chart"),
]


urlpatterns += htmx
