from django.urls import path

from .consumers import PageViewConsumer

ws_pattern = [
    path("ws/pageview/", PageViewConsumer.as_asgi(), name="pageview"),
]
