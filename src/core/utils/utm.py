import random
import string
from urllib.parse import parse_qs, urlparse


def generate_utm_url(
    url: str,
    utm_campaign: str = "",
    utm_medium: str = "",
    utm_source: str = "",
    utm_content: str = "",
    utm_term: str = "",
) -> str:
    """Generates a URL with UTM parameters appended as a query string.

    Args:
        url (str): The base URL to which UTM parameters will be added.
        utm_campaign (str, optional): The campaign name. Defaults to "".
        utm_medium (str, optional): The advertising medium. Defaults to "".
        utm_source (str, optional): The source of the traffic. Defaults to "".
        utm_content (str, optional): The specific content (e.g., ad variation). Defaults to "".
        utm_term (str, optional): The paid keyword used. Defaults to "".

    Returns:
        str: The URL with UTM parameters appended as a query string.

    Example usage:
        base_url = "https://www.example.com/product"
        utm_campaign = "summer_sale"
        utm_medium = "email"

        final_url = generate_utm_url(base_url, utm_campaign=utm_campaign, utm_medium=utm_medium)
        print(final_url)

    """

    utm_parameters = {
        "utm_campaign": utm_campaign,
        "utm_medium": utm_medium,
        "utm_source": utm_source,
        "utm_content": utm_content,
        "utm_term": utm_term,
    }

    # Generate random string for missing parameters
    for param, value in utm_parameters.items():
        if not value:
            utm_parameters[param] = "".join(
                random.choices(string.ascii_letters + string.digits, k=10)
            )

    # Construct the query string
    query_string = "&".join(
        f"{param}={value}" for param, value in utm_parameters.items() if value
    )

    # Append the query string to the URL
    if "?" in url:
        url += f"&{query_string}"
    else:
        url += f"?{query_string}"

    return url


def parse_utm_url(url):
    from icecream import ic

    ic(url)
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    utm_params = {}
    for param, values in query_params.items():
        if param.startswith("utm_"):
            utm_params[param] = values[0] if values else ""

    return utm_params
