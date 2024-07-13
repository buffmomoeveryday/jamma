import re


def ignore_urls(url, pattern_to_ignore):
    """
    Ignores URLs with the specified pattern in the path.

    Args:
        url: The URL string to check.
        pattern_to_ignore: The path pattern to ignore (e.g., "/container/detail/*").

    Returns:
        True if the URL should be ignored, False otherwise.
    """
    regex = rf"{pattern_to_ignore}$"  # Match the pattern at the end of the path
    return re.search(regex, url) is not None

