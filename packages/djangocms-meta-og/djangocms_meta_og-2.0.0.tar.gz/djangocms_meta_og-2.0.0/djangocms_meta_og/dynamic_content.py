from urllib.parse import quote

from django.http import HttpRequest


def get_current_page_url(request: HttpRequest, *args) -> str:
    """Get current page url."""
    return quote(request.build_absolute_uri(request.current_page.get_absolute_url()), "&?")


def get_current_page_title(request: HttpRequest, *args) -> str:
    """Get current page title."""
    return request.current_page.get_page_title()


def get_current_page_description(request: HttpRequest, *args) -> str:
    """Get current page description."""
    return request.current_page.get_meta_description()


def get_filer_image_url(request: HttpRequest, *args) -> str:
    """Get Filer Image URL."""
    if not (args and args[0]):
        return ""  # The meta og specification is missing a parameter.
    try:
        pk = int(args[0])
    except ValueError:
        return ""  # Parameter is not an integer.
    try:
        from filer.models import Image
    except ModuleNotFoundError:
        return ""  # There is no dependency on the Filer module.
    try:
        img = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        return ""  # Image with given id not found.
    return request.build_absolute_uri(img.file.url)
