from django import template

register = template.Library()


@register.filter()
def users_image(val):
    if val:
        return f'/media/{val}'

    return '#'