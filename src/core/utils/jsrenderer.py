from ninja.renderers import BaseRenderer


class MyRenderer(BaseRenderer):
    media_type = "text/javascript"

    def render(self, request, data, *, response_status):
        return ...  # your serialization here
