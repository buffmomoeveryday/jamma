from track.models import Website


# myapp/context_processors.py


def websites(request):
    from icecream import ic

    ic(request)
    return {"websites": getattr(request, "websites", [])}
