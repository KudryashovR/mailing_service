from django import template


register = template.Library()


@register.filter
def media_redirection(media_url):
    return f"/media/{media_url}"
