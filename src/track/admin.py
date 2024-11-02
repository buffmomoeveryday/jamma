from django.contrib import admin

from .models import (
    UTM,
    Event,
    PageView,
    Referer,
    UserAgent,
    Website,
    Ignore,
    TrackingURL,
)

# Register your models here.

admin.site.register(Website)
admin.site.register(PageView)buf
admin.site.register(Event)
admin.site.register(Referer)
admin.site.register(UserAgent)
admin.site.register(UTM)
admin.site.register(Ignore)
admin.site.register(TrackingURL)
