def create_url_string(domain):
    URL = f"<script defer data-domain='http://{domain}' src='https://jamma.buffmomo.xyz/api/script.js'></script>"
    url = URL.replace("'", '"')
    return url


def visitor_ip_address(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip