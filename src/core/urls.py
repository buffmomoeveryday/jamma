from django.contrib import admin
from django.urls import include, path

from track.api import (
    BaseScript,
    TrackAPI,
    EventTrackAPI,
    EventTrackingScript,
    TestApi,
    EventApi,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("landing.urls")),
    path("", include("user.urls")),
]

debg = [
    path("silk/", include("silk.urls", namespace="silk")),
    # path("__debug__/", include("debug_toolbar.urls")),
]

api = [
    path(
        "api/script.js",
        BaseScript.as_view(),
        name="basescript",
    ),
    path(
        "api/script.event.js",
        EventTrackingScript.as_view(),
        name="event-tracking-script",
    ),
    path(
        "api/track",
        TrackAPI.as_view(),
        name="trackapi",
    ),
    path(
        "api/event",
        EventTrackAPI.as_view(),
        name="event-track-event",
    ),
    path("api/test", TestApi.as_view()),
    path("api/ne", EventApi.as_view()),
]


urlpatterns += debg
urlpatterns += api
